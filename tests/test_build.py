"""Check the publishing path, including a newly authored Markdown page."""

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image

import site_builder


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
                "index.html", "about/index.html", "work/index.html",
                "interests/index.html", "blogs/index.html",
                "blogs/page/2/index.html", "blogs/chord-functions/index.html",
                "blogs/new-interactive-post/index.html", "tags/music/index.html",
                "tags/new-tag/index.html", "atom.xml", "sitemap.xml",
                "search_index.en.js",
            ):
                self.assertTrue((output / route).is_file(), route)
            self.assertIn("New interactive post", (output / "blogs/index.html").read_text())
            self.assertIn("New interactive post", (output / "work/index.html").read_text())
            self.assertNotIn("New interactive post", (output / "interests/index.html").read_text())
            self.assertIn("New interactive post", (output / "atom.xml").read_text())
            article_html = (output / "blogs/new-interactive-post/index.html").read_text()
            image_url = re.search(r'<img src="(/processed_images/[^"]+)"', article_html).group(1)
            with Image.open(output / image_url.lstrip("/")) as image:
                self.assertEqual(image.size, (64, 32))
            search = (output / "search_index.en.js").read_text().split("=", 1)[1].strip().rstrip(";")
            self.assertIn(site_builder.BASE_URL + "/blogs/new-interactive-post/",
                          json.loads(search)["documentStore"]["docs"])


if __name__ == "__main__":
    unittest.main()
