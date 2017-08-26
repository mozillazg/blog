asyncio 学习笔记：同步原语
==========================

:slug: python-asyncio-note-synchronization-primitives
:date: 2017-08-26
:tags: asyncio

本文是 https://pymotw.com/3/asyncio/synchronization.html
的学习笔记，强烈推荐直接阅读原文。

虽然 ``asyncio`` 应用一般都是单线程程序，但是它们仍然是并发程序。
为了支持安全的并发，\ ``asyncio`` 实现了一些 ``threading`` 和
``multiprocessing`` 模块中比较常用的类似的同步原语。

Lock
----

``Lock`` 可以用来安全的访问共享资源。

.. code:: python

    # asyncio_lock.py
    import asyncio
    import functools


    def unlock(lock):
        print('callback releasing lock')
        lock.release()


    async def coro1(lock):
        print('coro1 wating for the lock')
        with await lock:
            print('coro1 acquired lock')
        print('coro1 released lock')


    async def coro2(lock):
        print('coro2 wating for the lock')
        await lock
        try:
            print('coro2 acquired lock')
        finally:
            print('coro2 released lock')
            lock.release()


    async def main(loop):
        lock = asyncio.Lock()
        print('acquiring the lock before starting coroutines')
        await lock.acquire()
        print('lock acquired: {}'.format(lock.locked()))

        loop.call_later(0.1, functools.partial(unlock, lock))

        print('waiting for coroutines')
        await asyncio.wait([coro1(lock), coro2(lock)])


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

可以使用 ``await`` 来获取锁，使用 ``release()`` 方法来释放锁。也可以用
``with await`` 上下文语句来获取和释放锁。

::

    $ python3.6 asyncio_lock.py
    acquiring the lock before starting coroutines
    lock acquired: True
    waiting for coroutines
    coro1 wating for the lock
    coro2 wating for the lock
    callback releasing lock
    coro1 acquired lock
    coro1 released lock
    coro2 acquired lock
    coro2 released lock

Event
-----

``asyncio.Event`` 类似 ``threading.Event``
用来允许多个消费者等待某个事情发生，不用通过监听一个特殊的值的来说实现类似通知的功能。

.. code:: python

    # asyncio_event.py
    import asyncio
    import functools


    def set_event(event):
        print('setting event in callback')
        event.set()


    async def coro1(event):
        print('coro1 waiting for event')
        await event.wait()
        print('coro1 triggered')


    async def coro2(event):
        print('coro2 waiting for event')
        await event.wait()
        print('coro2 triggered')


    async def main(loop):
        event = asyncio.Event()
        print('event start state: {}'.format(event.is_set()))
        loop.call_later(
            0.1, functools.partial(set_event, event)
        )
        await asyncio.wait([coro1(event), coro2(event)])
        print('event end state: {}'.format(event.is_set()))


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

| 和 ``Lock`` 一样，\ ``coro1()`` 和 ``coro2()`` 都在等待 event 被设置。
| 不同的是它们都在 event 状态一发生变化的时候就启动了，它们不需要对
  event 对象获取一个唯一的所有权。

::

    $ python3.6 asyncio_event.py
    event start state: False
    coro1 waiting for event
    coro2 waiting for event
    setting event in callback
    coro1 triggered
    coro2 triggered
    event end state: True

Condition
---------

``Condition`` 的效果类似 ``Event``\ ，不同的是它不是唤醒所有等待中的
coroutine, 而是通过 ``notify()`` 唤醒指定数量的待唤醒 coroutine。

.. code:: python

    # asyncio_condition.py
    import asyncio


    async def consumer(condition, n):
        with await condition:
            print('consumer {} is waiting'.format(n))
            await condition.wait()
            print('consumer {} triggered'.format(n))
        print('ending consumer {}'.format(n))


    async def manipulate_condition(condition):
        print('starting manipulate_condition')

        await asyncio.sleep(0.1)

        for i in range(1, 3):
            with await condition:
                print('notifying {} consumers'.format(i))
                condition.notify(n=i)
            await asyncio.sleep(0.1)

        with await condition:
            print('notifying remaining consumers')
            condition.notify_all()

        print('ending manipulate_condition')


    async def main(loop):
        condition = asyncio.Condition()

        consumers = [
            consumer(condition, i)
            for i in range(5)
        ]

        loop.create_task(manipulate_condition(condition))

        await asyncio.wait(consumers)


    event_loop = asyncio.get_event_loop()
    try:
        result = event_loop.run_until_complete(main(event_loop))
    finally:
        event_loop.close()

在这个例子中，我们启动了五个 Condition 的消费者，每个都使用 ``wait()``
方法来等待它们可以继续处理的通知。\ ``manipulate_condition()``
首先通知了一个消费者，然后有通知了两个消费者，最后通知剩下的所有消费者。

::

    $ python3.6 asyncio_condition.py
    starting manipulate_condition
    consumer 0 is waiting
    consumer 4 is waiting
    consumer 1 is waiting
    consumer 2 is waiting
    consumer 3 is waiting
    notifying 1 consumers
    consumer 0 triggered
    ending consumer 0
    notifying 2 consumers
    consumer 4 triggered
    ending consumer 4
    consumer 1 triggered
    ending consumer 1
    notifying remaining consumers
    ending manipulate_condition
    consumer 2 triggered
    ending consumer 2
    consumer 3 triggered
    ending consumer 3

Queue
-----

``asyncio.Queue`` 为 coroutines
实现了一个先进先出的数据结构，类似多线程中的 ``queue.Queue``
，多进程中的 ``multiprocessing.Queue``

.. code:: python

    # asyncio_queue.py
    import asyncio


    async def consumer(n, q):
        print('consumer {}: waiting for item'.format(n))
        while True:
            print('consumer {}: waiting for item'.format(n))
            item = await q.get()
            print('consumer {}: has item {}'.format(n, item))
            # 在这个程序中 None 是个特殊的值，表示终止信号
            if item is None:
                q.task_done()
                break
            else:
                await asyncio.sleep(0.01 * item)
                q.task_done()

        print('consumer {}: ending'.format(n))


    async def producer(q, num_workers):
        print('producer: starting')
        # 向队列中添加一些数据
        for i in range(num_workers * 3):
            await q.put(i)
            print('producer: added task {} to the queue'.format(i))

        # 通过 None 这个特殊值来通知消费者退出
        print('producer: adding stop signals to the queue')
        for i in range(num_workers):
            await q.put(None)
        print('producer: waiting for queue to empty')
        await q.join()
        print('producer: ending')


    async def main(loop, num_consumers):
        # 创建指定大小的队列，这样的话生产者将会阻塞
        # 直到有消费者获取数据
        q = asyncio.Queue(maxsize=num_consumers)

        # 调度消费者
        consumers = [
            loop.create_task(consumer(i, q))
            for i in range(num_consumers)
        ]

        # 调度生产者
        prod = loop.create_task(producer(q, num_consumers))

        # 等待所有 coroutines 都完成
        await asyncio.wait(consumers + [prod])


    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop, 2))
    finally:
        event_loop.close()

通过 ``put()`` 添加项或者通过 ``get()``
移除项都是异步操作，同时有可能队列大小达到指定大小（阻塞添加操作）或者队列变空（阻塞所有获取项的调用）。

::

    $ python3.6 asyncio_queue.py
    consumer 0: waiting for item
    consumer 0: waiting for item
    consumer 1: waiting for item
    consumer 1: waiting for item
    producer: starting
    producer: added task 0 to the queue
    producer: added task 1 to the queue
    consumer 0: has item 0
    consumer 1: has item 1
    producer: added task 2 to the queue
    producer: added task 3 to the queue
    consumer 0: waiting for item
    consumer 0: has item 2
    producer: added task 4 to the queue
    consumer 1: waiting for item
    consumer 1: has item 3
    producer: added task 5 to the queue
    producer: adding stop signals to the queue
    consumer 0: waiting for item
    consumer 0: has item 4
    consumer 1: waiting for item
    consumer 1: has item 5
    producer: waiting for queue to empty
    consumer 0: waiting for item
    consumer 0: has item None
    consumer 0: ending
    consumer 1: waiting for item
    consumer 1: has item None
    consumer 1: ending
    producer: ending

参考资料
--------

-  `Synchronization Primitives — PyMOTW
   3 <https://pymotw.com/3/asyncio/synchronization.html>`__
-  `18.5.7. Synchronization primitives — Python 3.6.2
   documentation <https://docs.python.org/3.6/library/asyncio-sync.html>`__
