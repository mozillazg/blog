"""Settings for pelican."""

AUTHOR = 'mozillazg'
SITENAME = u"Mozillazg's Blog"
SITEURL = 'http://mozillazg.github.com'
SITEDESCRIPTION = u'Just another Pelican blog'


# This can also be the absolute path to a theme that you downloaded
# i.e. './themes/anothertheme/'
# THEME = 'notmyidea'
#THEME = './themes/bootstrap/'
THEME = './themes/relapse/'

# The folder ``images`` should be copied into the folder ``static`` when
# generating the output.
STATIC_PATHS = ['images', 'downloads', ]

# See http://pelican.notmyidea.org/en/latest/settings.html#timezone
TIMEZONE = 'UTC'

# Pelican will take the ``Date`` metadata and put the articles into folders
# like ``/posts/2012/02/`` when generating the output.
# ARTICLE_PERMALINK_STRUCTURE = '/%Y/%m/%d/'
ARTICLE_PERMALINK_STRUCTURE = '/%Y/%m/'

# I like to put everything into the category ``Blog``, which also appears on
# the main menu. Tags will not appear on the menu.
#DEFAULT_CATEGORY = 'Blog'
DEFAULT_CATEGORY = 'Uncategorized'

# I like to have ``Archives`` in the main menu.
MENUITEMS = (
    ('Archives', '{0}/archives.html'.format(SITEURL)),
)

DISPLAY_PAGES_ON_MENU = True

WITH_PAGINATION = True
DEFAULT_PAGINATION = 3
REVERSE_ARCHIVE_ORDER = True

# Uncomment what ever you want to use
#GOOGLE_ANALYTICS = 'XX-XXXXXXX-XX'
DISQUS_SITENAME = 'my-github-blog'
GITHUB_URL = 'http://github.com/mozillazg'
#TWITTER_USERNAME = 'username'
GITHUB_POSITION = True

DEFAULT_LANG = u'zh'

LINKS = (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
         ('Python.org', 'http://python.org'),
         ('Jinja2', 'http://jinja.pocoo.org'),
         ('GitHub', 'https://github.com'),
         )

SOCIAL = (('Atom Feed', '{0}/feeds/all.atom.xml'.format(SITEURL)),
          ('Fork me on GitHub', 'https://github.com/mozillazg'),
          )

FILES_TO_COPY = (('extra/CNAME', 'CNAME'),
                 ('extra/favicon.ico', 'favicon.ico'),
                 )

USE_FOLDER_AS_CATEGORY = True
