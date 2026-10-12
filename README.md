# Guochenmeinian's Blog

This personal site keeps the original Anemone appearance. The navigation has
four sections: About, Work, Interests, and Blogs. Work and Interests link to
their respective resources; Blogs collects all articles in reverse chronological
order, with category and tag filters above a compact row list. Filters apply to
the full archive and are saved in the URL. Existing article URLs under `/blogs/`
remain available; former archive pagination links redirect to `/blogs/`.

A small Python script builds the static HTML, tags, resized images,
sitemap, and Atom feed.
GitHub Actions publishes the output to the existing `gh-pages` branch.

## Local development

From the repository directory, create a Python environment once:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start the live preview:

```sh
.venv/bin/python dev_server.py
```

Open `http://localhost:8000/work/` and leave the terminal running. Saving Markdown,
templates, CSS, or images automatically rebuilds the site and refreshes the browser,
usually within 1–2 seconds. A failed build is reported in the terminal; the last
working preview stays available until you fix the source and save again. Restart
the server after editing `dev_server.py` itself. Use `--port 8001` if needed.

The preview uses a temporary output directory. Its refresh script is added only
to local HTTP responses and is never included in the published site. To build
`public/` for deployment and run checks:

```sh
.venv/bin/python site_builder.py
.venv/bin/python -m unittest discover -s tests
```

Python 3.12 is used in the publishing workflow.

The input content is in `content/`, the rendered page templates are in
`site_templates/`, and the original CSS is in
`static/css/style.css`. The theme license is retained in `ANEMONE-LICENSE.txt`.
Publishing happens automatically when `main` is pushed.

`/work/` begins with the experience summary and links to CS resources.
`/interests/` introduces personal interests with four photos and links to Music resources.
Old `/resume/`, `/about/2024/`, and `/blogs/blog-tutorial/` links redirect to
current pages. There is no downloadable resume.

New articles can go in `content/work/` or `content/interests/`; add a link from
the relevant section page when you want them visible there. Existing articles
remain in `content/blogs/` to keep their URLs; each has a `category = "work"`
or `category = "interests"` front matter field. The `/blogs/` archive is in the
main navigation; tags remain available through existing links. Site links
use local paths so they work in both local preview and the published site.
