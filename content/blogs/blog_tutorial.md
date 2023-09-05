+++
title = "blog tutorial"
date = 2023-09-01
[taxonomies]
tags = ['computer science']
+++


👋 Hello

**This is the tutorial for making this blog website** 🌱 2023.9.1 

Zola is a static site generator (SSG), similar to Hugo, Pelican, and Jekyll (for a comprehensive list of SSGs, please see Jamstack). It is written in Rust and uses the Tera template engine, which is similar to Jinja2, Django templates, Liquid, and Twig.


### Install Zola
Zola provides pre-built binaries for MacOS, Linux and Windows on the [GitHub release page](https://github.com/getzola/zola/releases). \
Find the installation methods for your machine in the official [website](https://www.getzola.org/documentation/getting-started/installation/).


### Zola Init

To initialize a new Zola project called blog:
```$ zola init blog```

During the initialization process, you can go with all the default options. Any modifications needed can be made in the configuration file later.

The directory structure after initialization looks like:
```
.
├── config.toml       # Zola configuration file
├── content           # Place to store Markdown files
├── sass              # CSS extension
├── static            # Global static resources
├── templates         # Template files
└── theme             # Zola themes
```

Now, you can run:
```zola serve```
And view Zola's default welcome page at http://127.0.0.1:1111.


### Zola Themes
Choose your desired theme for your personal blog from Zola Themes. This guide (my blog) uses the "anemone" theme.
To add the theme repository to your local project using the git submodule command:
```git submodule add https://github.com/Speyll/anemone themes/anemone```

Then, enable the theme in your config.toml file:
```theme = "anemone"```

This theme also requires the following configurations:
```
taxonomies = [
    # You can enable/disable RSS
    {name = "tags", feed = true}
]
```

By default, this theme doesn't paginate. If you wish to use pagination, enable it in content/_index.md:
```
+++
paginate_by = 5
sort_by = "date"
+++
```

Finally, set the top menu paths in config.toml:
```
# Customize the header navigation links with the following code in the extra section of config.toml:
[[extra.header_nav]]
en = { name = "/about/", url = "/about" }

[[extra.header_nav]]
en = { name = "/blogs", url = "/blogs" }

[[extra.header_nav]]
en = { name = "/tags/", url = "/tags" }
```

If all the above steps go smoothly, you should be able to see the main page with the newly applied theme!



## References

- [Zola Overview](https://www.getzola.org/documentation/getting-started/overview/)
- [Zola Installation](https://www.getzola.org/documentation/getting-started/installation/)
- [Even Theme Blog for Zola](https://snowfall99.github.io/zola/)
  
