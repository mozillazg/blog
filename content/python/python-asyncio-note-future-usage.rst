asyncio 学习笔记：产生异步结果
==============================

:slug: python-asyncio-note-future-usage
:date: 2017-08-20
:tags: asyncio

本文是 https://pymotw.com/3/asyncio/futures.html
的学习笔记，强烈推荐直接阅读原文。

``Future`` 对象表示一个还未完成的工作，事件循环可以监视 ``Future``
对象的状态直至它变成
done，这将运行程序的一部分等待另一部分完成一些工作。

等待一个 Future 对象
--------------------

示例:

.. code:: python

    # asyncio_future_event_loop.py
    import asyncio

    def mark_done(future, result):
        print('setting future result to {!r}'.format(result))
        future.set_result(result)


    event_loop = asyncio.get_event_loop()
    all_done = asyncio.Future()
    try:
        print('scheduling make_done')
        event_loop.call_soon(mark_done, all_done, 'the result')
        print('entering event loop')
        result = event_loop.run_until_complete(all_done)
        print('returned result: {!r}'.format(result))
    finally:
        print('closing event loop')
        event_loop.close()

    print('future result: {!r}'.format(all_done.result()))

当调用 ``set_result`` 方法后，\ ``Future`` 对象的状态会被修改为 done,
同时 \`Future\`\` 实例也会保存设置的结果值，供随后使用:

::

    $ python3.6 asyncio_future_event_loop.py
    scheduling make_done
    entering event loop
    setting future result to 'the result'
    returned result: 'the result'
    closing event loop
    future result: 'the result'

``Future`` 对象也可以同 ``await`` 关键字一起使用:

.. code:: python

    # asyncio_future_await.py
    import asyncio


    def mark_done(future, result):
        print('setting future result to {!r}'.format(result))
        future.set_result(result)


    async def main(loop):
        all_done = asyncio.Future()
        print('scheduling mark_done')
        loop.call_soon(mark_done, all_done, 'the result')
        result = await all_done
        print('returned result: {!r}'.format(result))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

``await`` 会返回 ``Future`` 的结果：

::

    $ python3.6 asyncio_future_await.py
    scheduling mark_done
    setting future result to 'the result'
    returned result: 'the result'

Future 回调函数
---------------

``Future``
在完成的时候可以执行一些回调函数，回调函数按注册时的顺序进行调用:

.. code:: python

    # asyncio_future_await.py
    import asyncio


    def mark_done(future, result):
        print('setting future result to {!r}'.format(result))
        future.set_result(result)


    async def main(loop):
        all_done = asyncio.Future()
        print('scheduling mark_done')
        loop.call_soon(mark_done, all_done, 'the result')
        result = await all_done
        print('returned result: {!r}'.format(result))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

回调函数的第一个参数是 ``Future`` 实例，要传递其他参数可以使用
``functools.partial()`` 来实现。

::

    $ python3.6 asyncio_future_callback.py
    registering callbacks on future
    setting result of future
    1: future done: the result
    2: future done: the result

参考资料
--------

-  `Producing Results Asynchronously — PyMOTW
   3 <https://pymotw.com/3/asyncio/futures.html>`__
-  `18.5.3. Tasks and coroutines — Python 3.6.2
   documentation <https://docs.python.org/3/library/asyncio-task.html>`__
