Title: How to add new content to this technical wiki
Date: 2018-04-19 13:56
Category: internal
Slug: how-to-add-new-content-to-this-technical-wiki
Authors: Qiang Chen

> Update on 2018-06-07. Steps greatly simplified:

1. Clone the git repo of tech wiki. Update content. Push to remote.
2. SSH to server. Run `bash update_wiki.sh` in the home folder (default folder
   when you login).


-------------------------------------------------------------------------------

## 1. Prepare content in Markdown format

To add new content to this technical wiki, you have two options of preparing
the content: markdown and jupyter notebook.

### 1.1 Markdown format

For this option, you need to prepare the article in markdown format, which
looks like this:

~~~markdown
Title: Title of article
Date: 2018-04-19 14:04
Category: DAL-templates
Slug: usually-copy-the-title-of-article-separted-by-dash
Authors: Your Name

This is the content in markdown format.
~~~

Name the markdown file as something like `20180101-title-of-article.md`.

If you need to insert figures into the article, the grammar is like:

~~~markdown
The following shows a figure:

![text]({filename}/static/<figure_name.jpg>)
~~~

Change the figure name and put the figure file to the static folder inside the
content folder.

*For the syntax of markdown file, please refer to [this guide](https://help.github.com/articles/about-writing-and-formatting-on-github/). It should take less than 15 minutes to learn the basics.*

### 1.2 Jupyter notebook format

If you're publishing a Jupyter notebook, first write the notebook, then copy
the notebook to ipynbs folder inside the content folder.

You also need to prepare another markdown file, which looks like this:

~~~markdown
Title: Title of article
Date: 2018-04-19 16:10
Category: DAL-templates
Slug: title-of-article
Authors: Qiang Chen

*Click [this]({filename}/ipynbs/name-of-jupyter-notebook.ipynb) to download the original Jupyter notebook file.*

{% notebook ipynbs/name-of-jupyter-notebook.ipynb %}
~~~


## 2. Publish new content

Use ftp to connect to the wiki server, upload the new content to the content
folder, and other files like ipynb to corresponding folders as well.

Then use putty or other SSH client to connect to the server, go to the wiki
path (parallel to the `content` path), run `pelican content`. Make sure no
warning or error pops up. Then refresh browser to check if the new content is
already online.

![putty]({filename}/static/putty-run-pelican.png){width="600px"}
