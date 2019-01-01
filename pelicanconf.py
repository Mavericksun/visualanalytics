#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Advanced Analytics Team'
SITENAME = 'UTC Data Analytics Library (DAL)'
SITEURL = ''

#custom settings  -------------------------------------------------------------
THEME = 'pelican-themes/bootstrap2'
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    'render_math',
    'ipynb.liquid',
    # 'encrypt_content'
]
MARKUP = ('md', )
STATIC_PATHS = ['ipynbs', 'static']
IGNORE_FILES = ['.ipynb_checkpoints']
ENCRYPT_CONTENT = {
    'title_prefix': '[Encrypted]',
    'summary': 'This content is encrypted.'
}
DISPLAY_PAGES_ON_MENU = False
#custom settings  -------------------------------------------------------------

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'English'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('UTCDAL GitLab', 'http://172.28.203.93/DBI-DAL/UTCDAL/'),
         ('UTRC', 'http://www.utrc.utc.com/'),
         ('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
