[python]如何生成一个 Unicode 编码的文件
========================================

:date: 2014-03-03
:tags: python
:slug: python-save-an-Unicode-encoding-file

平时我们用记事本保存文件时，可以看到文件编码可以选择 Unicode 编码。
那么如何用 python 生成一个 Unicode 编码的文件呢？

只需知道 python 中哪个编码代表 Unicode 编码，我们就可以生成一个 Unicode 编码的文件：

+-----------+------------+-----------------------------+------------------------+
|Codec      |  Aliases   | Languages                   | Note                   |
+-----------+------------+-----------------------------+------------------------+
| utf_16    | U16, utf16 | all languages               | Unicode(UTF-16 LE BOM)            |
+-----------+------------+-----------------------------+------------------------+
|utf_16_be  | UTF-16BE   | all languages (BMP only)    | Unicode(UTF-16 BE)     |
+-----------+------------+-----------------------------+------------------------+
|utf_16_le  | UTF-16LE   | all languages (BMP only)    | Unicode(UTF-16 LE)     |
+-----------+------------+-----------------------------+------------------------+

上面表格中，LE 是 Little Endian 的缩写, BE 是 Big Endian 的缩写。

示例：

.. code-block:: python

    import codecs

    with codecs.open('a.txt', 'w', encoding='utf_16') as f:
        f.write(u'a')


参考资料
---------

* `how to read a file that can be saved as either ansi or unicode in python? <http://stackoverflow.com/questions/8466460/how-to-read-a-file-that-can-be-saved-as-either-ansi-or-unicode-in-python>`__
* `7.8. codecs — Codec registry and base classes — Python v2.7.6 documentation <http://docs.python.org/2/library/codecs.html#standard-encodings>`__
* `Unicode HOWTO — Python v2.7.6 documentation <http://docs.python.org/2/howto/unicode.html#reading-and-writing-unicode-data>`__
