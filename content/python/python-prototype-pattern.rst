Python 设计模式: 原型模式(prototype pattern)
===================================================
:date: 2016-09-06
:slug: python-prototype-pattern
:tags: design pattern, 设计模式

当需要在原有对象的基础上创建一个该对象的副本时，我们就可以使用原型模式。
在 Python 里可以很简单的通过 ``copy.copy`` 或 ``copy.deepcopy`` 函数来实现原型模式。

对于 copy 后需要再做一些处理的，可以给这个对象定义一个 ``clone`` 方法封装一下具体的操作
或者把操作封装到一个函数里。


比如:

.. code-block:: python


    class Book:
        def __init__(self, name, authors, price):
            self.name = name
            self.authors = authors
            self.price = price

        def clone(self, **kwargs):
            book_copy = self.__class__(self.name, self.authors[:], self.price)
            book_copy.__dict__.update(**kwargs)
            return book_copy

    book = Book('hello', ['tom', 'jim'], 10)
    book2 = book.clone(name='world', price=20)
    book3 = copy.deepcopy(book)
    book3.name = 'english'
    book3.price = 10.5



参考资料
-----------
* `《Mastering Python Design Patterns》 <https://book.douban.com/subject/26336439/>`_
* `《Python in Practice》 <https://book.douban.com/subject/24390228/>`_
