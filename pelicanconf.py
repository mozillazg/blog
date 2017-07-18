#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

"""Settings for pelican."""

AUTHOR = 'mozillazg'
SITENAME = u"Huang Huang 的博客"
SITEURL = os.environ.get('BLOG_SITE_URL', 'https://mozillazg.github.io')
SITEDESCRIPTION = u'Just another Pelican blog'

# This can also be the absolute path to a theme that you downloaded
# i.e. './themes/anothertheme/'
THEME = './pelican-bootstrap3/'
# THEME = './pelican-octopress-theme/'

SHOW_ARTICLE_CATEGORY = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = False
# GITHUB_USER = 'mozillazg'
GITHUB_SKIP_FORK = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 5
CC_LICENSE = 'CC-BY-SA'
CC_ATTR_MARKUP = True

MD_EXTENSIONS = (['toc', 'codehilite', 'footnotes', 'tables'])
PLUGIN_PATHS = [
   os.path.abspath('./pelican-plugins'),
]
PLUGINS = [
   # 'sitemap',
   'related_posts',
   # 'extract_toc',
   'headerid',
   # 'series',
]
HEADERID_LINK_CHAR = '¶'

WEBASSETS = True
ABOUT = u'宅（伪）&& Geek（伪）'
SITE_DESCRIPTION = u'Just another Pelican blog'
SITE_KEYWORDS = u'mozillazg, python, golang'

PYGMENTS_STYLE = 'github'
# CUSTOM_CSS = 'static/custom.css'
CUSTOM_CSSES = [
    # 'static/han.min.css',
    # 'static/yue.css',
    'static/custom.css'
]
# The folder ``images`` should be copied into the folder ``static`` when
# generating the output.
# STATIC_PATHS = ['static/images', 'static/downloads', ]
STATIC_PATHS = ['static', ]

# See http://pelican.notmyidea.org/en/latest/settings.html#timezone
TIMEZONE = 'UTC'

# Pelican will take the ``Date`` metadata and put the articles into folders
# like ``/posts/2012/02/`` when generating the output.
# ARTICLE_PERMALINK_STRUCTURE = '/%Y/%m/%d/'
# ARTICLE_PERMALINK_STRUCTURE = '/%Y/%m/'
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_LANG_URL = '{date:%Y}/{date:%m}/{slug}-{lang}.html'
PAGE_URL = '{date:%Y}/{date:%m}/pages/{slug}.html'
PAGE_LANG_URL = '{date:%Y}/{date:%m}/pages/{slug}-{lang}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_LANG_SAVE_AS = '{date:%Y}/{date:%m}/{slug}-{lang}.html'
PAGE_SAVE_AS = '{date:%Y}/{date:%m}/pages/{slug}.html'
PAGE_LANG_SAVE_AS = '{date:%Y}/{date:%m}/pages/{slug}-{lang}.html'

# I like to put everything into the category ``Blog``, which also appears on
# the main menu. Tags will not appear on the menu.
# DEFAULT_CATEGORY = 'Blog'
DEFAULT_CATEGORY = 'Uncategorized'

# I like to have ``Archives`` in the main menu.
MENUITEMS = (
    # ('Home', '/index.html'),
    ('Feed', '{0}/feeds/all.atom.xml'.format(SITEURL)),
    # ('RSS Feed', '{0}/feeds/all.rss.xml'.format(SITEURL)),
    ('About', '/2014/10/pages/about-me.html'),
    # ('Archives', '/archives.html'),
)

DISPLAY_PAGES_ON_MENU = True

WITH_PAGINATION = True
DEFAULT_PAGINATION = 30
REVERSE_ARCHIVE_ORDER = True

# Uncomment what ever you want to use
# GOOGLE_ANALYTICS = 'RbRRsoKca_Yxb_Zy0IRrXLtjKZlefx2qdKbP6Et9NeE'
GOOGLE_ANALYTICS_UNIVERSAL = 'UA-77172981-1'
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'auto'
DISQUS_SITENAME = 'my-github-blog'
TWITTER_USER = 'mozillazg'
# GITHUB_POSITION = True
TWITTER_CARDS = True
USE_OPEN_GRAPH = True
TWITTER_USERNAME = 'mozillazg'

DEFAULT_LANG = u'zh-Hans'

LINKS = (
    ('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
    ('Python.org', 'http://python.org'),
    ('Jinja2', 'http://jinja.pocoo.org'),
    # ('GitHub', 'https://github.com'),
)
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ATOM = None
SOCIAL = (
    # (u'豆瓣', 'http://www.douban.com/people/mozillazg/'),
    ('Fork me on GitHub', 'https://github.com/mozillazg'),
    # ('About Me', 'http://about.me/mozillazg'),
    (u'Comics', 'https://comic.mozillazg.com'),
    ('Atom Feed', '{0}/feeds/all.atom.xml'.format(SITEURL)),
    ('RSS Feed', '{0}/feeds/all.rss.xml'.format(SITEURL)),
)


# FILES_TO_COPY = (
#    ('extra/CNAME', 'CNAME'),
#    ('extra/robots.txt', 'robots.txt'),
#    ('extra/favicon.ico', 'favicon.ico'),
#    ('extra/google37c30fbcbbc5f169.html', 'google37c30fbcbbc5f169.html'),
# )
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/google37c30fbcbbc5f169.html': {
        'path': 'google37c30fbcbbc5f169.html'
    },
}
FAVICON = 'favicon.ico'
USE_FOLDER_AS_CATEGORY = True
DISPLAY_CATEGORIES_ON_MENU = False

SITEMAP = {'format': 'xml', }

SEARCH_BOX = True

# ADDTHIS_PROFILE = 'ra-54f7c39e17a8ec5f'

NOT_ON_HOME_CATEGORIES = [
    "comic",
    "comics",
]
SHOW_DATE_MODIFIED = True
HIDE_SIDEBAR = True
