在 python 中使用 exec 函数时需要注意的一些安全问题
===================================================================

:date: 2016-05-18
:slug: python-some-security-problems-about-use-exec-function.rst
:tags: 安全, exec

众所周知，在 python 中可以使用 ``exec`` 函数来执行包含 python 源代码的字符串:

.. code-block:: python

    >>> code = '''
       ...: a = "hello"
       ...: print(a)
       ...: '''
    >>> exec(code)
    hello
    >>> a
    'hello'

``exec`` 函数的这个功能很是强大，慎用。如果一定要用的话，那么就需要注意一下下面这些安全相关的问题。


全局变量和内置函数
------------------------

在 ``exec`` 执行的代码中，默认可以访问执行 ``exec`` 时的局部变量和全局变量，
同样也会修改全局变量。如果 exec 执行的代码是根据用户提交的数据生产的话，这种默认行为就是一个安全隐患。

如何更改这种默认行为呢？可以通过执行 ``exec`` 函数的时候再传两个参数的方式来
修改这种行为（详见 `之前`_  关于 exec 的文章）:

.. code-block:: python

    >>> g = {}
    >>> l = {'b': 'world'}
    >>> exec('hello = "hello" + b', g, l)
    >>> l
    {'b': 'world', 'hello': 'helloworld'}
    >>> g
    {'__builtins__': {...}}
    >>> hello
    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)
    ...
    NameError: name 'hello' is not defined

如果要限制使用内置函数的话，可以在 globals 参数中定义一下 ``__builtins__`` 这个 key:

.. code-block:: python

    >>> g = {}
    >>> l = {}
    >>> exec('a = int("1")', g, l)
    >>> l
    {'a': 1}

    >>> g = {'__builtins__': {}}
    >>> exec('a = int("1")', g, l)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<string>", line 1, in <module>
    NameError: name 'int' is not defined
    >>>


现在我们限制了访问和修改全局变量以及使用内置函数，难道这样就万事大吉了吗？
然而并非如此，还是可以通过其他的方式来获取内置函数甚至 ``os.system`` 函数。


另辟蹊径获取内置函数和 os.system
------------------------------------

通过函数对象:

.. code-block:: python

    >>> def a(): pass
    ...
    >>> a.__globals__['__builtins__']

    >>> a.__globals__['__builtins__'].open
    <built-in function open>

通过内置类型对象:

.. code-block:: python

    >>> for cls in {}.__class__.__base__.__subclasses__():
    ...     if cls.__name__ == 'WarningMessage':
    ...         b = cls.__init__.__globals__['__builtins__']
    ...         b['open']
    ...
    <built-in function open>
    >>>

获取 ``os.system``:

.. code-block:: python

    >>> cls = [x for x in [].__class__.__base__.__subclasses__() if x.__name__ == '_wrap_close'][0]
    >>> cls.__init__.__globals__['path'].os
    <module 'os' from '/usr/local/var/pyenv/versions/3.5.1/lib/python3.5/os.py'>
    >>>


对于这两种办法又如何应对呢？ 一种办法就是禁止访问以 ``_`` 开头的属性：

* 如果可以控制 code 的生成，那么就在生成 code 的时候判断
* 如果不能的话，可以通过 ``dis`` 模块分析生成的 code:

.. code-block:: python

    >>> code = "[x for x in [].__class__.__base__.__subclasses__() if x.__name__ == '_wrap_close'][0].__init__.__globals__['path'].os.system('date')"
    >>> exec(code)
    Wed May 18 22:55:05 CST 2016
    >>>
    >>> import dis
    >>> dis.dis(code)
      1           0 LOAD_CONST               0 (<code object <listcomp> at 0x10722c270, file "<dis>", line 1>)
                  3 LOAD_CONST               1 ('<listcomp>')
                  6 MAKE_FUNCTION            0
                  9 BUILD_LIST               0
                 12 LOAD_ATTR                0 (__class__)
                 15 LOAD_ATTR                1 (__base__)
                 18 LOAD_ATTR                2 (__subclasses__)
                 21 CALL_FUNCTION            0 (0 positional, 0 keyword pair)
                 24 GET_ITER
                 25 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
                 28 LOAD_CONST               2 (0)
                 31 BINARY_SUBSCR
                 32 LOAD_ATTR                3 (__init__)
                 35 LOAD_ATTR                4 (__globals__)
                 38 LOAD_CONST               3 ('path')
                 41 BINARY_SUBSCR
                 42 LOAD_ATTR                5 (os)
                 45 LOAD_ATTR                6 (system)
                 48 LOAD_CONST               4 ('date')
                 51 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
                 54 RETURN_VALUE
    >>>

从上面可以看出来，获取属性的操作是 ``LOAD_ATTR`` 操作。我们只需要检查 ``LOAD_ATTR``
的名字有没有以下划线开头就可以了:

.. code-block:: python

    >>> class Writer:
    ...     def __init__(self):
    ...         self.text = ''
    ...     def write(self, msg):
    ...         self.text += msg
    ...
    >>> w = Writer()
    >>> dis.dis(code, file=w)
    >>> print(w.text)
      1           0 LOAD_CONST               0 (<code object <listcomp> at 0x1072ce300, file "<dis>", line 1>)
                  3 LOAD_CONST               1 ('<listcomp>')
                  6 MAKE_FUNCTION            0
                  9 BUILD_LIST               0
                 12 LOAD_ATTR                0 (__class__)
                 15 LOAD_ATTR                1 (__base__)
                 18 LOAD_ATTR                2 (__subclasses__)
                 21 CALL_FUNCTION            0 (0 positional, 0 keyword pair)
                 24 GET_ITER
                 25 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
                 28 LOAD_CONST               2 (0)
                 31 BINARY_SUBSCR
                 32 LOAD_ATTR                3 (__init__)
                 35 LOAD_ATTR                4 (__globals__)
                 38 LOAD_CONST               3 ('path')
                 41 BINARY_SUBSCR
                 42 LOAD_ATTR                5 (os)
                 45 LOAD_ATTR                6 (system)
                 48 LOAD_CONST               4 ('date')
                 51 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
                 54 RETURN_VALUE

    >>> re.search(r'\d+\s+LOAD_ATTR\s+\d+\s+\(_[^\)]+\)', w.text)
    <_sre.SRE_Match object; span=(264, 305), match='12 LOAD_ATTR                0 (__class__)'>


我所知道的使用 ``exec`` 函数时需要注意的安全问题就是这些了。
如果你还知道其他需要注意的安全问题的话，欢迎留言告知。


.. _之前: https://mozillazg.com/2016/03/python-exec-function-globals-and-locals-arguments.html
