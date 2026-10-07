"""Build the personal site from Markdown without Zola.

The existing content and Anemone markup are intentionally kept separate from
this small build pipeline so that the visual design can evolve independently.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import html
import json
import re
import shutil
import subprocess
import tomllib
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt
from PIL import Image
from pygments.lexers import get_lexer_by_name
from pygments.token import Comment, Keyword, Name, Number, String
from pygments.util import ClassNotFound


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
BASE_URL = "https://guochenmeinian.github.io"
SHORTCODE = re.compile(r"\{\{\s*([a-zA-Z_]+)\((.*?)\)\s*\}\}", re.DOTALL)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).lower().replace("_", "-")
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def url_for(path: str) -> str:
    return BASE_URL + path


def parse_markdown(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"\A\+\+\+\s*\n(.*?)\n\+\+\+\s*\n?", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Missing TOML front matter: {path}")
    return tomllib.loads(match.group(1)), raw[match.end():]


def route_for(path: Path) -> str:
    rel = path.relative_to(CONTENT).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] in ("index", "_index"):
        parts.pop()
    return "/" + "/".join(slugify(part) for part in parts) + ("/" if parts else "")


def parse_shortcode_arguments(raw: str) -> dict:
    call = ast.parse(f"f({raw})", mode="eval").body
    if not isinstance(call, ast.Call) or call.args:
        raise ValueError(f"Unsupported shortcode arguments: {raw}")
    return {item.arg: ast.literal_eval(item.value) for item in call.keywords}


class Builder:
    def __init__(self, output: Path):
        self.output = output
        self.env = Environment(
            loader=FileSystemLoader(ROOT / "site_templates"),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=False,
        )
        self.env.globals["get_url"] = self.get_url
        self.env.filters["slugify"] = slugify
        self.markdown = MarkdownIt("default", {"html": True, "highlight": self.highlight_code})
        self.markdown.enable("table")
        self.images: dict[tuple, str] = {}
        self.legacy_images = json.loads((ROOT / "image_manifest.json").read_text(encoding="utf-8"))
        self.config = {
            "title": "",
            "base_url": BASE_URL,
            "generate_feed": True,
            "extra": {
                "header_nav": [
                    {"name": "/about/", "url": "/about"},
                    {"name": "/work/", "url": "/work"},
                    {"name": "/interests/", "url": "/interests"},
                ],
                "twitter_card": True,
            },
        }

    @staticmethod
    def get_url(path: str, trailing_slash: bool = False) -> str:
        result = "/" + path.lstrip("/")
        if trailing_slash and not result.endswith("/"):
            result += "/"
        return result

    @staticmethod
    def highlight_code(code: str, language: str, _attributes: str) -> str | None:
        if not language:
            return ('<pre style="background-color:#151515;color:#e8e8d3;"><code>'
                    + html.escape(code) + '</code></pre>')
        try:
            lexer = get_lexer_by_name(language)
        except ClassNotFound:
            return None
        fragments = []
        for token, value in lexer.get_tokens(code):
            if token in Name.Class or token in Name.Builtin or (token in Name and value.isupper()):
                color = "#ffb964"
            elif token in Name.Function:
                color = "#fad07a"
            elif token in Keyword and token not in Keyword.Constant:
                color = "#8fbfdc"
            elif token in Number:
                color = "#cf6a4c"
            elif token in Comment:
                color = "#888888"
            elif token in String:
                color = "#99ad6a"
            else:
                color = None
            fragment = html.escape(value)
            fragments.append(f'<span style="color:{color};">{fragment}</span>' if color else fragment)
        body = "".join(fragments)
        label = html.escape(language, quote=True)
        return (f'<pre data-lang="{label}" style="background-color:#151515;color:#e8e8d3;" '
                f'class="language-{label}"><code class="language-{label}" data-lang="{label}">{body}</code></pre>')

    def resized_image(self, args: dict) -> str:
        source = CONTENT / args["path"]
        if not source.is_file():
            raise FileNotFoundError(source)
        op = args.get("op", "fit")
        width, height = int(args["width"]), int(args["height"])
        kind = args.get("format", "auto")
        key = (str(source), width, height, op, kind)
        if key not in self.images:
            original = self.legacy_images.get(args["path"])
            if (original and original["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
                    and all(original[field] == value for field, value in
                            {"width": width, "height": height, "op": op, "format": kind}.items())
                    and (ROOT / "static" / "processed_images" / original["file"]).is_file()):
                self.images[key] = "/processed_images/" + original["file"]
                return self.images[key]
            digest = hashlib.sha256(source.read_bytes() + repr(key[1:]).encode()).hexdigest()[:12]
            suffix = ".jpg" if kind == "jpg" else source.suffix.lower()
            if suffix not in (".png", ".jpg", ".jpeg", ".webp"):
                suffix = ".png"
            name = f"{source.stem}.{digest}{suffix}"
            destination = self.output / "processed_images" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source) as image:
                if op == "fit_width":
                    size = (width, max(1, round(image.height * width / image.width)))
                elif op == "fit_height":
                    size = (max(1, round(image.width * height / image.height)), height)
                elif op == "fit":
                    ratio = min(width / image.width, height / image.height)
                    size = (max(1, round(image.width * ratio)), max(1, round(image.height * ratio)))
                else:
                    raise ValueError(f"Unsupported image operation: {op}")
                image.resize(size, Image.Resampling.LANCZOS).save(destination)
            self.images[key] = "/processed_images/" + name
        return self.images[key]

    def render_body(self, raw: str, metadata: dict) -> str:
        def replace(match: re.Match) -> str:
            name, args = match.group(1), parse_shortcode_arguments(match.group(2))
            if name == "resize_image":
                src = html.escape(self.resized_image(args), quote=True)
                return f'<img src="{src}" />'
            if name in ("double_image", "youtube"):
                return self.env.get_template(f"shortcodes/{name}.html").render(**args)
            raise ValueError(f"Unsupported shortcode: {name}")

        raw = SHORTCODE.sub(replace, raw)
        # This is used by the existing resume page, outside a shortcode.
        raw = raw.replace("{{ page.extra.path }}", html.escape(metadata.get("extra", {}).get("path", ""), quote=True))
        return self.markdown.render(raw)

    def write(self, route: str, text: str) -> None:
        if route.endswith("/"):
            path = self.output / route.lstrip("/") / "index.html"
        else:
            path = self.output / route.lstrip("/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def render(self, template: str, **context) -> str:
        defaults = {"page": {"extra": {}, "taxonomies": {}}, "section": {"extra": {}},
                    "paginator": None, "lang": "en", "config": self.config}
        defaults.update(context)
        return self.env.get_template(template).render(**defaults)

    def collect(self) -> tuple[list[dict], dict[str, dict]]:
        pages, sections = [], {}
        for path in sorted(CONTENT.rglob("*.md")):
            meta, raw = parse_markdown(path)
            route = route_for(path)
            location = path.relative_to(CONTENT).parts[0]
            category = meta.get("category") or (location if location in ("work", "interests") else None)
            if location == "blogs" and path.name != "_index.md" and category not in ("work", "interests"):
                raise ValueError(f"Blog article needs category = 'work' or 'interests': {path}")
            entry = {
                "source": path, "route": route, "permalink": url_for(route),
                "title": meta.get("title", ""), "description": meta.get("description", ""),
                "date": meta.get("date"), "taxonomies": meta.get("taxonomies", {"tags": []}),
                "extra": meta.get("extra", {}), "slug": route.rstrip("/").split("/")[-1],
                "toc": [], "content": self.render_body(raw, meta),
                "category": category,
            }
            if path.name == "_index.md":
                entry["pages"] = []
                sections[route] = entry
            else:
                pages.append(entry)
        return pages, sections

    def render_listing(self, route: str, section: dict, pages: list[dict]) -> None:
        section["pages"] = pages
        chunks = [pages[i:i + 10] for i in range(0, len(pages), 10)] or [[]]
        for index, chunk in enumerate(chunks, 1):
            paginator = None
            if len(chunks) > 1:
                paginator = {
                    "pages": chunk, "current_index": index, "number_pagers": len(chunks),
                    "first": route, "last": f"{route}page/{len(chunks)}/",
                    "previous": route if index == 2 else (f"{route}page/{index - 1}/" if index > 2 else None),
                    "next": f"{route}page/{index + 1}/" if index < len(chunks) else None,
                }
            rendered = self.render("section.html", section=section, paginator=paginator)
            self.write(route if index == 1 else f"{route}page/{index}/", rendered)
            if index == 1 and len(chunks) > 1:
                self.write(f"{route}page/1/", self.env.get_template("redirect.html").render(target=route))

    def build(self) -> None:
        if self.output == ROOT or self.output == CONTENT:
            raise ValueError("Output must be a separate directory")
        if self.output.exists():
            shutil.rmtree(self.output)
        self.output.mkdir(parents=True)
        shutil.copytree(ROOT / "static", self.output, dirs_exist_ok=True)
        pages, sections = self.collect()
        for page in pages:
            source_dir = page["source"].parent
            if page["source"].stem == "index":
                for asset in source_dir.iterdir():
                    if asset.is_file() and asset.suffix.lower() != ".md":
                        destination = self.output / page["route"].lstrip("/") / asset.name
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(asset, destination)
            self.write(page["route"], self.render("page.html", page=page))

        blogs = sorted((page for page in pages if page["category"] in ("work", "interests")),
                       key=lambda page: (-(page["date"].toordinal() if page["date"] else 0), page["source"].name))
        for route, section in sections.items():
            if route in ("/blogs/", "/work/", "/interests/"):
                listing = blogs if route == "/blogs/" else [page for page in blogs if page["category"] == route.strip("/")]
                self.render_listing(route, section, listing)
            elif route == "/":
                self.write(route, self.env.get_template("redirect.html").render(target="/about/"))
            else:
                self.write(route, self.render("section.html", section=section))

        tags: dict[str, list[dict]] = {}
        for page in pages:
            for tag in page["taxonomies"].get("tags", []):
                tags.setdefault(tag, []).append(page)
        terms = []
        for tag, tagged_pages in sorted(tags.items()):
            tagged_pages.sort(key=lambda page: (-(page["date"].toordinal() if page["date"] else 0), page["source"].name))
            term = {"name": tag, "slug": slugify(tag), "pages": tagged_pages,
                    "permalink": url_for("/tags/" + slugify(tag) + "/")}
            terms.append(term)
            self.write(f"/tags/{term['slug']}/", self.render("tags-single.html", term=term))
        self.write("/tags/", self.render("tags-list.html", taxonomy={"name": "tags"}, terms=terms))

        routes = [*sections.keys(), *[page["route"] for page in pages], "/tags/",
                  *[f"/tags/{term['slug']}/" for term in terms]]
        sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for route in routes:
            ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = url_for(route)
        self.write("/sitemap.xml", ET.tostring(sitemap, encoding="unicode", xml_declaration=True))
        self.write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")

        feed = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom")
        ET.SubElement(feed, "title").text = "Guochenmeinian's Blog"
        ET.SubElement(feed, "id").text = BASE_URL + "/"
        ET.SubElement(feed, "updated").text = datetime.now(timezone.utc).isoformat()
        for page in blogs[:20]:
            item = ET.SubElement(feed, "entry")
            ET.SubElement(item, "title").text = page["title"]
            ET.SubElement(item, "id").text = page["permalink"]
            ET.SubElement(item, "link", href=page["permalink"])
            if isinstance(page["date"], date):
                ET.SubElement(item, "updated").text = page["date"].isoformat() + "T00:00:00Z"
        self.write("/atom.xml", ET.tostring(feed, encoding="unicode", xml_declaration=True))

        searchable = [sections["/"], sections["/blogs/"], sections["/work/"], sections["/interests/"],
                      *(page for page in pages if page["route"] != "/about/2024/")]
        search = [{"id": item["permalink"], "title": item["title"],
                   "body": html.unescape(re.sub(r"<[^>]+>", " ", item["content"]))}
                  for item in searchable]
        index = subprocess.run(
            ["node", str(ROOT / "build_search.js")], input=json.dumps(search, ensure_ascii=False),
            text=True, capture_output=True, check=True,
        ).stdout
        self.write("/search_index.en.js", index)
        self.write("/404.html", self.render("404.html"))
        print(f"Built {len(pages)} pages, {len(sections)} sections, {len(terms)} tags into {self.output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "public")
    args = parser.parse_args()
    Builder(args.output.resolve()).build()
