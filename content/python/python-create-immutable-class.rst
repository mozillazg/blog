[python]如何创建一个不可变的类
===============================

:date: 2014-01-25
:tags: python
:slug: python-create-immutable-class

所谓的不可变的类就是类的实例不可修改。

下面我们先看一下普通的类:

.. code-block:: python

    In [1]: class A(object):
       ...:     pass
       ...:

    In [2]: a = A()

    In [3]: a.abc = 1

    In [4]: a.abc
    Out[4]: 1

普通的类的实例可以在运行时添加新的属性。

那么如何定义一个不可变的类呢？
下面就来看一个不可变类的例子：

.. code-block:: python

    In [8]: class B(object):
      ....:     __slots__ = ['abc']
      ....:     def __init__(self, abc):
      ....:         super(B, self).__setattr__('abc', abc)
      ....:     def __setattr__(self, name, value):
      ....:         raise AttributeError("'%s' has no attribute %s" % (self.__class__, name))
      ....:

    In [9]: b = B(123)

    In [10]: b.abc
    Out[10]: 123

    In [11]: b.abc = 4
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-15-fecd1642a038> in <module>()
    ----> 1 b.abc = 4

    <ipython-input-12-030c2c96393c> in __setattr__(self, name, value)
          4         super(B, self).__setattr__('abc', abc)
          5     def __setattr__(self, name, value):
    ----> 6         raise AttributeError("'%s' has no attribute %s" % (self.__class__, name))
          7

    AttributeError: '<class '__main__.B'>' has no attribute abc

    In [12]: b.__dict__
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-18-25106575ab93> in <module>()
    ----> 1 b.__dict__

    AttributeError: 'B' object has no attribute '__dict__'

    In [13]: b.x = 1
    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)
    <ipython-input-20-0205c051c209> in <module>()
    ----> 1 b.x = 1

    <ipython-input-12-030c2c96393c> in __setattr__(self, name, value)
          4         super(B, self).__setattr__('abc', abc)
          5     def __setattr__(self, name, value):
    ----> 6         raise AttributeError("'%s' has no attribute %s" % (self.__class__, name))
          7

    AttributeError: '<class '__main__.B'>' has no attribute x

这里有两个要点：一个是 ``__slots__`` 另一个是 ``__setattr__`` 。

通过定义 ``__slots__`` 替换掉了类的实例的 ``__dict__`` 属性，阻止新增属性。
通过覆盖 ``__setattr__`` 方法，阻止修改现有属性的值。


参考资料
---------

* `How to Create “Immutable” Classes in Python « The Mouse Vs. The Python <http://www.blog.pythonlibrary.org/2014/01/17/how-to-create-immutable-classes-in-python/>`__
* `Python __slots__ - Stack Overflow <http://stackoverflow.com/questions/472000/python-slots>`__
* `Python: What the Hell is a Slot? by Elf Sternberg <http://www.elfsternberg.com/2009/07/06/python-what-the-hell-is-a-slot/>`__
* `3. Data model — Python v2.7.6 documentation <http://docs.python.org/2/reference/datamodel.html?highlight=__slots__#slots>`__
