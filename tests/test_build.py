"""Check the publishing path, including a newly authored Markdown page."""

import re
import shutil
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

from PIL import Image

import site_builder


class PageReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for key in ("href", "src"):
            if key in attributes:
                self.references.append((tag, attributes[key]))


class SiteBuildTest(unittest.TestCase):
    def test_existing_routes_and_new_article(self):
        with tempfile.TemporaryDirectory(prefix="site-build-test-") as directory:
            root = Path(directory)
            content = root / "content"
            shutil.copytree(site_builder.CONTENT, content)
            article = content / "blogs" / "new_interactive_post"
            article.mkdir()
            Image.new("RGB", (100, 50), "#336699").save(article / "new.png")
            (article / "index.md").write_text(
                '+++\ntitle = "New interactive post"\ndate = 2026-10-07\n'
                'category = "work"\n'
                '[taxonomies]\ntags = ["new-tag"]\n+++\n\n'
                'A new article with an image.\n\n'
                '{{ resize_image(path="blogs/new_interactive_post/new.png", '
                'width=64, height=64, op="fit_width") }}\n',
                encoding="utf-8",
            )
            previous = site_builder.CONTENT
            try:
                site_builder.CONTENT = content
                site_builder.Builder(root / "public").build()
            finally:
                site_builder.CONTENT = previous

            output = root / "public"
            for route in (
                "index.html", "about/index.html", "about/2024/index.html",
                "work/index.html", "resume/index.html",
                "interests/index.html", "blogs/index.html",
                "blogs/page/2/index.html", "blogs/blog-tutorial/index.html",
                "blogs/chord-functions/index.html",
                "blogs/new-interactive-post/index.html", "tags/music/index.html",
                "tags/new-tag/index.html", "atom.xml", "sitemap.xml",
            ):
                self.assertTrue((output / route).is_file(), route)
            blogs_html = (output / "blogs/index.html").read_text()
            self.assertIn("New interactive post", blogs_html)
            self.assertIn('data-tag="new-tag"', blogs_html)
            # Filtering must include older articles that were formerly on page 2.
            self.assertIn('href="/blogs/finance/"', blogs_html)
            self.assertIn('href="/blogs/music-resources/"', blogs_html)
            self.assertIn('href="/blogs/"', (output / "blogs/page/2/index.html").read_text())
            work_html = (output / "work/index.html").read_text()
            self.assertIn("Bilibili", work_html)
            self.assertIn("TCL heyAiMe", work_html)
            self.assertIn('href="/blogs/cs-resources/"', work_html)
            self.assertNotIn("New interactive post", work_html)
            self.assertNotIn("resume_sde.png", work_html)
            self.assertIn("/work/", (output / "resume/index.html").read_text())
            self.assertIn("/work/", (output / "blogs/blog-tutorial/index.html").read_text())
            self.assertIn("/about/", (output / "about/2024/index.html").read_text())
            self.assertFalse((output / "resume/resume_sde.png").exists())
            self.assertFalse((output / "about/.DS_Store").exists())
            self.assertFalse((output / "search_index.en.js").exists())
            about_html = (output / "about/index.html").read_text()
            self.assertNotIn("graduate student", about_html)
            self.assertIn("Shanghai", about_html)
            self.assertIn("machine learning engineer", about_html)
            self.assertNotIn('href="/blogs/cs-resources/"', about_html)
            self.assertNotIn("Markdown (Emoji)", about_html)
            interests_html = (output / "interests/index.html").read_text()
            self.assertIn('href="/blogs/music-resources/"', interests_html)
            interest_images = re.findall(r'<img src="(/processed_images/[^"]+)"', interests_html)
            self.assertEqual(len(interest_images), 4)
            for src in interest_images:
                self.assertTrue((output / src.lstrip("/")).is_file(), src)
            jz_club_image = next(src for src in interest_images if "/jz-club." in src)
            with Image.open(output / jz_club_image.lstrip("/")) as image:
                self.assertGreater(image.height, image.width)
            self.assertNotIn("New interactive post", interests_html)
            self.assertIn('href="/blogs/new-interactive-post/"', (output / "blogs/index.html").read_text())
            self.assertIn('href="/blogs/chord-functions/"', (output / "tags/music/index.html").read_text())
            self.assertIn('href="/blogs/ffmpeg/"', (output / "blogs/cs-resources/index.html").read_text())
            self.assertIn("New interactive post", (output / "atom.xml").read_text())
            article_html = (output / "blogs/new-interactive-post/index.html").read_text()
            image_url = re.search(r'<img src="(/processed_images/[^"]+)"', article_html).group(1)
            with Image.open(output / image_url.lstrip("/")) as image:
                self.assertEqual(image.size, (64, 32))

            for html_file in output.rglob("*.html"):
                parser = PageReferences()
                parser.feed(html_file.read_text(encoding="utf-8"))
                route = "/" + str(html_file.relative_to(output)).replace("index.html", "")
                for tag, reference in parser.references:
                    if tag == "a":
                        self.assertFalse(reference.startswith(site_builder.BASE_URL), reference)
                    if not reference or reference.startswith(("#", "mailto:", "javascript:")):
                        continue
                    url = urlsplit(urljoin("https://preview.local" + route, reference))
                    if url.netloc != "preview.local":
                        continue
                    target = output / unquote(url.path).lstrip("/")
                    if target.is_dir():
                        target /= "index.html"
                    self.assertTrue(target.is_file(), f"{html_file}: {reference}")


if __name__ == "__main__":
    unittest.main()
