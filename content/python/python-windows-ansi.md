Title: [python]Windows 下的 ANSI 编码
Date: 2013-09-24
Slug: python-windows-ansi

Windows 下用记事本保存文件时有个 ANSI 编码，那么如何用 python 保存一个 ANSI 编码的文件呢？

python 中使用 `mbcs` 编码（Windows only）表示 ANSI:

    :::python
    with open('hello.txt', 'w') as f:
        f.write(u'你好'.encode('mbcs'))

执行上面的代码，就可以创建一个 ANSI 编码的文件。

> ANSI == Windows 本地编码

在简体中文 Windows 系统中：ansi == gbk :

    :::python
    >>> u'你好'.encode('mbcs')
    '\xc4\xe3\xba\xc3'
    >>> u'你好'.encode('mbcs').decode('gbk')
    u'\u4f60\u597d'


## 参考

* [\[CPyUG\] 请问在python中如何将utf8编码的文件转换成ansi编码](http://comments.gmane.org/gmane.org.user-groups.python.chinese/93052)
* [7.8. codecs — Codec registry and base classes — Python v2.7.5 documentation ](http://docs.python.org/2/library/codecs.html#python-specific-encodings)
