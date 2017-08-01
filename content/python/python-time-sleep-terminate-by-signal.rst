Python: time.sleep 与 signal 一起使用可能会出现 sleep 被提前终止的情况
=====================================================================================

:slug: python-time-sleep-terminate-by-signal
:date: 2017-07-18
:tags: signal


如题所述，当 ``time.sleep`` 与 ``signal`` 一起使用时可能会出现 ``time.sleep``
失效，提前结束 sleep 的问题。

我们先来看一下 ``time.sleep`` 的文档:

Python 2.7.13:


    time.sleep(secs)

        Suspend execution of the current thread for the given number of seconds. The argument may be a floating point number to indicate a more precise sleep time. **The actual suspension time may be less than that requested because any caught signal will terminate the sleep() following execution of that signal’s catching routine.** Also, the suspension time may be longer than requested by an arbitrary amount because of the scheduling of other activity in the system.

Python 3.6.2:


    time.sleep(secs)

        Suspend execution of the calling thread for the given number of seconds. The argument may be a floating point number to indicate a more precise sleep time. **The actual suspension time may be less than that requested because any caught signal will terminate the sleep() following execution of that signal’s catching routine.** Also, the suspension time may be longer than requested by an arbitrary amount because of the scheduling of other activity in the system.

        Changed in version 3.5: **The function now sleeps at least secs even if the sleep is interrupted by a signal, except if the signal handler raises an exception** (see `PEP 475 <https://www.python.org/dev/peps/pep-0475>`__ for the rationale).

通过文档可以看到，在 Python 2 下，当定义了 signal handler 并接收到
signal 时， ``time.sleep`` 会提前返回， 在 Python 3.5+
下，没有这个问题，只是在 signal handler 抛异常时 sleep 会被终止 。

下面我们就来验证一下这个问题。

测试环境
--------

-  os: mac os
-  python: python2.7, python3.6

Python 2
--------

普通 sleep 程序
~~~~~~~~~~~~~~~

先来看一个正常 sleep 的程序:

.. code-block:: python

    $ cat time_a.py
    import logging
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(levelname)s - %(message)s'
    )

    n = 60

    logging.info('start sleep %s seconds', n)
    start = time.time()
    time.sleep(n)
    logging.info('end sleep %s seconds, spend %s', n, time.time() - start)

测试:

::

    $ python time_a.py
    2017-07-16 15:29:05,323 - INFO - start sleep 60 seconds
    2017-07-16 15:30:05,327 - INFO - end sleep 60 seconds, spend 60.0042099953

可以看到确实 sleep 了 60 秒。

signal
~~~~~~

给普通的 sleep 程序发个 signal 试试:

::

    $ python time_a.py &
    [1] 6208
    $ 2017-07-16 15:44:01,290 - INFO - start sleep 60 seconds

    $ kill -s SIGHUP 6208
    [1]+  Hangup: 1               python time_a.py

因为 ``SIGHUP`` 的默认行为就是终止程序，所以程序终止了。

我们下面来测试自定义 signal handler 的影响。

signal handler
~~~~~~~~~~~~~~

测试程序如下：

.. code-block:: python

    $ cat time_b.py
    import logging
    import signal
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(levelname)s - %(message)s'
    )

    n = 60

    def handler(sig, strace):
        logging.info('recived %s', sig)

    signal.signal(signal.SIGHUP, handler)

    logging.info('start sleep %s seconds', n)
    start = time.time()
    time.sleep(n)
    logging.info('end sleep %s seconds, spend %s', n, time.time() - start)

测试:

::

    $ python time_b.py &
    [1] 5910
    2017-07-16 15:31:46,448 - INFO - start sleep 60 seconds
    $ kill -s SIGHUP 5910
    2017-07-16 15:31:52,180 - INFO - recived 1
    2017-07-16 15:31:52,181 - INFO - end sleep 60 seconds, spend 5.73180794716
    [1]+  Done                    python time_b.py

从测试结果可以看到，当收到 signal 后，sleep 就提前结束了， 60 秒的 sleep
实际只花了 6 秒钟。

下面再看看 Python 3 文档中提到的 handler 抛异常的情况。

signal handler raise exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

测试程序：

.. code-block:: python

    $ cat time_c.py
    import logging
    import signal
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(levelname)s - %(message)s'
    )

    n = 60

    def handler(sig, strace):
        logging.info('recived %s', sig)
        raise Exception('test')

    signal.signal(signal.SIGHUP, handler)

    logging.info('start sleep %s seconds', n)
    start = time.time()
    try:
        time.sleep(n)
    except Exception as e:
        logging.exception(e)
    logging.info('end sleep %s seconds, spend %s', n, time.time() - start)

测试：

::

    $ python time_c.py &
    [1] 6390
    2017-07-16 16:09:31,340 - INFO - start sleep 60 seconds

    $ kill -s SIGHUP 6390
    2017-07-16 16:09:35,328 - INFO - recived 1
    2017-07-16 16:09:35,329 - ERROR - test
    Traceback (most recent call last):
      File "time_c.py", line 21, in <module>
        time.sleep(n)
      File "time_c.py", line 14, in handler
        raise Exception('test')
    Exception: test
    2017-07-16 16:09:35,329 - INFO - end sleep 60 seconds, spend 3.988664150238037
    [1]+  Done                    python time_c.py

可以看到，当 signal handler 抛异常时， ``time.sleep`` 会抛出异常提前终止 sleep 操作。

下面来测试 Python 3.5+ 下这四种情况的行为。

Python 3.5+
-----------

普通 sleep 程序
~~~~~~~~~~~~~~~

用的还是之前的 time\_a.py 文件，测试结果：

::

    $ python3.6 time_a.py
    2017-07-16 16:12:28,566 - INFO - start sleep 60 seconds
    2017-07-16 16:13:28,571 - INFO - end sleep 60 seconds, spend 60.00386714935303

可以看到，跟 Python 2 一样，正常 sleep.

signal
~~~~~~

同样试试给 time\_a.py 进程发送 signal:

::

    $ python3.6 time_a.py  &
    [1] 6790
    $ 2017-07-16 16:15:53,529 - INFO - start sleep 60 seconds

    $ kill -s SIGHUP 6790
    [1]+  Hangup: 1               python3.6 time_a.py

跟 Python 2 下也是一样，进程终止。

signal handler
~~~~~~~~~~~~~~

按照文档，当 signal handler 不错误的时候，应该可以正常 sleep,
下面我们试试看：

::

    $ python3.6 time_b.py &
    [1] 6848
    $ 2017-07-16 16:17:25,144 - INFO - start sleep 60 seconds

    $ kill -s SIGHUP 6848
    2017-07-16 16:17:31,252 - INFO - recived 1
    $ jobs
    [1]+  Running                 python3.6 time_b.py &
    $ 2017-07-16 16:18:25,147 - INFO - end sleep 60 seconds, spend 60.00310564041138

    [1]+  Done                    python3.6 time_b.py

确实跟文档中说的一样，就算收到并处理了 signal 还是可以正常 sleep 。👍

下面再看看 signal handler raise exception 的情况。

signal handler raise exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

测试：

::

    $ python3.6 time_c.py &
    [1] 42908
    2017-07-16 16:20:00,679 - INFO - start sleep 60 seconds

    $ kill -s SIGHUP 42908
    2017-07-16 16:20:06,126 - INFO - recived 1
    2017-07-16 16:20:06,126 - ERROR - test
    Traceback (most recent call last):
      File "time_c.py", line 21, in <module>
        time.sleep(n)
      File "time_c.py", line 14, in handler
        raise Exception('test')
    Exception: test
    2017-07-16 16:20:06,127 - INFO - end sleep 60 seconds, spend 5.4475321769714355
    [1]+  Done                    python3.6 time_c.py

可以看到，跟在 Python 2 下一样，当 signal handler
抛异常时，``time.sleep`` 会抛出异常提前终止 sleep 操作。

原因
----

那么，为什么 Python 2 下 ``time.sleep`` 遇到 signal
时会出现提前返回的情况呢？

在 gevent 的一个 `issue <https://github.com/gevent/gevent/issues/280>`__
中 `@jamadden <https://github.com/jamadden>`__ 是 `这样解释的 <https://github.com/gevent/gevent/issues/280#issuecomment-120123286>`__ :

    The stdlib **time.sleep** method is implemented by calling **select**,
    passing in a timeout value, and no file descriptors to actually
    select on. The intended effect is to block in the operating system,
    sleeping until the timeout has elapsed.

    However, **select** is one of those system calls that is vulnerable to
    signals. When a signal is delivered to the process, **select**
    prematurely wakes up and sets **errno** to **EINTR** (interrupted). In that
    case, **time.sleep** makes no attempt to account for any unelapsed time;
    it simple returns. Therefore, **time.sleep** can sometimes return early.
    `This is
    documented <https://docs.python.org/3/library/time.html#time.sleep>`__.

查看 python 2.7 的源代码以及 ``select`` 的文档可以确认这个解释：

python 2.7 源码中 ``time.sleep`` 的
`实现片段 <https://github.com/python/cpython/blob/2.7/Modules/timemodule.c#L937>`__
如下：

.. code-block:: c


    static int

    floatsleep(double secs)

    {
    /* XXX Should test for MS_WINDOWS first! */
    #if defined(HAVE_SELECT) && !defined(__BEOS__) && !defined(__EMX__)
        struct timeval t;
        double frac;
        frac = fmod(secs, 1.0);
        secs = floor(secs);
        t.tv_sec = (long)secs;
        t.tv_usec = (long)(frac*1000000.0);
        Py_BEGIN_ALLOW_THREADS
        if (select(0, (fd_set *)0, (fd_set *)0, (fd_set *)0, &t) != 0) {
    #ifdef EINTR
            if (errno != EINTR) {
    #else
            if (1) {
    #endif
                Py_BLOCK_THREADS
                PyErr_SetFromErrno(PyExc_IOError);
                return -1;
            }
        }


可以看到确实是用 ``select`` 来实现的 ``time.sleep`` 。

``select`` 的
`文档 <http://man7.org/linux/man-pages/man2/select.2.html>`__ 中关于
signal 的说明如下：


       The **timeout** argument specifies the interval that **select()** should
       block waiting for a file descriptor to become ready.  **The call will
       block until either**:

       *  a file descriptor becomes ready;

       *  **the call is interrupted by a signal handler**; or

       *  the timeout expires.

通过文档我们知道， ``select`` 的 **timeout** 的阻塞效果确实会被 signal handler 所中断。

至于 Python 3.5+ 为什么不会提前返回，是因为它的 ``time.sleep``
实现中对于这种情况增加了判断，\ `如果时间没到会用剩下的时间再次
sleep <https://github.com/python/cpython/blob/3.6/Modules/timemodule.c#L1482-L1487>`__\ ：

.. code-block:: c

    static int
    pysleep(_PyTime_t secs)
    {
         // ...
         do {
            // ...
            monotonic = _PyTime_GetMonotonicClock();
            secs = deadline - monotonic;
            if (secs < 0)
                break;
            /* retry with the recomputed delay */
        } while (1);

        return 0;
    }

启示
----

如果想在 Python 2 下实现类似 Python 3.5+ 下的效果，可以仿照 Python 3.5+
下的实现增加“如果时间没到会用剩下的时间再次 sleep”的逻辑：

参考代码（修改自 time\_b.py）

.. code-block:: python

    $ cat time_d.py
    import logging
    import signal
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(levelname)s - %(message)s'
    )

    n = 60


    def handler(sig, strace):
        logging.info('recived %s', sig)


    signal.signal(signal.SIGHUP, handler)

    logging.info('start sleep %s seconds', n)
    start = time.time()
    remain = n
    while True:
        time.sleep(remain)
        remain = (start + n) - time.time()
        if remain < 0:
            break
        else:
            logging.warn('retry sleep %s', remain)
    logging.info('end sleep %s seconds, spend %s', n, time.time() - start)

测试：

::

    $ python time_d.py &
    [1] 14751
    $ 2017-07-16 17:10:53,235 - INFO - start sleep 60 seconds

    $ kill -s SIGHUP 14751
    2017-07-16 17:10:59,803 - INFO - recived 1
    2017-07-16 17:10:59,803 - WARNING - retry sleep 53.4323399067

    $ kill -s SIGHUP 14751
    2017-07-16 17:11:44,792 - INFO - recived 1
    2017-07-16 17:11:44,792 - WARNING - retry sleep 8.44309687614
    $ 2017-07-16 17:11:53,239 - INFO - end sleep 60 seconds, spend 60.0035960674

    [1]+  Done                    python time_d.py

**最重要的一点是** ：不要觉得 ``time.sleep``
会非常的精确，它有可能变快也有可能变慢，不要对它有过高的期望，不要依赖这个功能来实现需要精确
sleep 的需求。

目测可能也可以利用 python 2 下的这一行为实现一些特殊的需求。


好了，本文的内容就是这些了，希望这篇文章能对你有所帮助。

参考资料
--------

-  `15.3. time — Time access and conversions — Python 2.7.13
   documentation <https://docs.python.org/2/library/time.html#time.sleep>`__
-  `16.3. time — Time access and conversions — Python 3.6.2rc2
   documentation <https://docs.python.org/3/library/time.html#time.sleep>`__
-  `gevent.subprocess.Popen alters the behavior of time.sleep · Issue
   #280 · gevent/gevent <https://github.com/gevent/gevent/issues/280>`__
-  `cpython/timemodule.c at 2.7 ·
   python/cpython <https://github.com/python/cpython/blob/2.7/Modules/timemodule.c#L937>`__
-  `cpython/timemodule.c at 3.6 ·
   python/cpython <https://github.com/python/cpython/blob/3.6/Modules/timemodule.c#L1482-L1487>`__
