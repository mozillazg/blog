[python] 函数陷阱
==================

:date: 2014-05-28
:tag: python
:slug: python-function-xyz

本文说的这几个问题适用于 ``python 2.6+``  。


UnboundLocalError
------------------

.. code-block:: python

    In [1]: a = 1
    In [2]: def func():
       ...:     print(a)
       ...:     a = 2
       ...:
    In [3]: func()
    ---------------------------------------------------------------------------
    UnboundLocalError                         Traceback (most recent call last)
    <ipython-input-3-08a2da4138f6> in <module>()
    ----> 1 func()
    <ipython-input-2-9e6cf545bc05> in func()
          1 def func():
    ----> 2     print(a)
          3     a = 2
          4
    UnboundLocalError: local variable 'a' referenced before assignment

产生这种问题的原因在于被赋值的变量名在函数内部是被当作局部变量来对待的，而不是仅仅在赋值以后的语句中才被当作是局部变量。

可以使用 global 关键字实现在函数中对全局变量进行重新赋值:

.. code-block:: python

    In [4]: def func():
       ...:     global a
       ...:     print(a)
       ...:     a = 2
       ...:
    In [5]: func()
    1
    In [6]: a
    Out[6]: 2


如果你真的既要调用全局变量，又要定义一个同名的局部变量的话，可以通过下面的方式间接访问全局变量:

.. code-block:: python

    In [7]: b = 10
    In [8]: def funcb():
       ...:     import __main__
       ...:     print(__main__.b)
       ...:     b = 3
       ...:     print(b)
       ...:
    In [9]: funcb()
    10
    3
    In [10]: b
    Out[10]: 10

__main__ 交互模式下的命名空间，可以通过 __main__.a 取得全局变量 a 。
如果是在模块中的话，请将 __main__ 替换为函数所在的模块名称即可。

.. code-block:: python

    # xyz.py
    b = 10
    def funcb():
        import xyz
        print(xyz.b)
        b = 3
        print(b)

    # ipython
    In [11]: import xyz
    In [12]: print xyz.b
    10
    In [13]: xyz.funcb()
    10
    3
    In [14]: xyz.b
    Out[14]: 10


使用可变类型作为默认参数
-------------------------

将可变类型设为函数的默认参数会导致出现背离我们初衷的情况：

.. code-block:: python

    In [1]: def func(a=[]):
       ...:     a.append(1)
       ...:     print(a)
       ...:
    In [2]:
    In [2]: func()
    [1]
    In [3]: func()
    [1, 1]
    In [4]: func()
    [1, 1, 1]

可以看到，上面的代码中，每次调用 func() 的返回值都不一样，这显然不是我们想要的结果。

这是因为默认参数是在 def 语句定义时评估并保存的，而不是在这个函数调用时。
从内部来讲，Python 会将每一个默认参数保存成一个对象，附加在这个函数本身,
如果默认参数是个可变类型的话，该对象会在调用过程中保留状态，而不是每次调用时都重新设定初始值。

修改可变的默认参数就类似于修改函数的一个可变类型的属性。跟下面类似：

.. code-block:: python

    In [5]: def func():
       ...:     func.a.append(1)
       ...:     print(func.a)
       ...:
    In [6]: func.a = []
    In [7]: func()
    [1]
    In [8]: func()
    [1, 1]
    In [9]: func()
    [1, 1, 1]


两种解决办法:

* 不要使用可变类型作为函数默认参数的值（推荐）:

    .. code-block:: python

        In [32]: def func(a=None):
           ....:     if a is None:
           ....:         a = []
           ....:     a.append(1)
           ....:     print(a)
           ....:
        In [33]: func()
        [1]
        In [34]: func()
        [1]
        In [35]: func([1, 2])
        [1, 2, 1]
        In [36]: func()
        [1]

* 在函数内部对默认参数进行简单的拷贝:

    .. code-block:: python

        In [12]: from copy import copy
        In [13]:
        In [13]: def func(a=[]):
           ....:         a = copy(a)
           ....:         a.append(1)
           ....:         print(a)
           ....:
        In [14]: func()
        [1]
        In [15]: func()
        [1]
        In [16]: func([1, 2])
        [1, 2, 1]
        In [17]: func()
        [1]


嵌套作用域的循环变量
--------------------

在进行嵌套函数作用域查找时，**处理在循环中被改变的嵌套变量时要小心，所有的引用都将会使用在最后的循环迭代中对应的值** 。作为替代，请使用默认参数来保存循环变量的值。

.. code-block:: python

    In [43]: def func():
       ....:     a = []
       ....:     for x in range(5):
       ....:         a.append(lambda n: x ** n)
       ....:     return a
       ....:
    In [44]: ab = func()
    In [45]: ab[0]
    Out[45]: <function __main__.<lambda>>
    In [46]: ab[0](3)
    Out[46]: 64
    In [47]: ab[1](3)
    Out[47]: 64
    In [48]: ab[3](3)
    Out[48]: 64

之所以会出现这种情况是因为：嵌套作用域的变量在嵌套的函数被调用时才进行查找，
所以它们实际上记住的是同样的值（在最后一次循环迭代中循环变量的值）。
因此，对于上面的 ab 列表, lambda 中 x 的值永远都是 4。

为了让这类代码能够工作，必须使用默认参数把当前的值传递给嵌套的作用域的变量，因为默认参数使之嵌套函数创建是评估的（而不是在其稍后调用时）。

.. code-block:: python

    In [57]: def func():
       ....:     a = []
       ....:     for x in range(5):
       ....:         a.append(lambda n, x=x: x ** n)
       ....:     return a
       ....:
    In [58]: ab = func()
    In [59]: ab[0]
    Out[59]: <function __main__.<lambda>>
    In [60]: ab[0](3)
    Out[60]: 0
    In [61]: ab[1](3)
    Out[61]: 1
    In [62]: ab[3](3)
    Out[62]: 27


参考
-----

* `《Python 学习手册第4版》第 16 ~ 20 章 <http://book.douban.com/subject/6049132/>`__
