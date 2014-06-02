[python] 模块间互相导入的问题
==============================

:date: 2014-06-02
:tag: python
:slug: python-import-xy

两个模块间互相导入时，可能会出现如下的问题：

.. code-block:: python

    # a.py
    from b import y
    print y
    x = 5
    
    # b.py
    from a import x
    print x
    y = 10

    >>> import b
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "b.py", line 1, in <module>
        from a import x
      File "a.py", line 1, in <module>
        from b import y
    ImportError: cannot import name y
    >>>

因为在 b 中， ``from a import x`` 此时的 x 还不存在。

有三种办法可以解决这个问题：

* 模块间不要互相导入
* 使用 import ::

    # a.py
    import b
    x = 5
    # print b.y  不能立即访问 b 内的变量
    
    # b.py
    import a
    y = 10
    # print a.x  不能立即访问 a 内的变量
* 在函数中执行导入操作 ::

    # a.py
    def abc():
        from b import y
        print y
    x = 5
    abc()
    
    # b.py
    def efg():
        from a import x
        print x
    y = 10
    efg()
* 在文件末尾执行导入操作 ::

    # a.py
    x = 5
    from b import y
    print y
    
    # b.py
    y = 10
    from a import x
    print x

参考
-----

* `《Python 学习手册第4版》第 612 ~ 613 页 <http://book.douban.com/subject/6049132/>`__
