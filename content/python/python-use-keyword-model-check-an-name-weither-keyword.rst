[python]使用 keyword 模块检查变量名是否是 python 关键字
=========================================================
:date: 2016-03-08
:slug: python-use-keyword-model-check-an-name-weither-keyword

无意中发现 python 标准库中包含呢一个 ``keyword`` 模块
可以用来检查一个变量名是否是 python 关键字:

.. code-block:: python

    >>> import keyword
    >>> keyword.iskeyword('is')
    True
    >>> keyword.iskeyword('name')
    False

    >>> keyword.kwlist
    ['False', 'None', 'True', 'and', 'as', ..., 'with', 'yield']

这个模块只有两个函数:

* ``keyword.iskeyword(s)``: 是否是关键字
* ``keyword.kwlist``: 返回解释器定义的所有关键字列表


参考资料
-----------

* `32.6. keyword — Testing for Python keywords — Python 3.5.1 documentation <https://docs.python.org/3/library/keyword.html>`__
