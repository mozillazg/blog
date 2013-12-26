[python]去掉 unicode 字符串前面的 u
===================================

:date: 2013-12-26
:tags: python, unicode
:slug: python-raw-unicode

有时我们会碰到类似下面这样的 unicode 字符串:

.. code-block:: python

    u'\xe4\xbd\xa0\xe5\xa5\xbd'

这明显不是一个正确的 unicode 字符串，可能是在哪个地方转码转错了。

我们要想得到正确的 unicode 字符串首先就必须先将这个字符串转成非 unicode 字符串，
然后再进行解码。按照普通的办法进行 ``encode`` 肯定是不行的，因为这不是一个正确的 unicode 字符串：

.. code-block:: python

    In [1]: u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('utf8')
    Out[1]: '\xc3\xa4\xc2\xbd\xc2\xa0\xc3\xa5\xc2\xa5\xc2\xbd'

    In [2]: print u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('utf8')
    盲陆聽氓楼陆

那如何才能得到我们想要的 ``\xe4\xbd\xa0\xe5\xa5\xbd`` 呢？

python 提供了一个特殊的编码（ ``raw_unicode_escape`` ）用来处理这种情况：

.. code-block:: python

    In [4]: u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('raw_unicode_escape')
    Out[4]: '\xe4\xbd\xa0\xe5\xa5\xbd'

    In [5]: u'\xe4\xbd\xa0\xe5\xa5\xbd'.encode('raw_unicode_escape').decode('utf8')
    Out[5]: u'\u4f60\u597d'

    In [7]: print u'\u4f60\u597d'
    你好


参考资料
--------

* `7.8. codecs — Codec registry and base classes — Python v2.7.6 documentation <http://docs.python.org/2/library/codecs.html#python-specific-encodings>`__
