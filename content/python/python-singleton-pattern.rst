Python 设计模式: 单例模式(singleton pattern)
===================================================
:date: 2016-09-07
:slug: python-singleton-pattern
:tags: design pattern, 设计模式

如果想在整个程序的运行过程中，某个类只有一个实例的话，可以通过单例模式来实现。


在 Python 中实现单例模式有很多种方式，可以通过传统的在定义类的时候判断,
也可以通过模块级别的变量来实现，也可以通过装饰器实现等等, 有很多种方法可以实现。
但是基本上这些方法都可以破解 ;)


比如:

.. code-block:: python

    # 存储在类属性中，通过类方法去获取
    class Singleton:
        __instance = None

        @classmethod
        def instance(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = cls(*args, **kwargs)
            return cls.__instance



    # 在类的 __new__ 方法中判断
    class Singleton:
        __instance = None
        def __new__(cls, *args, **kwargs):
            if Singleton.__instance is None:
                Singleton.__instance = object.__new__(cls, *args, **kwargs)
            return Singleton.__instance

    s1 = Singleton()
    s2 = Singleton()
    assert id(s2) == id(s1)

    # 依附在一个可变对象上
    def Singleton(*args, **kwargs):
        if Singleton.__instance is not None:
            return Singleton.__instance

        class _Singleton:
            def __init__(self):
                pass

        Singleton.__instance = _Singleton(*args, **kwargs)
        return Singleton.__instance
    Singleton.__instance = None

    s1 = Singleton()
    s2 = Singleton()
    assert id(s1) == id(s2)

    # 闭包
    class _Singleton:
        def __call__(self):
            return self
    Singleton = _Singleton()
    del _Singleton

    s1 = Singleton()
    s2 = Singleton()
    assert id(s1) == id(s2)


更多单例模式的实现详见: `The Singleton Pattern implemented with Python « Python recipes « ActiveState Code <http://code.activestate.com/recipes/52558-the-singleton-pattern-implemented-with-python/>`_



参考资料
-----------
* `《Python in Practice》 <https://book.douban.com/subject/24390228/>`_
* `The Singleton Pattern implemented with Python « Python recipes « ActiveState Code <http://code.activestate.com/recipes/52558-the-singleton-pattern-implemented-with-python/>`_
* `SingletonProgramming - Python Wiki <https://wiki.python.org/moin/SingletonProgramming>`_
