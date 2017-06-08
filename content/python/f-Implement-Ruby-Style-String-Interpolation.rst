Python: 实现 Ruby 风格的字符串插值功能
=================================================
:slug: f-Implement-Ruby-Style-String-Interpolation
:date: 2017-02-16

什么是字符串插值功能
---------------------

字符串插值功能是一种定义字符串的方式，可以在字符串中包含变量、表达式，
这些字符串中的变量/表达式会被自动替换为相应的值。


很多语言都支持字符串插值功能。下面我们来看一下 Ruby 和 Python 3.6 中字符串插值功能是什么样的。


Ruby 风格
-----------

Ruby 风格的字符串插值是这样的： ::


    $ irb
    >> a = 2
    => 2
    >> b = 3
    => 3
    >> "#{a}"
    => "2"
    >> "#{a + b}"
    => "5"

Ruby 中是通过 ``"#{var}"`` 来定义的。

Python 3.6+ 风格
------------------

Python 3.6 也增加了对字符串插值功能的支持: ::


    $ python3.6
    >>> a = 2
    >>> b = 3
    >>> f"{a}"
    '2'
    >>> f"{a + b}"
    '5'

Python 3.6 中新引入了一个 ``f`` ,  是通过 ``f"{var}"`` 来定义的。


通过上面的定义以及两个语言的例子，我们可以知道：
字符串插值就是自动使用当前上下文的变量来求取字符串中特殊标志位中变量或表达式的值,
同时用求得的值替换掉这个标志位 。


所以实现这个功能有三个要点：

* 定义语法
* 获取上下文的变量
* 把字符串当作 python 代码执行并求值

语法
------

我们的字符串插值的语法如下: ::

    f('#{var}')

通过一个 ``f`` 函数来实现字符串插值功能，通过正则来解析变量: ::

    re_code = re.compile(r'#\{([^\}]+)\}')


获取上下文的变量的值
-----------------------

可以通过 ``locals()`` 或者当前上下文变量的值，如果要获取调用方的上下文变量的值
可以使用 frame.

``frame = sys._getframe()`` 可以获取当前 frame, ``frame.f_locals`` 可以获取该 frame
所在上下文的局部变量的值， ``frame.f_globals`` 可以获取该 frame 所在上下文的全局变量的值。
而 ``frame = sys._getframe(1)`` 则可以获取调用方所在  frame: ::

    $ cat f.py
    import sys


    def test():
        frame = sys._getframe(1)
        print('locals: ', frame.f_locals)
        print('globals: ', frame.f_globals)


    a = 1
    test()

    $ python f.py
    locals:  {'__name__': '__main__', ..., 'test': <function test at 0x100f1ee18>, 'a': 1}
    globals:  {'__name__': '__main__', ..., 'test': <function test at 0x100f1ee18>, 'a': 1}

在上面的例子中我们可以看到，可以在 ``test`` 函数中获取调用方所在上下文的变量 ``a`` 的值。


把字符串当作 python 代码执行并求值
-------------------------------------

这个可以通过 ``eval`` 函数来实现这个功能: ::

    eval(source, globals=None, locals=None, /)
        Evaluate the given source in the context of globals and locals.

        The source may be a string representing a Python expression
        or a code object as returned by compile().
        The globals must be a dictionary and locals can be any mapping,
        defaulting to the current globals and locals.
        If only globals is given, locals defaults to it.

    >>> eval('1 + 1')
    2
    >>> a = 2
    >>> eval('a')
    2
    >>> eval('a + 1')
    3
    >>> eval('b', {'b': 2})
    2



实现 f 函数
-------------

下面的代码是一种 ``f`` 函数的实现方法 :

.. code:: python

    $ cat f.py
    # -*- coding: utf-8 -*-
    import re
    import sys

    re_code = re.compile(r'#\{([^\}]+)\}')


    def f(text):
        """实现字符串插值功能"""
        frame = sys._getframe(1)
        chucks = get_chucks(text)
        values = eval_chucks(chucks, frame.f_globals, frame.f_locals)
        return ''.join(values)


    def eval_chucks(chucks, f_globals, f_locals):
        """字符串插值求值"""
        for string, code in chucks:
            yield str(string)

            if code:
                eval_ret = eval(code, f_globals, f_locals)
                yield str(eval_ret)


    def get_chucks(text):
        """按插值语法处理字符串

        get_chucks('aa #{a} bb') -> [('aa ', '#{a}'), (' bb', '')]
        """
        matchs = re_code.finditer(text)
        pos = 0
        for match in matchs:
            yield text[pos:match.start()], match.group(1)
            pos = match.end()
        yield text[pos:], ''


效果 ::

    >>> from f import f
    >>> a = 1
    >>> b = 2
    >>> c = '3'
    >>> f('#{ a }')
    '1'
    >>> f('#{ a + b}')
    '3'
    >>> f('#{ c * 2}')
    '33'


参考资料
--------

* `29.1. sys — System-specific parameters and functions — Python 3.6.1 documentation <https://docs.python.org/3.6/library/sys.html#sys._getframe>`_
* `29.12. inspect — Inspect live objects — Python 3.6.1 documentation <https://docs.python.org/3.6/library/inspect.html#types-and-members>`_
* `2. Built-in Functions — Python 3.6.1 documentation <https://docs.python.org/3.6/library/functions.html#eval>`_
* `github.com/mozillazg/f <https://github.com/mozillazg/f>`_
