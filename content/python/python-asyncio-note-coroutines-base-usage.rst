asyncio 学习笔记：基本用法
==========================

:slug: python-asyncio-note-coroutines-base-usage
:date: 2017-08-17
:tags: asyncio

本文是 https://pymotw.com/3/asyncio/coroutines.html
的学习笔记，强烈推荐直接阅读原文。

启动一个 Coroutine
------------------

启动一个 Coroutine 的最简单的一个方法就是使用
``asyncio.run_until_complete`` 函数：

.. code:: python

    # asyncio_coroutine.py
    import asyncio


    async def coroutine():
        print('in coroutine')


    event_loop = asyncio.get_event_loop()
    try:
        print('starting coroutine')
        coro = coroutine()
        print('entering event loop')
        event_loop.run_until_complete(coro)
    finally:
        print('closing event loop')
        event_loop.close()

首先是获取一个事件循环，然后用 ``run_until_complete`` 执行 Coroutine
对象，当 Coroutine 执行完成并退出时， ``run_until_complete``
也会随后退出。

::

    $ python3.6 asyncio_coroutine.py
    starting coroutine
    entering event loop
    in coroutine
    closing event loop

获取 Coroutine 的返回值
-----------------------

``run_until_complete`` 会把 Coroutine
的返回值当做自身的返回值返回给调用方：

.. code:: python

    # asyncio_coroutine_return.py

    import asyncio


    async def coroutine():
        print('in coroutine')
        return 'result'


    event_loop = asyncio.get_event_loop()
    try:
        return_value = event_loop.run_until_complete(coroutine())
        print('it returned: {!r}'.format(return_value))
    finally:
        event_loop.close()

执行结果:

::

    $ python3.6 asyncio_coroutine_return.py
    in coroutine
    it returned: 'result'

链式调用 Coroutine
------------------

即在一个 Coroutine 函数中调用另外的 Coroutine 函数，同时还需要等待这个
Coroutine 函数返回结果。

.. code:: python

    # asyncio_coroutine_chain.py
    import asyncio


    async def one():
        print('in one')
        return 'one'


    async def two(arg):
        print('in two')
        return 'two with arg {}'.format(arg)


    async def outer():
        print('in outer')
        print('waiting for one')
        result1 = await one()
        print('waiting for two')
        result2 = await two(result1)
        return result1, result2


    event_loop = asyncio.get_event_loop()
    try:
        return_value = event_loop.run_until_complete(outer())
        print('result value: {!r}'.format(return_value))
    finally:
        event_loop.close()

可以直接使用 ``await`` 等待 Coroutine 返回结果。

::

    $ python3.6 asyncio_coroutine_chain.py
    in outer
    waiting for one
    in one
    waiting for two
    in two
    result value: ('one', 'two with arg one')

使用生成器代替 Coroutine
------------------------

在 Python 3.5 之前的 Python 3 版本中还没有 ``async/await``
语法，我们可以使用 ``asyncio.coroutine`` 装饰器加 ``yield from``
来实现同样的功能:

.. code:: python

    # asyncio_generator.py
    import asyncio


    @asyncio.coroutine
    def one():
        print('in one')
        return 'one'


    @asyncio.coroutine
    def two(arg):
        print('in two')
        return 'two with arg {}'.format(arg)


    @asyncio.coroutine
    def outer():
        print('in outer')
        print('waiting for one')
        result1 = yield from one()
        print('waiting for two')
        result2 = yield from two(result1)
        return result1, result2


    event_loop = asyncio.get_event_loop()
    try:
        return_value = event_loop.run_until_complete(outer())
        print('result value: {!r}'.format(return_value))
    finally:
        event_loop.close()

执行结果：

::

    $ python3.4 asyncio_generator.py
    in outer
    waiting for one
    in one
    waiting for two
    in two
    result value: ('one', 'two with arg one')

参考资料
--------

-  `Cooperative Multitasking with Coroutines — PyMOTW
   3 <https://pymotw.com/3/asyncio/coroutines.html>`__
-  `18.5.1. Base Event Loop — Python 3.6.2
   documentation <https://docs.python.org/3/library/asyncio-eventloop.html>`__
