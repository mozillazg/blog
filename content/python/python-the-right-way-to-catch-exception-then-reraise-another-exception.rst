Python: 捕获异常然后再抛出另一个异常的正确姿势
==================================================
:slug: python-the-right-way-to-catch-exception-then-reraise-another-exception
:date: 2016-08-16

一般大家实现捕获异常然后再抛出另一个异常的方法是下面这样的:

.. code-block:: python

    def div():
        2 / 0

    try:
        div()
    except ZeroDivisionError as e:
        raise ValueError(e)


不知道大家有没有注意到这样抛出异常的方式有一个很严重的问题，那就是
在重新抛出另一个异常的时候，捕获的上一个异常的 traceback 信息丢失了(python2): ::

    $ cat a.py
    def div():
        2 / 0
    try:
        div()
    except ZeroDivisionError as e:
        raise ValueError(e)

    $ python2 a.py
    Traceback (most recent call last):
      File "a.py", line 6, in <module>
        raise ValueError(e)
    ValueError: integer division or modulo by zero

这样的话非常不利于查找问题: 比如上面的例子中实际出错的代码是第二行，但是
当我们捕获了第一个异常然后再抛出一个自定义异常的时候，
实际出错位置的信息就丢失了。


Python 2
--------------

那么在 Python 2 下如果我们不想丢失捕获的异常的 traceback 信息的话，应该
怎样重新抛出异常呢？


有两种办法, 还是用上面的例子举例:


一种办法是直接 ``raise``: ::

    $ cat a.py
    def div():
        2 / 0
    try:
        div()
    except ZeroDivisionError as e:
        raise

    $ python2 a.py
    Traceback (most recent call last):
      File "a.py", line 4, in <module>
        div()
      File "a.py", line 2, in div
        2 / 0
    ZeroDivisionError: integer division or modulo by zero


另一种办法就是 ``raise`` 另一个异常时指定上一个异常的 traceback 信息
(通过 ``sys.exc_info()`` 获取当前捕获的异常信息): ::

    $ cat a.py
    import sys

    def div():
        2 / 0
    try:
        div()
    except ZeroDivisionError as e:
        raise ValueError(e), None, sys.exc_info()[2]

    $ python2 a.py
    Traceback (most recent call last):
      File "a.py", line 6, in <module>
        div()
      File "a.py", line 4, in div
        2 / 0
    ValueError: integer division or modulo by zero


这个是 ``raise`` 的高级用法:

.. code-block:: python

    raise exception, value, traceback

* ``exception``: 异常类实例/异常类

* ``value``: 初始化异常类的参数值/异常类实例（使用这个实例作为 raise 的异常实例）/元组/None

* ``traceback``: traceback 对象/None

下面我们来看看上面的方法是否可以应对多层异常捕获然后再抛出的情况: ::

    $ cat a.py
    import sys

    def div():
        2 / 0

    def foo():
        try:
            div()
        except ZeroDivisionError as e:
            raise ValueError(e), None, sys.exc_info()[2]

    def bar():
        try:
            foo()
        except ValueError as e:
            raise TypeError(e), None, sys.exc_info()[2]

    def foobar():
        try:
            bar()
        except TypeError as e:
            raise
    foobar()

    $ python2 a.py
    Traceback (most recent call last):
      File "a.py", line 23, in <module>
        foobar()
      File "a.py", line 20, in foobar
        bar()
      File "a.py", line 14, in bar
        foo()
      File "a.py", line 8, in foo
        div()
      File "a.py", line 4, in div
        2 / 0
    TypeError: integer division or modulo by zero

从上面的结果可以看到这两种方法是支持多层异常 traceback 信息传递的。


那么在 Python 3 下又怎么解决这个问题呢？


Python 3
--------------

在 Python 3 下默认会附加上捕获的上个异常的 trackback 信息（保存在异常实例的 ``__traceback__`` 属性中）: ::

    $ cat a.py
    def div():
        2 / 0
    try:
        div()
    except ZeroDivisionError as e:
        raise ValueError(e)

    $ python3 a.py
    Traceback (most recent call last):
      File "a.py", line 4, in <module>
        div()
      File "a.py", line 2, in div
        2 / 0
    ZeroDivisionError: division by zero

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "a.py", line 6, in <module>
        raise ValueError(e)
    ValueError: division by zero

也支持指定使用哪个异常实例的 traceback 信息: ``raise ... from ...`` ::

    $ cat a.py
    def div():
        2 / 0

    try:
        div()
    except ZeroDivisionError as e:
        raise ValueError(e) from e

    $ python a.py
    Traceback (most recent call last):
      File "a.py", line 5, in <module>
        div()
      File "a.py", line 2, in div
        2 / 0
    ZeroDivisionError: division by zero

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
      File "a.py", line 7, in <module>
        raise ValueError(e) from e
    ValueError: division by zero


也可以指定使用的 traceback 对象: ``raise exception.with_traceback(traceback)`` ::

    $ cat a.py
    import sys

    def div():
        2 / 0

    try:
        div()
    except ZeroDivisionError as e:
        raise ValueError(e).with_traceback(sys.exc_info()[2])

    $ python a.py
    Traceback (most recent call last):
      File "a.py", line 7, in <module>
        div()
      File "a.py", line 4, in div
        2 / 0
    ZeroDivisionError: division by zero

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "a.py", line 9, in <module>
        raise ValueError(e).with_traceback(sys.exc_info()[2])
      File "a.py", line 7, in <module>
        div()
      File "a.py", line 4, in div
        2 / 0
    ValueError: division by zero


兼容 Python 2 和 Python 3 的写法
------------------------------------

上面介绍了在 Python 2 和 Python 3 下的不同解决办法，那么如何写一个兼容 Python 2
和 Python 3 的 ``reraise`` 函数呢？

下面将介绍一种方法:

.. code-block:: python

    PY3 = sys.version_info[0] == 3
    if PY3:
        def reraise(tp, value, tb=None):
            if value.__traceback__ is not tb:
                raise value.with_traceback(tb)
            else:
                raise value
    else:
        exec('''def reraise(tp, value, tb=None):
               raise tp, value, tb
        ''')

这里的 ``reraise`` 函数我们约定了 ``vlaue`` 参数的值是一个异常类的实例。
上面 ``else`` 中之所以用 ``exec`` 去定义 ``reraise`` 函数是因为
``raise tp, value, tb`` 在 Python 3 下会报语法错误，所以用 ``exec`` 来
绕过 Python 3 下的语法错误检查。


下面我们来看一下效果: ::

    $ cat a.py

    ef div():
        2 / 0

    def foo():
        try:
            div()
        except ZeroDivisionError as e:
            reraise(ValueError, ValueError(e), sys.exc_info()[2])

    def bar():
        try:
            foo()
        except ValueError as e:
            reraise(TypeError, TypeError(e), sys.exc_info()[2])

    def foobar():
        try:
            bar()
        except TypeError:
            raise
    foobar()

Python 2: ::

    $ python2 a.py
    Traceback (most recent call last):
      File "a.py", line 34, in <module>
        foobar()
      File "a.py", line 31, in foobar
        bar()
      File "a.py", line 27, in bar
        reraise(TypeError, TypeError(e), sys.exc_info()[2])
      File "a.py", line 25, in bar
        foo()
      File "a.py", line 21, in foo
        reraise(ValueError, ValueError(e), sys.exc_info()[2])
      File "a.py", line 19, in foo
        div()
      File "a.py", line 15, in div
        2 / 0
    TypeError: integer division or modulo by zero

Python 3: ::

    $ python3 a.py
    Traceback (most recent call last):
      File "a.py", line 19, in foo
        div()
      File "a.py", line 15, in div
        2 / 0
    ZeroDivisionError: division by zero

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "a.py", line 25, in bar
        foo()
      File "a.py", line 21, in foo
        reraise(ValueError, ValueError(e), sys.exc_info()[2])
      File "a.py", line 6, in reraise
        raise value.with_traceback(tb)
      File "a.py", line 19, in foo
        div()
      File "a.py", line 15, in div
        2 / 0
    ValueError: division by zero

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "a.py", line 34, in <module>
        foobar()
      File "a.py", line 31, in foobar
        bar()
      File "a.py", line 27, in bar
        reraise(TypeError, TypeError(e), sys.exc_info()[2])
      File "a.py", line 6, in reraise
        raise value.with_traceback(tb)
      File "a.py", line 25, in bar
        foo()
      File "a.py", line 21, in foo
        reraise(ValueError, ValueError(e), sys.exc_info()[2])
      File "a.py", line 6, in reraise
        raise value.with_traceback(tb)
      File "a.py", line 19, in foo
        div()
      File "a.py", line 15, in div
        2 / 0
    TypeError: division by zero


下次需要捕获一个异常然后再抛出另一个异常的时候大家可以试试本文的方法。


参考资料
------------

* `6. Simple statements — Python 2.7.12 documentation <https://docs.python.org/2/reference/simple_stmts.html#the-raise-statement>`_
* `6. Built-in Exceptions — Python 2.7.12 documentation <https://docs.python.org/2/library/exceptions.html#exceptions.BaseException>`_
* `7. Simple statements — Python 3.5.2 documentation <https://docs.python.org/3/reference/simple_stmts.html#raise>`_
* `5. Built-in Exceptions — Python 3.5.2 documentation <https://docs.python.org/3/library/exceptions.html#BaseException>`_
* `PEP 3109 -- Raising Exceptions in Python 3000 | Python.org <https://www.python.org/dev/peps/pep-3109/#compatibility-issues>`_
* `bottle/bottle.py at cafc15419cbb4a6cb748e6ecdccf92893bb25ce5 · bottlepy/bottle <https://github.com/bottlepy/bottle/blob/cafc15419cbb4a6cb748e6ecdccf92893bb25ce5/bottle.py#L160>`_
* `flask/_compat.py at 6e46d0cd3969f6c13ff61c95c81a975192232fed · pallets/flask <https://github.com/pallets/flask/blob/6e46d0cd3969f6c13ff61c95c81a975192232fed/flask/_compat.py#L30>`_
