title: python 中 += 运算符在可变对象和不可变对象上的不同效果
slug: python-plus-work-on-immutable-or-mutable-object.md
date: 2016-01-31

先来看内置的不可变对象 `+=` 的结果：

    >>> a = 'b'
    >>> id(a)
    140606482358088
    >>> a += 'c'
    >>> a
    'bc'
    >>> id(a)
    140606244543656

可以看到内置的不可变对象 `+=` 时，会返回一个新的对象。那么内置的可变对象 `+=` 呢？：

    >>> a = [1, 2]
    >>> id(a)
    140606245413384
    >>> a += [3, 4]
    >>> a
    [1, 2, 3, 4]
    >>> id(a)
    140606245413384
    >>> a += (1, 2)
    >>> a
    [1, 2, 3, 4, 1, 2]
    >>> id(a)
    140606245413384


可以看到内置的可变对象的 `+=` 操作实际是原地修改操作，并不是返回一个新的对象。

## 启示

一方面要注意到 `+=`, `-=` 之类的 `x=` 操作在作用于内置的可变对象时是原地修改的情况，
另一方面也给了我们重载 `+=`, `-=` 之类的 `x=` 运算符时的一个参考。

比如自定义的一个可变对象要实现支持 `+=` 运算符:

    class Mutable:

        def __init__(self, number):
            self.number = number

        def __iadd__(self, other):
            """可变对象原地修改，返回 self"""
            self.number += other.number
            return self


    >>> m = Mutable(3)
    >>> id(m)
    140606244895432
    >>> m += Mutable(4)
    >>> m.number
    7
    >>> id(m)
    140606244895432


不可变对象:

    class Immutable:

        def __init__(self, number):
            self._number = number

        @property
        def number(self):
            return self._number

        def __iadd__(self, other):
            """不可变对象，返回一个新的对象"""
            return self.__class__(self._number + other.number)


    >>> im = Immutable(3)
    >>> id(im)
    140606234970432
    >>> im += Immutable(4)
    >>> im.number
    7
    >>> id(im)
    140606245096192

## 参考资料

* [3. Data model &mdash; Python 3.5.1 documentation](https://docs.python.org/3/reference/datamodel.html#object.__radd__)