# Guochenmeinian's Blog

This personal site keeps the original Anemone appearance. The navigation has
three sections: About, Work, and Interests. Technical articles appear under
Work; music, finance, fitness, and other personal writing appear under
Interests. Existing article URLs under `/blogs/` remain available.

A small Python script builds the static HTML, tags, pagination, resized images,
sitemap, and Atom feed.
GitHub Actions publishes the output to the existing `gh-pages` branch.

## Local development

From the repository directory, create a Python environment and build the site:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python site_builder.py
python -m http.server 8000 --directory public
```

Open `http://localhost:8000/work/`. Leave the server running. After editing
Markdown, templates, or CSS, activate `.venv` in a second terminal, run
`python site_builder.py`, and refresh the browser. To check the build before pushing, run
`python -m unittest discover -s tests`.

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
or `category = "interests"` front matter field. The `/blogs/` archive and tags
remain available for old links, but are not in the main navigation. Site links
use local paths so they work in both local preview and the published site.
