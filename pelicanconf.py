#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

"""Settings for pelican."""

AUTHOR = 'mozillazg'
SITENAME = u"Mozillazg's Blog"
SITEURL = 'http://mozillazg.com'
SITEDESCRIPTION = u'Just another Pelican blog'

# This can also be the absolute path to a theme that you downloaded
# i.e. './themes/anothertheme/'
THEME = './pelican-octopress-theme'  # 'notmyidea'
# THEME = './pelican-elegant'  # 'notmyidea'
# THEME = './themes/bootstrap/'
# THEME = './themes/bootstrap2/'
# THEME = './themes/tuxlite_tbs/'
# THEME = './themes/relapse/'
# THEME = './themes/syte/'
THEME = './themes/foundation-default-colours/'
THEME = './themes/zurb-F5-basic/'
THEME = './pure-single'
THEME = './pure'
THEME = './pelican-octopress-theme'  # 'notmyidea'
THEME = './themes/tuxlite_tbs/'
THEME = './themes/pelican-simplegrey/'
THEME = './themes/blueidea/'
THEME = './themes/pelican-bootstrap3/'

SHOW_ARTICLE_CATEGORY = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_TAGS_ON_SIDEBAR = False
GITHUB_USER = 'mozillazg'
GITHUB_SKIP_FORK = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 5
CC_LICENSE = 'CC-BY-SA'
CC_ATTR_MARKUP = True

MD_EXTENSIONS = (['toc', 'codehilite', 'footnotes', 'tables'])
PLUGIN_PATH = os.path.abspath('./pelican-plugins')
PLUGINS = [# 'assets',
           # 'gravatar',
           # 'pelican.plugins.github_activity',
           'sitemap',
           'related_posts',
           'extract_toc',
           # 'cjk-auto-spacing',
           # 'pin_to_top',
	   'series',
           ]

WEBASSETS = True
ABOUT = u'宅（伪）&& Geek（伪）'
SITE_DESCRIPTION = u'Just another Pelican blog'
SITE_KEYWORDS = u'python, web.py, django, firefox, vim'
# GITHUB_INTEGRATION_ENABLED = True
# GITHUB_INTEGRATION_ENABLED = False
# GITHUB_USERNAME = 'mozillazg'
# GRAVATAR = u'https://en.gravatar.com/userimage/7906007/7f8709a4ab3a1398b46c628bb193900b.jpg'
# GITHUB_USER = 'mozillazg'
# GITHUB_REPO_COUNT = 0
# GITHUB_SKIP_FORK = True
# GITHUB_SHOW_USER_LINK = True

# GITHUB_ACTIVITY_FEED = 'https://github.com/mozillazg.atom'

PYGMENTS_STYLE = 'solarizedlight'
CUSTOM_CSS = 'static/custom.css'
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
#DEFAULT_CATEGORY = 'Blog'
DEFAULT_CATEGORY = 'Uncategorized'

# I like to have ``Archives`` in the main menu.
MENUITEMS = (
    ('Home', '/index.html'),
    ('Archives', '/archives.html'),
)

DISPLAY_PAGES_ON_MENU = True

WITH_PAGINATION = True
DEFAULT_PAGINATION = 3
REVERSE_ARCHIVE_ORDER = True

# Uncomment what ever you want to use
# GOOGLE_ANALYTICS = 'RbRRsoKca_Yxb_Zy0IRrXLtjKZlefx2qdKbP6Et9NeE'
DISQUS_SITENAME = 'my-github-blog'
# GITHUB_URL = 'https://github.com/mozillazg'
#TWITTER_USERNAME = 'username'
TWITTER_USER = 'mozillazg'
# GITHUB_POSITION = True

DEFAULT_LANG = u'zh'

LINKS = (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
         ('Python.org', 'http://python.org'),
         ('Jinja2', 'http://jinja.pocoo.org'),
         # ('GitHub', 'https://github.com'),
         )
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ATOM = None
SOCIAL = (
           #('Atom Feed', '{0}/feeds/all.atom.xml'.format(SITEURL)),
          (u'豆瓣', 'http://www.douban.com/people/mozillazg/'),
          ('Fork me on GitHub', 'https://github.com/mozillazg'),
          ('About Me', 'http://about.me/mozillazg'),
          ('翻译的漫画', 'http://comic.mozillazg.com'),
          ('Atom Feed', '{0}/feeds/all.atom.xml'.format(SITEURL)),
          ('RSS Feed', '{0}/feeds/all.rss.xml'.format(SITEURL)),
          )

FILES_TO_COPY = (('extra/CNAME', 'CNAME'),
                 ('extra/robots.txt', 'robots.txt'),
                 ('extra/favicon.ico', 'favicon.ico'),
                 ('extra/google37c30fbcbbc5f169.html', 'google37c30fbcbbc5f169.html'),
                 )

USE_FOLDER_AS_CATEGORY = True
DISPLAY_CATEGORIES_ON_MENU = False

SITEMAP = {'format': 'xml', }

SEARCH_BOX = True
# GITHUB_SKIP_FORK = True
# GITHUB_SHOW_USER_LINK = True
# GITHUB_USER = 'mozillazg'
# GITHUB_REPO_COUNT = 0
QR_CODE = True

ADDTHIS_PROFILE = 'ra-54f7c39e17a8ec5f'
