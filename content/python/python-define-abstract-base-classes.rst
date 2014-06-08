[python] 定义抽象基类(Abstract Base Classes)
==============================================

:date: 2014-06-07
:tag: python, abc, NotImplementedError
:slug: python-define-abstract-base-classes

抽象基类一般用于规定子类必须重新定义某些方法。比如 web 框架中的 cache 部分的基类一般类似下面这样:

.. code-block:: python

    class BaseCache(object):
        def get(self, key):
            raise NotImplementedError('subclasses of BaseCache must provide a get() method')
        
        def set(self, key, value, timeout=60):
            raise NotImplementedError('subclasses of BaseCache must provide a set() method')


    class MemcachedCache(BaseCache):
        def get(self, key):
            value = self._cache.get(key)
            return value
        
        def set(self, key, value, timeout=60):
            self._cache.set(key, value, timeout)


在插件、cache、session 等支持功能扩展的系统中，常用抽象基类来统一接口。

.. 

    Why use Abstract Base Classes?

    Abstract base classes are a form of interface checking more strict than individual hasattr() checks for particular methods. By defining an abstract base class, you can define a common API for a set of subclasses. This capability is especially useful in situations where a third-party is going to provide implementations, such as with plugins to an application, but can also aid you when working on a large team or with a large code-base where keeping all classes in your head at the same time is difficult or not possible.


下面介绍三种定义抽象基类的方法。

使用 assert 语句
+++++++++++++++++

.. code-block:: python

    class BaseClass(object):
        def action(self, foobar):
            assert False, 'subclasses of BaseClass must provide an action() method'

    In [6]: BaseClass().action('a')
    ---------------------------------------------------------------------------
    AssertionError                            Traceback (most recent call last)
    <ipython-input-6-69f195c0ee1f> in <module>()
    ----> 1 BaseClass().action('a')

    <ipython-input-3-25c84a2cb72e> in action(self, foobar)
          1 class BaseClass(object):
          2     def action(self, foobar):
    ----> 3         assert False, 'subclasses of BaseClass must provide an action() method'

    AssertionError: subclasses of BaseClass must provide an action() method


使用 NotImplementedError 异常
++++++++++++++++++++++++++++++

.. code-block:: python

    class BaseClass(object):
        def action(self, foobar):
            raise NotImplementedError('subclasses of BaseClass must provide an action() method')

    In [8]: BaseClass().action('a')
    ---------------------------------------------------------------------------
    NotImplementedError                       Traceback (most recent call last)
    <ipython-input-8-69f195c0ee1f> in <module>()
    ----> 1 BaseClass().action('a')

    <ipython-input-7-81782a1e8377> in action(self, foobar)
          1 class BaseClass(object):
          2     def action(self, foobar):
    ----> 3         raise NotImplementedError('subclasses of BaseClass must provide an action() method')

    NotImplementedError: subclasses of BaseClass must provide an action() method


使用 abc 模块
++++++++++++++

python 2.6, 2.7:

.. code-block:: python

    from abc import ABCMeta, abstractmethod
    
    class BaseClass(object):
        __metaclass__ = ABCMeta
        
        @abstractmethod
        def action(self, foobar):
            pass

    In [11]: BaseClass().action('a')
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)
    <ipython-input-11-69f195c0ee1f> in <module>()
    ----> 1 BaseClass().action('a')

    TypeError: Can't instantiate abstract class BaseClass with abstract methods action


python 3.x:

.. code-block:: python

    from abc import ABCMeta, abstractmethod
    
    class BaseClass(metaclass=ABCMeta):
        @abstractmethod
        def action(self, foobar):
            pass

推荐使用 ``abc`` 模块，``NotImplementedError`` 也比较常用。


参考资料
---------

* `《Python 学习手册第4版》第 695 ~ 697 页 <http://book.douban.com/subject/6049132/>`__
* `abc – Abstract Base Classes - Python Module of the Week <http://pymotw.com/2/abc/>`__
* `django/django/core/cache/backends at master · django/django · GitHub <https://github.com/django/django/tree/master/django/core/cache/backends>`__
* `27.8. abc — Abstract Base Classes — Python v2.7.7 documentation <https://docs.python.org/2/library/abc.html>`__
* `29.7. abc — Abstract Base Classes — Python 3.4.1 documentation <https://docs.python.org/3/library/abc.html>`__
