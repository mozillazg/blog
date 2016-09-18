Python: threading + multiprocessing + logging = 死锁 ?
============================================================

:slug: python-threading-multiprocessing-logging-equal-deadlock
:date: 2016-09-18


前段时间有个程序突然出现了子进程不工作的情况。

后来通过调查发现是因为程序中同时使用了多线程，多进程以及 logging
模块，导致子进程中出现了死锁的情况。

当创建子进程的时候，后台线程中的 logging 模块正好获取了一个锁(``threading.RLock``)在记录日志信息。由于在 unix/linux 平台下 Python 是通过 fork 来创建子进程的，因此创建子进程的时候会把 logging 中的锁也复制了一份，当子进程中需要记录日志的时候发现 logging 的锁一直处于被占用的状态，从而出现了死锁（复制的这个锁永远也不会被释放，因为它的所有者是父进程的某个线程，但是这个线程释放锁的时候又不会影响子进程里的这个锁）。


复现问题的代码如下:

.. code-block:: python

    import os
    import sys
    import threading
    import time


    class ThreadWorker(threading.Thread):
        def __init__(self):
            print('ThreadWorker: init')
            super().__init__()

        def run(self):
            print('ThreadWorker: running (rlock = {0})'.format(global_rlock))

            global_rlock.acquire()
            print('ThreadWorker: i got lock {0}'.format(global_rlock))
            time.sleep(5)
            global_rlock.release()
            print('ThreadWorker: release lock {0} and '
                  'sleeping forever'.format(global_rlock))

            time.sleep(600000)

    global_rlock = threading.RLock(verbose=True)
    worker = ThreadWorker()
    worker.start()

    time.sleep(1)
    print('forking')
    pid = os.fork()
    if pid != 0:    # pid != 0 当前处于父进程
        print('parent: running (rlock = {0})'.format(global_rlock))
    else:      # pid = 0 当前处于子进程
        print('child: running (rlock = {0}), '
              'getting the lock...'.format(global_rlock))
        global_rlock.acquire()
        print('child: got the lock {0}'.format(global_rlock))
        sys.exit(0)

    time.sleep(10)

上面代码的执行结果如下:

.. code-block:: bash

    $ python fork.py
    ThreadWorker: init
    ThreadWorker: running (rlock = <unlocked _thread.RLock object owner=0 count=0 at 0x10116cb40>)
    ThreadWorker: i got lock <locked _thread.RLock object owner=123145307557888 count=1 at 0x10116cb40>
    forking
    parent: running (rlock = <locked _thread.RLock object owner=123145307557888 count=1 at 0x10116cb40>)
    child: running (rlock = <locked _thread.RLock object owner=123145307557888 count=1 at 0x10116cb40>), getting the lock...
    ThreadWorker: release lock <unlocked _thread.RLock object owner=0 count=0 at 0x10116cb40> and sleeping forever

从上面的结果中可以看出来：虽然线程随后释放了获得的锁，但是子进程却永远的卡在了获取锁的地方。


那么, 应该如何解决这个问题呢？至少有三种解决办法:

* 先创建子进程，然后再创建线程:

.. code-block:: python

    import os
    import sys
    import threading
    import time


    class ThreadWorker(threading.Thread):
        def __init__(self):
            print('ThreadWorker: init')
            super().__init__()

        def run(self):
            print('ThreadWorker: running (rlock = {0})'.format(global_rlock))

            global_rlock.acquire()
            print('ThreadWorker: i got lock {0}'.format(global_rlock))
            time.sleep(5)
            global_rlock.release()
            print('ThreadWorker: release lock {0} and '
                  'sleeping forever'.format(global_rlock))

            time.sleep(600000)

    global_rlock = threading.RLock(verbose=True)
    worker = ThreadWorker()

    print('forking')
    pid = os.fork()
    if pid != 0:    # pid != 0 当前处于父进程
        print('parent: running (rlock = {0})'.format(global_rlock))
        worker.start()
    else:      # pid = 0 当前处于子进程
        time.sleep(1)
        print('child: running (rlock = {0}), '
              'getting the lock...'.format(global_rlock))
        global_rlock.acquire()
        print('child: got the lock {0}'.format(global_rlock))
        global_rlock.release()
        print('child: release the lock {0}'.format(global_rlock))
        sys.exit(0)

    time.sleep(10)

结果:

.. code-block:: bash

    $ python fork2.py
    ThreadWorker: init
    forking
    parent: running (rlock = <unlocked _thread.RLock object owner=0 count=0 at 0x10f24cb70>)
    ThreadWorker: running (rlock = <unlocked _thread.RLock object owner=0 count=0 at 0x10f24cb70>)
    ThreadWorker: i got lock <locked _thread.RLock object owner=123145307557888 count=1 at 0x10f24cb70>
    child: running (rlock = <unlocked _thread.RLock object owner=0 count=0 at 0x10f24cb70>), getting the lock...
    child: got the lock <locked _thread.RLock object owner=140735162044416 count=1 at 0x10f24cb70>
    child: release the lock <unlocked _thread.RLock object owner=0 count=0 at 0x10f24cb70>
    ThreadWorker: release lock <unlocked _thread.RLock object owner=0 count=0 at 0x10f24cb70> and sleeping forever

可以看到子进程和线程都能够正常获取锁。

* 不要混合使用 threading, multiprocessing, logging/其他使用了线程锁的模块。
  要么都是多线程，要么都是多进程。


* 另一个办法就是配置 logging 使用无锁的 handler 来记录日志信息。

.. * 还有一个解决办法是使用一个第三方模块 `python-atfork <https://github.com/google/python-atfork>`_ (这个模块已经停止维护)，这个模块可以给 logging 模块打 monkey patch。
..
.. pip install https://github.com/google/python-atfork/archive/master.zip

.. .. code-block:: python
..
..     import os
..     import sys
..     import threading
..     import time
..
..     import atfork
..     atfork.monkeypatch_os_fork_functions()
..
..
..     class ThreadWorker(threading.Thread):
..         def __init__(self):
..             print('ThreadWorker: init')
..             super(ThreadWorker, self).__init__()
..
..         def run(self):
..             print('ThreadWorker: running (rlock = {0})'.format(global_rlock))
..
..             global_rlock.acquire()
..             print('ThreadWorker: i got lock {0}'.format(global_rlock))
..             time.sleep(5)
..             global_rlock.release()
..             print('ThreadWorker: release lock {0} and '
..                   'sleeping forever'.format(global_rlock))
..
..             time.sleep(600000)
..
..     global_rlock = threading.RLock(verbose=True)
..     atfork.atfork(prepare=global_rlock.acquire,
..                   parent=global_rlock.release,
..                   child=global_rlock.release)
..
..     worker = ThreadWorker()
..     worker.start()
..
..     time.sleep(1)
..     print('forking')
..     pid = os.fork()
..     if pid != 0:    # pid != 0 当前处于父进程
..         print('parent: running (rlock = {0})'.format(global_rlock))
..     else:      # pid = 0 当前处于子进程
..         print('child: running (rlock = {0}), '
..               'getting the lock...'.format(global_rlock))
..         global_rlock.acquire()
..         print('child: got the lock {0}'.format(global_rlock))
..         sys.exit(0)
..
..     time.sleep(10)
..
..     $ python2 fork3.py
..     ThreadWorker: init
..     ThreadWorker: running (rlock = <_RLock owner=None count=0>)
..     Thread-1: <_RLock owner='Thread-1' count=1>.acquire(1): initial success
..     ThreadWorker: i got lock <_RLock owner='Thread-1' count=1>
..     forking
..     Thread-1: <_RLock owner=None count=0>.release(): final release
..     MainThread: <_RLock owner='MainThread' count=1>.acquire(1): initial success
..     MainThread: <_RLock owner=None count=0>.release(): final release
..     parent: running (rlock = <_RLock owner=None count=0>)
..     ThreadWorker: release lock <_RLock owner=None count=0> and sleeping forever
..     MainThread: <_RLock owner=None count=0>.release(): final release
..     child: running (rlock = <_RLock owner=None count=0>), getting the lock...
..     MainThread: <_RLock owner='MainThread' count=1>.acquire(1): initial success
..     child: got the lock <_RLock owner='MainThread' count=1>
..


参考资料
-------------

* `PythonLoggingThreadingMultiprocessingIntermixedStudy(Using modules Python logging, threading and multiprocessing in a single application.) < Main < TWiki <https://twiki.cern.ch/twiki/bin/view/Main/PythonLoggingThreadingMultiprocessingIntermixedStudy>`_
* `Issue 6721: Locks in the standard library should be sanitized on fork - Python tracker <http://bugs.python.org/issue6721>`_
* `multithreading - Deadlock with logging multiprocess/multithread python script - Stack Overflow <http://stackoverflow.com/questions/24509650/deadlock-with-logging-multiprocess-multithread-python-script>`_
* `python - 使用multiprocessing.Process调用start方法后，有较小的几率子进程中run方法未执行 - SegmentFault <https://segmentfault.com/q/1010000005919174>`_
* `python multiprocessing hanging, potential queue memory error? - Stack Overflow <http://stackoverflow.com/questions/14087527/python-multiprocessing-hanging-potential-queue-memory-error>`_
* `Threads and fork(): think twice before mixing them. | Linux Programming Blog <http://www.linuxprogrammingblog.com/threads-and-fork-think-twice-before-using-them>`_
