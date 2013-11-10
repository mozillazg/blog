[python] 修复读取 utf-8 BOM 编码的配置文件时出现的 ConfigParser.MissingSectionHeaderError: File contains no section headers 错误
================================================================================================================================

:date: 2013-11-10
:tags: python, unicode
:slug: python-utf8-bom-MissingSectionHeaderError

当使用 ConfigParser 读取 utf-8 BOM 编码的配置文件时,会出现如下类似错误：

.. code-block:: python

    ConfigParser.MissingSectionHeaderError: File contains no section headers.
    File: settings.ini, line: 1
    '\xef\xbb\xbf[General]\n'

解决办法就是先将文件内容读出来，然后转码，然后再读取转码后的配置信息：

.. code-block:: python

    import ConfigParser
    from StringIO import StringIO

    conf = ConfigParser.RawConfigParser()
    with open('settings.ini', 'rb') as f:
        content = f.read().decode('utf-8-sig').encode('utf8')
        conf.readfp(StringIO(content))

参考
----

* `Issue 7519: ConfigParser can't read files with BOM markers - Python tracker <http://bugs.python.org/issue7519>`__
* `13.2. ConfigParser — Configuration file parser — Python v2.7.5 documentation <http://docs.python.org/2/library/configparser.html`__
