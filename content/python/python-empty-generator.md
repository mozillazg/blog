Title: [python]返回一个空的生成器
Date: 2013-08-15
Tags: python, generator
Slug: python-empty-generator

如何返回一个空的生成器：

    :::python
    >>> def foo():
    ...     return
    ...     yield
    ...
    >>> foo()
    <generator object foo at 0x01C46968>
    >>> list(foo())
    []
    >>>


## 参考

* [Python Empty Generator Function - Stack Overflow](http://stackoverflow.com/questions/13243766/python-empty-generator-function)
