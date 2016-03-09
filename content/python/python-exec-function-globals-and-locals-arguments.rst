[python] exec 函数的 globals 和 locals 参数的用法
====================================================

:slug: python-exec-function-globals-and-locals-arguments
:date: 2016-03-08
:tags: exec, sanbox

我们都知道 ``exec`` 函数可以用来动态执行 python 代码::

    >> exec('foobar = 123')
    >>> foobar
    123

那么大家是否知道 ``exec`` 函数还支持两个可选参数呢(不支持通过关键字去指定参数)？ ::

    exec(object[, globals[, locals]])

``globals`` 参数用来指定执行代码时可以使用的全局变量，
``locals`` 参数用来保存执行代码后生成的局部变量。

``globals`` 默认为 ``globals()``,
``locals`` 默认为 ``locals()``.
所以 ``exec('foobar=[1,2,3]')`` 和 ``exec('foobar.append(2')`` 才能正常执行。

下面将举例说明指定 ``globals`` 和 ``locals`` 时的效果。


globals
---------

``globals`` 是个 ``dict`` 对象，用来指定代码执行时可以使用的全局变量::

    >>> age = 10
    >>> exec('abc = age + 1')
    >>> exec('abc = age + 1', {})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<string>", line 1, in <module>
    NameError: name 'age' is not defined

有一点需要注意的是: 当 ``globals`` 字典不包含 ``__builtins__`` 这个 key 时，
python 会自动加一个指向 `builtins <https://docs.python.org/3/library/builtins.html#module-builtins>`__ 的引用。所以如果要禁止/限制代码使用内置函数的话，
需要同时指定 ``__builtins__`` 这个 key::

    >>> exec('int(1)', {})

    >>> exec('int(1)', {'__builtins__': {}})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<string>", line 1, in <module>
    NameError: name 'int' is not defined


locals
-------

``locals`` 可以是任何 mapping 对象，用来存储代码执行后生成的局部变量::

    >>> local = {}
    >>> exec('''
    ... name = 'Tom'
    ... age = 13
    ... ''', {}, local)

    >>> local
    {'age': 13, 'name': 'Tom'}


参考资料
----------

* `2. Built-in Functions — Python 3.5.1 documentation <https://docs.python.org/3/library/functions.html#exec>`__
