# Guochenmeinian's Blog

This personal site keeps the original Anemone appearance. The navigation has
three sections: About, Work, and Interests. Technical articles appear under
Work; music, finance, fitness, and other personal writing appear under
Interests. Existing article URLs under `/blogs/` remain available.

A small Python script builds the static HTML, tags, pagination, resized images,
search index, sitemap, and Atom feed. Node.js builds the elasticlunr index.
GitHub Actions publishes the output to the existing `gh-pages` branch.

## Local development

```sh
python3 -m pip install -r requirements.txt
python3 site_builder.py
python3 -m http.server 8000 --directory public
```

Python 3.12 and Node.js 20 are used in the publishing workflow.

Open `http://localhost:8000`. The input content is in `content/`, the rendered
page templates are in `site_templates/`, and the original CSS is in
`static/css/style.css`. The theme license is retained in `ANEMONE-LICENSE.txt`.
Publishing happens automatically when `main` is pushed.

New articles can go in `content/work/` or `content/interests/` and will be
listed in the matching section. Existing articles remain in `content/blogs/`
to keep their URLs; each has a `category = "work"` or
`category = "interests"` front matter field. The `/blogs/` archive and tags
remain available for old links, but are not in the main navigation. The older
Zola tutorial in `content/blogs/blog_tutorial.md` describes the former setup.
