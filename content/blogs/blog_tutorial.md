+++
title = "how to make this blog website"
date = 2023-09-07
[taxonomies]
tags = ['computer science']
+++


👋 Hello

**This is the tutorial for making this blog website**

Zola is a static site generator (SSG), similar to Hugo, Pelican, and Jekyll (for a comprehensive list of SSGs, please see Jamstack). It is written in Rust and uses the Tera template engine, which is similar to Jinja2, Django templates, Liquid, and Twig.


### Install Zola
Zola provides pre-built binaries for MacOS, Linux and Windows on the [GitHub release page](https://github.com/getzola/zola/releases). \
Find the installation methods for your machine in the official [website](https://www.getzola.org/documentation/getting-started/installation/).


### Zola Init

To initialize a new Zola project called blog:
```
$ zola init blog
```

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
```
zola serve
```
And view Zola's default welcome page at http://127.0.0.1:1111.


### Zola Themes
This guide (my blog) uses the "anemone" theme. Feel free to explore the existing [themes](https://www.getzola.org/themes/) available on Zola pick one and tweak it to your style just like I did with mine or you could even imlement your own theme. 

To add the theme repository to your local project using the git submodule command:
```
git submodule add https://github.com/Speyll/anemone themes/anemone
```

Then, enable the theme in your config.toml file:
```
theme = "anemone"
```

This theme also requires the following configurations:
```
taxonomies = [
    # You can enable/disable RSS
    {name = "tags", feed = true}
]
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


### Github
Use github for version control, collaboration, code sharing, and continuous deployment: 

```
git add .              
```
- Stages all modified files for commit.
```
git commit -m "Finalize blog and ready for deployment"   
```
- Commits the staged changes with a provided message.
```
git push origin master  
```
- Pushes the committed changes to your GitHub repository.


### Connect to Netlify:
Once your code is on GitHub:
- Sign in to Netlify.
- Click "New site from Git" > select GitHub.
- Link your GitHub repo containing your Zola project.



### Build Configuration:
Zola requires a specific build command to be executed on Netlify to ensure your site is constructed correctly.
```
wget -q -O - https://github.com/getzola/zola/releases/download/v0.17.2/zola-v0.17.2-x86_64-unknown-linux-gnu.tar.gz | tar xvz -C . && ./zola build --base-url $DEPLOY_URL
```
After setting this command in the "Build command" field on Netlify, it will use it every time you push changes to your GitHub repository, automatically rebuilding and redeploying your site.



### (Optional) 
1. By default, this theme doesn't paginate. If you wish to use pagination, enable it in content/_index.md:
```
+++
paginate_by = 5
sort_by = "date"
+++
```


2. For those curious, below is a breakdown of the build command:
```
wget -q -O - https://github.com/getzola/zola/releases/download/v0.17.2/zola-v0.17.2-x86_64-unknown-linux-gnu.tar.gz 
```
- This command fetches the content of the specified URL. In this context, it's downloading the Zola binary.

```
tar xvz -C . 
```
- This command extracts the downloaded tarball in the current directory.
  
```
./zola build --base-url $DEPLOY_URL
```
- Runs the Zola build command and sets the base URL for the site to the value of the DEPLOY_URL environment variable provided by Netlify.


3. I later deployed this site on Github Pages because that customized domain name costs 70+ dollars after first year trial. Integrating Zola with Github Action is also fairly straightforward. You can check out their blog on how to deploy on Gihub: https://www.getzola.org/documentation/deployment/github-pages/.


## References

- [Zola Overview](https://www.getzola.org/documentation/getting-started/overview/)
- [Zola Installation](https://www.getzola.org/documentation/getting-started/installation/)
- [Even Theme Blog for Zola](https://snowfall99.github.io/zola/)
  
