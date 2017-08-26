asyncio 学习笔记：控制组合式 Coroutines
=======================================

:slug: python-asyncio-note-control-Coroutines
:date: 2017-08-25
:tags: asyncio


本文是 https://pymotw.com/3/asyncio/control.html
的学习笔记，强烈推荐直接阅读原文。

对于线性执行的 Coroutines 可以很方便的通过 ``await`` 来控制。
对于组合式的 Coroutines，比如在一个 coroutine 中等待其他并发执行的
Coroutines 完成的操作也可以通过 asyncio 模块来实现。

等待多个 Coroutines
-------------------

| 在一个 Coroutine 中等待其他多个 Coroutines
  操作完成是一个很常见的需求，比如下载一批数据，执行对顺序没有要求，只想要最后的结果。
| ``wait()`` 方法可以实现暂停当前 Coroutine， 直到后台其他 Coroutines
  操作完成：

.. code:: python

    # asyncio_wait.py
    import asyncio


    async def phase(i):
        print('in phase {}'.format(i))
        await asyncio.sleep(0.1 * i)
        print('done with phase {}'.format(i))
        return 'phase {} result'.format(i)


    async def main(num_phases):
        print('starting main')
        phases = [
            phase(i)
            for i in range(num_phases)
        ]
        print('waiting for phases to complete')
        completed, pending = await asyncio.wait(phases)
        results = [t.result() for t in completed]
        print('results: {!r}'.format(results))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(3))
    finally:
        event_loop.close()

在 ``wait`` 内部，它使用一个集合来保存它创建的 ``Task``
实例，所以它保存的 ``Task`` 的结果是无序的。\ ``wait``
返回一个由两个集合组成的元祖，一个保存状态为 done 的 ``Task``
，一个保存状态为 pending 的 ``Task``:

::

    $ python3.6 asyncio_wait.py
    starting main
    waiting for phases to complete
    in phase 0
    in phase 2
    in phase 1
    done with phase 0
    done with phase 1
    done with phase 2
    results: ['phase 0 result', 'phase 2 result', 'phase 1 result']

当调用 ``wait`` 时指定 ``timeout`` 参数才会有可能出现结果中包含状态为
pending 的 ``Task``:

.. code:: python

    # asyncio_wait_timeout.py
    import asyncio


    async def phase(i):
        print('in phase {}'.format(i))
        try:
            await asyncio.sleep(0.1 * i)
        except asyncio.CancelledError:
            print('phase {} canceled'.format(i))
            raise
        else:
            print('done with phase {}'.format(i))
            return 'phase {} result'.format(i)


    async def main(num_phases):
        print('starting main')
        phases = [
            phase(i)
            for i in range(num_phases)
        ]
        print('waiting 0.1 for phases to complete')
        completed, pending = await asyncio.wait(phases, timeout=0.1)
        print('{} completed and {} pending'.format(
            len(completed), len(pending),
        ))
        if pending:
            print('canceling tasks')
            for t in pending:
                t.cancel()

        print('exiting main')


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(3))
    finally:
        event_loop.close()

对于 pending 的 task 最好是把它们 cancel
掉，否则事件循环在之后会继续执行它们或者退出程序的时候会有警告信息.

::

    $ python3.6 asyncio_wait_timeout.py
    starting main
    waiting 0.1 for phases to complete
    in phase 0
    in phase 2
    in phase 1
    done with phase 0
    1 completed and 2 pending
    canceling tasks
    exiting main
    phase 1 canceled
    phase 2 canceled

不 cancel 会警告的情况:

.. code:: python

    # asyncio_wait_timeout_without_cancel.py
    import asyncio


    async def phase(i):
        print('in phase {}'.format(i))
        try:
            await asyncio.sleep(0.1 * i)
        except asyncio.CancelledError:
            print('phase {} canceled'.format(i))
            raise
        else:
            print('done with phase {}'.format(i))
            return 'phase {} result'.format(i)


    async def main(num_phases):
        print('starting main')
        phases = [
            phase(i)
            for i in range(num_phases)
        ]
        print('waiting 0.1 for phases to complete')
        completed, pending = await asyncio.wait(phases, timeout=0.1)
        print('{} completed and {} pending'.format(
            len(completed), len(pending),
        ))

        print('exiting main')


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(3))
    finally:
        event_loop.close()

运行结果:

::

    $ python3.6 asyncio_wait_timeout_without_cancel_warn.py
    starting main
    waiting 0.1 for phases to complete
    in phase 1
    in phase 0
    in phase 2
    done with phase 0
    1 completed and 2 pending
    exiting main
    done with phase 1
    Task was destroyed but it is pending!
    task: <Task pending coro=<phase() done, defined at asyncio_wait_timeout_without_cancel_warn.py:5> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x10e227918>()]>>

pending 还会继续执行的情况:

.. code:: python

    # asyncio_wait_timeout_without_cancel_continue.py
    import asyncio


    async def phase(i):
        print('in phase {}'.format(i))
        try:
            await asyncio.sleep(0.1 * i)
        except asyncio.CancelledError:
            print('phase {} canceled'.format(i))
            raise
        else:
            print('done with phase {}'.format(i))
            return 'phase {} result'.format(i)


    async def main(num_phases):
        print('starting main')
        phases = [
            phase(i)
            for i in range(num_phases)
        ]
        print('waiting 0.1 for phases to complete')
        completed, pending = await asyncio.wait(phases, timeout=0.1)
        print('{} completed and {} pending'.format(
            len(completed), len(pending),
        ))

        print('exiting main')


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(3))
        event_loop.run_until_complete(asyncio.sleep(3))
    finally:
        event_loop.close()

运行结果

::

    $ python3.6 asyncio_wait_timeout_without_cancel_continue.py
    starting main
    waiting 0.1 for phases to complete
    in phase 1
    in phase 0
    in phase 2
    done with phase 0
    1 completed and 2 pending
    exiting main
    done with phase 1
    done with phase 2

收集 Coroutines 结果
--------------------

如果 Coroutines
是在程序中显示生成的，并且只关心返回值结果的话，\ ``gather()``
是一种比较好的收集多个操作结果的方法：

.. code:: python

    # asyncio_gather.py
    import asyncio


    async def phase1():
        print('in phase1')
        await asyncio.sleep(2)
        print('done with phase1')
        return 'phase1 result'


    async def phase2():
        print('in phase2')
        await asyncio.sleep(1)
        print('done with phase2')
        return 'phase2 result'


    async def main():
        print('starting main')
        print('waiting for phases to complete')
        results = await asyncio.gather(
            phase1(),
            phase2()
        )
        print('results: {!r}'.format(results))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main())
    finally:
        event_loop.close()

通过 gather 创建的 task
对外部是不可见的，所以它们不能被取消。返回值是按输入参数顺序保存的对应
coroutine
的执行结果，无论真正执行的时候是否按顺序执行的，最终的结果都是有序的。

::

    $ python3.6 asyncio_gather.py
    starting main
    waiting for phases to complete
    in phase2
    in phase1
    done with phase2
    done with phase1
    results: ['phase1 result', 'phase2 result']

当后台操作完成的时候做一些事情
------------------------------

| ``as_completed()`` 是一个生成器，它将管理传入的 coroutines 执行，
| 每次迭代都将返回一个 coroutine 执行完成的 task。
| 跟 ``wait()`` 一样，\ ``as_completed()`` 也不会保证顺序，跟 ``wait()``
  的区别就是它不会等待所有的
| coroutine 操作都完成以后才能做其他操作。

.. code:: python

    # asyncio_as_completed.py
    import asyncio


    async def phase(i):
        print('in phase {}'.format(i))
        await asyncio.sleep(0.5 - (0.1 * i))
        print('done with phase {}'.format(i))
        return 'phase {} result'.format(i)


    async def main(num_phases):
        print('starting main')
        phases = [
            phase(i)
            for i in range(num_phases)
        ]
        print('waiting for phases to complete')
        results = []
        for next_to_complete in asyncio.as_completed(phases):
            answer = await next_to_complete
            print('recevived answer {!r}'.format(answer))
            results.append(answer)
        print('results: {!r}'.format(results))
        return results


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(3))
    finally:
        event_loop.close()

结果:

::

    $ python3.6 asyncio_as_completed.py
    starting main
    waiting for phases to complete
    in phase 1
    in phase 2
    in phase 0
    done with phase 2
    recevived answer 'phase 2 result'
    done with phase 1
    recevived answer 'phase 1 result'
    done with phase 0
    recevived answer 'phase 0 result'
    results: ['phase 2 result', 'phase 1 result', 'phase 0 result']

参考资料
--------

-  `Composing Coroutines with Control Structures — PyMOTW
   3 <https://pymotw.com/3/asyncio/control.html>`__
-  `18.5.3. Tasks and coroutines — Python 3.6.2
   documentation <https://docs.python.org/3.6/library/asyncio-task.html>`__
