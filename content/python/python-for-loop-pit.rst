[python]for 循环中的局部变量陷阱
################################

:date: 2013-10-13
:tags: python
:slug: python-for-loop-pit

先看一段代码：

.. code-block:: python

    >>> x = 10
    >>> [x for x in range(3)]
    [0, 1, 2]
    >>> x
    2

从这段代码，我们可以知道：for 循环中用于循环主体的变量会影响上下文的局部变量。

所以，类似下面这样的代码就会有问题：

.. code-block:: python

    for x in foo:
        # ...
        bar = [ x for x in foobar]
        n = x['abc']   # error
        # ...
