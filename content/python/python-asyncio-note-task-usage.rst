asyncio 学习笔记：并发执行 Task
===============================

:slug: python-asyncio-note-task-usage
:date: 2017-08-20
:tags: asyncio


本文是 https://pymotw.com/3/asyncio/tasks.html
的学习笔记，强烈推荐直接阅读原文。

Task 是跟事件循环交互的一种主要方式。Task 包装并追踪 Coroutine
的完成状态。Task 是 ``Future`` 的子类，因此其他 Coroutine 可以 wait Task
并且在 Task 完成时还可以获取 Coroutine 的结果。

启动 Task
---------

可以使用 ``create_task`` 来创建一个 ``Task`` 实例:

.. code:: python

    # asyncio_create_task.py
    import asyncio


    async def task_func():
        print('in task_func')
        return 'the result'


    async def main(loop):
        print('creating task')
        task = loop.create_task(task_func())
        print('waiting for {!r}'.format(task))
        return_value = await task
        print('task completed {!r}'.format(task))
        print('return value: {!r}'.format(return_value))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

可以看到 ``await task`` 返回的是 ``task_func`` 函数的返回值:

::

    $ python3.6 asyncio_create_task.py
    creating task
    waiting for <Task pending coro=<task_func() running at asyncio_create_task.py:5>>
    in task_func
    task completed <Task finished coro=<task_func() done, defined at asyncio_create_task.py:5> result='the result'>
    return value: 'the result'

取消 Task
---------

可以在 ``Task`` 完成之前取消 task 的操作:

.. code:: python

    # asyncio_cancel_task.py
    import asyncio


    async def task_func():
        print('in task_func')
        return 'the result'


    async def main(loop):
        print('creating task')
        task = loop.create_task(task_func())

        print('canceling task')
        task.cancel()

        print('canceled task {!r}'.format(task))
        try:
            await task
        except asyncio.CancelledError:
            print('caught error from canceled task')
        else:
            print('task result: {!r}'.format(task.result()))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

当在事件循环启动前取消一下 task 时， ``await task`` 会抛出
``CancelledError`` 异常:

::

    $ python3.6 asyncio_cancel_task.py
    creating task
    canceling task
    canceled task <Task cancelling coro=<task_func() running at asyncio_cancel_task.py:5>>
    caught error from canceled task

当取消一个正在等待其他 concurrent 操作的 task 时，等待操作的位置会抛出
``CancelledError`` 异常:

.. code:: python

    # asyncio_cancel_task2.py
    import asyncio


    async def task_func():
        print('in task_func, sleeping')
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            print('task_func was canceled')
            raise
        return 'the result'


    def task_canceller(t):
        print('in task_canceller')
        t.cancel()
        print('canceled the task')


    async def main(loop):
        print('creating task')
        task = loop.create_task(task_func())
        loop.call_soon(task_canceller, task)
        try:
            await task
        except asyncio.CancelledError:
            print('main() also sees task as canceled')


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

结果:

::

    $ python3.6 asyncio_cancel_task2.py
    creating task
    in task_func, sleeping
    in task_canceller
    canceled the task
    task_func was canceled
    main() also sees task as canceled

上面 asyncio\_cancel\_task2.py 的 ``task_func`` 中如果没有把
``CancelledError`` 异常再 raise 出来的话，其实还是会继续执行下去的:

.. code:: python

    # asyncio_cancel_task3.py
    import asyncio


    async def task_func():
        print('in task_func, sleeping')
        try:
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            print('task_func was canceled')
        print('task_func still active')
        return 'the result'


    def task_canceller(t):
        print('in task_canceller')
        ok = t.cancel()
        print('canceled the task: {0}'.format(ok))


    async def main(loop):
        print('creating task')
        task = loop.create_task(task_func())
        loop.call_soon(task_canceller, task)
        return_value = await task
        print('task completed {!r}'.format(task))
        print('return value: {!r}'.format(return_value))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

结果:

::

    $ python3.6 asyncio_cancel_task3.py
    creating task
    in task_func, sleeping
    in task_canceller
    canceled the task: True
    task_func was canceled
    task_func still active
    task completed <Task finished coro=<task_func() done, defined at asyncio_cancel_task3.py:5> result='the result'>
    return value: 'the result'

在 Coroutine 中创建 Task
------------------------

``ensure_future()`` 函数返回一个与一个 coroutine 的执行相关连的
Task。这个 Task
实例可以作为变量传入其他代码中，这样的话其他代码就可以直接 await 这个
Task 而不需要知道原始的 coroutine 是如何被创建的。

.. code:: python

    # asyncio_ensure_future.py
    import asyncio


    async def wrapped():
        print('wrapped')
        return 'result'


    async def inner(task):
        print('inner: starting')
        print('inner: waiting for {!r}'.format(task))
        result = await task
        print('inner: task returned {!r}'.format(result))


    async def starter():
        print('starter: creating task')
        task = asyncio.ensure_future(wrapped())
        print('starter: waiting for inner')
        await inner(task)
        print('starter: inner returned')


    event_loop = asyncio.get_event_loop()
    try:
        print('entering event loop')
        result = event_loop.run_until_complete(starter())
    finally:
        event_loop.close()

需要注意的是，传入 ``ensure_future()`` 的 coroutine
不会立马启动，需要有某个地方使用了 ``await`` 语句操作创建的 task
的时候它才会被执行。

::

    $ python3.6 asyncio_ensure_future.py
    entering event loop
    starter: creating task
    starter: waiting for inner
    inner: starting
    inner: waiting for <Task pending coro=<wrapped() running at asyncio_ensure_future.py:5>>
    wrapped
    inner: task returned 'result'
    starter: inner returned

参考资料
--------

-  `Executing Tasks Concurrently — PyMOTW
   3 <https://pymotw.com/3/asyncio/tasks.html>`__
-  `18.5.3. Tasks and coroutines — Python 3.6.2
   documentation <https://docs.python.org/3/library/asyncio-task.html>`__
