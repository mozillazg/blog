asyncio 学习笔记：调用定时函数
==============================

:slug: python-asyncio-note-coroutine-schedule
:date: 2017-08-17
:tags: asyncio

本文是 https://pymotw.com/3/asyncio/scheduling.html
的学习笔记，强烈推荐直接阅读原文。

立马执行一个函数
----------------

``call_soon``
支持在下一次事件循环的迭代中执行提供的回调函数。回调函数只能传递位置参数，如果想指定关键字参数的话，可以使用
functools.partial 函数来辅助使用。

.. code:: python

    # asyncio_call_soon.py
    import asyncio
    import functools


    def callback(arg, *, kwarg='default'):
        print('callback with {0} and {1}'.format(arg, kwarg))


    async def main(loop):
        print('register callbacks')
        loop.call_soon(callback, 1)
        wrapped = functools.partial(callback, kwarg='not default')
        loop.call_soon(wrapped, 2)

        await asyncio.sleep(0.1)


    event_loop = asyncio.get_event_loop()
    try:
        print('entering event loop')
        event_loop.run_until_complete(main(event_loop))
    finally:
        print('closing event loop')
        event_loop.close()

回调函数会按调度顺序执行:

::

    $ python3.6 asyncio_call_soon.py
    entering event loop
    register callbacks
    callback with 1 and default
    callback with 2 and not default
    closing event loop

延迟执行
--------

可以使用 ``call_later``
方法实现延迟多少秒后执行回调函数。\ ``call_later``
的第一个参数是延迟多少秒，第二个参数是回调函数，后面的参数是回调函数的位置参数:

.. code:: python

    # asyncio_call_later.py
    import asyncio


    def callback(n):
        print('callback with {0}'.format(n))


    async def main(loop):
        print('register callbacks')
        loop.call_later(0.2, callback, 1)
        loop.call_later(0.1, callback, 2)
        loop.call_soon(callback, 3)

        await asyncio.sleep(0.4)


    event_loop = asyncio.get_event_loop()
    try:
        print('entering event loop')
        event_loop.run_until_complete(main(event_loop))
    finally:
        print('closing event loop')
        event_loop.close()

执行结果：

::

    $ python3.6 asyncio_call_later.py
    entering event loop
    register callbacks
    callback with 3
    callback with 2
    callback with 1
    closing event loop

指定时间执行
------------

可以使用 ``call_at``
方法实现在将来指定的某个时间执行回调函数。\ ``call_at``
的第一个参数是执行的时间点，第二个参数是回调函数，后面的参数是回调函数的位置参数。有一点需要注意的是不用使用
``time`` 或 ``datetime`` 模块的时间点，要使用 ``loop.time()``
获取当前时间。

.. code:: python

    # asyncio_call_at.py
    import asyncio
    import time


    def callback(n, loop):
        print('callback with {0} at {1}'.format(n, loop.time()))


    async def main(loop):
        now = loop.time()
        print('clock time: {0}'.format(time.time()))
        print('loop time: {0}'.format(now))

        print('register callbacks')
        loop.call_at(now + 0.2, callback, 1, loop)
        loop.call_at(now + 0.1, callback, 2, loop)
        loop.call_soon(callback, 3, loop)

        await asyncio.sleep(1)


    event_loop = asyncio.get_event_loop()
    try:
        print('entering event loop')
        event_loop.run_until_complete(main(event_loop))
    finally:
        print('closing event loop')
        event_loop.close()

再次提醒，不要用 ``time.time()`` 来计算时间，而是应该使用
``loop.time()``\ ，它们其实是不同的：

::

    $ python3.6 asyncio_call_at.py
    entering event loop
    clock time: 1502272983.100926
    loop time: 513773.744280748
    register callbacks
    callback with 3 at 513773.744416457
    callback with 2 at 513773.848605754
    callback with 1 at 513773.94877137
    closing event loop

参考资料
--------

-  `Scheduling Calls to Regular Functions — PyMOTW
   3 <https://pymotw.com/3/asyncio/scheduling.html>`__
-  `18.5.1. Base Event Loop — Python 3.6.2
   documentation <https://docs.python.org/3/library/asyncio-eventloop.html>`__
