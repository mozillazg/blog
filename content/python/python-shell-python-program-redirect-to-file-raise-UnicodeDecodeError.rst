[python]解决将 python 程序输出结果重定向到文件时，出现 UnicodeDecodeError 错误
===============================================================================

:date: 2014-01-19
:tags: python
:slug: python-fix-shell-python-program-redirect-to-file-raise-UnicodeDecodeError

比如：有一个 python 程序 hello.py

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    print u'你好'

将输出结果重定向到文件，就会出现 UnicodeEncodeError:

.. code-block:: console

    $ python hello.py > hello.txt
    Traceback (most recent call last):
      File "hello.py", line 4, in <module>
        print u'你好'
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)

之所以会出现编码错误，是因为：
输出到控制台时，print 使用的是控制台的默认编码，
而重定向到文件时，print 就不知道使用什么编码了，于是就使用了默认编码 ascii 导致出现编码错误。

可以通过设置环境变量 ``PYTHONIOENCODING`` 告诉 python 使用哪种编码:

.. code-block:: console

    $ export PYTHONIOENCODING=utf8
    $ python hello.py  > hello.txt
    $ cat hello.txt
    你好


参考资料
---------

* `Python脚本重定向其输出时的编码问题 - 巴蛮子 - 博客园 <http://www.cnblogs.com/bamanzi/archive/2012/08/16/python-encoding-when-redirection.html>`__
* `PrintFails - Python Wiki <https://wiki.python.org/moin/PrintFails>`__
* `python - UnicodeDecodeError when redirecting to file - Stack Overflow <http://stackoverflow.com/questions/4545661/unicodedecodeerror-when-redirecting-to-file>`__
* `unicode - How to set sys.stdout encoding in Python 3? - Stack Overflow <http://stackoverflow.com/questions/4374455/how-to-set-sys-stdout-encoding-in-python-3>`__
