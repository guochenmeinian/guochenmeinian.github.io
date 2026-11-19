# guochenmeinian.github.io

Personal site with four sections: About, Work, Interests, and Blogs. It keeps the
original [anemone](https://github.com/Speyll/anemone) look (license in
`ANEMONE-LICENSE.txt`). A small Python script (`site_builder.py`) turns Markdown
into static HTML; GitHub Actions publishes it to `gh-pages` whenever `main` is
pushed.

## Layout

```
content/
  about/index.md        homepage text + Moments photos
  work/_index.md        work page
  interests/_index.md   interests page
  blogs/                articles (each needs category = "work" or "interests")
  about/ work/ interests/   photos live next to the page that uses them
site_templates/         Jinja templates and shortcodes
static/                 CSS, JS, favicon — copied as-is
site_builder.py         the build
dev_server.py           live-reload preview
tests/test_build.py     build + link checks (run in CI before publishing)
```

## Writing pages

About, Work, and Interests are photo-led: their text, links, and photo lists sit
in the `[extra]` front matter of `content/<section>/…md` (rendered by
`site_templates/about.html`, `work.html`, `interests.html`). Edit that file to
change wording or swap photos.

Blog articles are plain Markdown. Images go through shortcodes, which resize them at
build time (originals stay in `content/`):

```
{{ resize_image(path="blogs/x/diagram.png", width=800, height=500, op="fit_width") }}

{{ double_image(path1="work/a.jpg", path2="work/b.jpg", width=650, height=650,
                op="fit_width", format="jpg", resize=True) }}

{{ moments(photos=[
    ["about/view.jpg", "Manhattan"],
    ["about/courant.jpg", "Courant"],
]) }}
```

`moments` shows photos in a masonry grid at their own proportions; clicking one
opens it larger, with previous/next. The homepage strip, the Interests photo rows, and
link popovers (e.g. hovering a school) are driven by `static/js/photos.js`.

## Local development

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python dev_server.py            # http://127.0.0.1:8000/about/
```

Saving anything under `content/`, `site_templates/`, or `static/` rebuilds and
refreshes the browser. To build `public/` and run the CI checks:

```sh
.venv/bin/python site_builder.py
.venv/bin/python -m unittest discover -s tests
```

Old `/resume/`, `/about/2024/`, `/blogs/blog-tutorial/`, and `/blogs/page/N/`
URLs redirect to current pages.
