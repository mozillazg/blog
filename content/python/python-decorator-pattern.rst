Python 设计模式: 装饰器模式(decorator pattern)
==================================================
:date: 2016-08-22
:slug: python-decorator-pattern
:tags: design pattern, 设计模式

装饰器模式说的是在不修改原有对象的基础上，给这个对象增加新的职责/功能。

举个栗子:

.. code-block:: python

    def max_age(*args):
        time.sleep(3)
        return max(args)

    def cache_decorator(func):
        cache = {}
        def _wrapper(*args):
            if args in cache:
                return cache[args]
            cache[args] = result = func(*args)
            return result
        return _wrapper
    cached_max_age = cache_decorator(max_age)
    cached_max_age(1, 2, 3, 0)
    cached_max_age(1, 2, 3, 0)


参考资料
-----------
* `《Mastering Python Design Patterns》 <https://book.douban.com/subject/26336439/>`_
* `DecoratorPattern - Python Wiki <https://wiki.python.org/moin/DecoratorPattern>`_
* `Decorator pattern - Wikipedia, the free encyclopedia <https://en.wikipedia.org/wiki/Decorator_pattern#Python>`_
