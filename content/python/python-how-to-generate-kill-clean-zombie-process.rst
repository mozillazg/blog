Python: 僵尸进程的产生和清除方法
====================================

:slug: python-how-to-generate-kill-clean-zombie-process
:date: 2017-07-20
:tags: process, zombie


僵尸进程产生的原因
------------------

在 unix 或 unix-like
的系统中，当一个子进程退出后，它就会变成一个僵尸进程，如果父进程没有通过
``wait``
系统调用来读取这个子进程的退出状态的话，这个子进程就会一直维持僵尸进程状态。

`Zombie process -
Wikipedia <https://en.wikipedia.org/wiki/Zombie_process>`__
中是这样描述的：

    On Unix and Unix-like computer operating systems, a zombie process
    or defunct process is a process that has completed execution (via
    the exit system call) but still has an entry in the process table:
    it is a process in the "Terminated state". This occurs for child
    processes, where the entry is still needed to allow the parent
    process to read its child's exit status: once the exit status is
    read via the wait system call, the zombie's entry is removed from
    the process table and it is said to be "reaped". A child process
    always first becomes a zombie before being removed from the resource
    table. In most cases, under normal system operation zombies are
    immediately waited on by their parent and then reaped by the system
    – processes that stay zombies for a long time are generally an error
    and cause a resource leak.

并且僵尸进程无法通过 ``kill`` 命令来清除。

本文将探讨如何手动制造一个僵尸进程以及清除僵尸进程的办法。

手动制造一个僵尸进程
--------------------

为了便于后面讲解清除僵尸进程的方法，我们使用日常开发中经常使用的
``multiprocessing``
模块来制造僵尸进程（准确的来说是制造一个长时间维持僵尸进程状态的子进程）：

.. code-block:: python

    $ cat test_a.py
    from multiprocessing import Process, current_process
    import logging
    import os
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(levelname)s - %(message)s'
    )


    def run():
        logging.info('exit child process %s', current_process().pid)
        os._exit(3)

    p = Process(target=run)
    p.start()
    time.sleep(100)

测试：

::

    $ python test_a.py &
    [1] 10091
    $ 2017-07-20 21:28:14,792 - INFO - exit child process 10106

    $ ps aux |grep 10106
    mozillazg              10126   0.0  0.0  2434836    740 s006  R+    0:00.00 grep 10106
    mozillazg              10106   0.0  0.0        0      0 s006  Z     0:00.00 (Python)

可以看到，子进程 ``10106`` 变成了僵尸进程。

既然已经可以控制僵尸进程的产生了，那我们就可以进入下一步如何清除僵尸进程了。

清除僵尸进程
------------

清除僵尸进程有两种方法：

-  第一种方法就是结束父进程（一般是主进程）。当父进程退出的时候僵尸进程随后也会被清除。
-  第二种方法就是通过 ``wait``
   调用来读取子进程退出状态。我们可以通过处理 ``SIGCHLD``
   信号，在处理程序中调用 ``wait`` 系统调用来清除僵尸进程。
-  第三种办法就说把进程变成孤儿进程，这样进程就会自动交由 init 进程（pid 为 1 的进程）来处理，一般 init 进程都包含对僵尸进程进行处理的逻辑。（这里有个坑，那就是 docker 容器中一般 pid 为 1 进程就是主程序的进程，而不是我们预期的 init 进程。如果要使用这种方法的话，需要注意一下类似的场景）

处理 SIGCHLD 信号
~~~~~~~~~~~~~~~~~~~~~

子进程退出时系统会向父进程发送 ``SIGCHLD`` 信号，父进程可以通过注册
``SIGCHLD`` 信号处理程序，在信号处理程序中调用 ``wait``
系统调用来清理僵尸进程。

.. code-block:: python

    $ cat test_b.py
    import errno
    from multiprocessing import Process, current_process
    import logging
    import os
    import signal
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(levelname)s - %(message)s'
    )


    def run():
        exitcode = 3
        logging.info('exit child process %s with exitcode %s',
                     current_process().pid, exitcode)
        os._exit(exitcode)


    def wait_child(signum, frame):
        logging.info('receive SIGCHLD')
        try:
            while True:
                # -1 表示任意子进程
                # os.WNOHANG 表示如果没有可用的需要 wait 退出状态的子进程，立即返回不阻塞
                cpid, status = os.waitpid(-1, os.WNOHANG)
                if cpid == 0:
                    logging.info('no child process was immediately available')
                    break
                exitcode = status >> 8
                logging.info('child process %s exit with exitcode %s', cpid, exitcode)
        except OSError as e:
            if e.errno == errno.ECHILD:
                logging.warning('current process has no existing unwaited-for child processes.')
            else:
                raise
        logging.info('handle SIGCHLD end')

    signal.signal(signal.SIGCHLD, wait_child)

    p = Process(target=run)
    p.start()

    while True:
        time.sleep(100)

效果：

::

    $ python test_b.py  &
    [1] 10159
    $ 2017-07-20 21:28:56,085 - INFO - exit child process 10174 with exitcode 3
    2017-07-20 21:28:56,088 - INFO - receive SIGCHLD
    2017-07-20 21:28:56,089 - INFO - child process 10174 exit with exitcode 3
    2017-07-20 21:28:56,090 - WARNING - current process has no existing unwaited-for child processes.
    2017-07-20 21:28:56,090 - INFO - handle SIGCHLD end

    $ ps aux |grep 10174
    mozillazg              10194   0.0  0.0  2432788    556 s006  R+    0:00.00 grep 10174

可以看到，子进程退出变成僵尸进程后，系统给父进程发送了 ``SIGCHLD``
信号，我们在 ``SIGCHLD`` 信号的处理程序中通过 ``os.waitpid`` 调用
``wait``
系统调用后阻止了子进程一直处于僵尸进程状态，从而实现了清除僵尸进程的效果。


把进程变成孤儿进程
~~~~~~~~~~~~~~~~~~~~~

什么是孤儿进程：当父进程已经退出但是子进程仍旧在运行时，这个子进程就变成了孤儿进程。
系统会把孤儿进程的父进程设置为 init 进程，将由 init 进程来管理这个孤儿进程。

我们修改一下前面的程序，改成由子进程的子进程来执行具体逻辑：

.. code-block:: python

    $ cat test_c.py
    from multiprocessing import Process, current_process
    import logging
    import os
    import time

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(levelname)s - %(message)s'
    )


    def run():
        time.sleep(30)
        logging.info('exit grandchild process %s', current_process().pid)
        os._exit(3)


    def worker():
        p = Process(target=run)
        p.start()
        logging.info('exit worker process %s, grandchild is %s',
                     current_process().pid, p.pid)
        os._exit(1)


    p = Process(target=worker)
    p.start()
    p.join()
    time.sleep(100)


效果:

::


    $ python test_c.py &
    [1] 79565
    2017-07-30 18:18:27,680 - INFO - exit worker process 79585, grandchild is 79586

    $ ps -f |grep test_c.py
      mozillazg 79565 62003   0  6:18PM ttys009    0:00.06 python test_c.py
      mozillazg 79586     1   0  6:18PM ttys009    0:00.00 python test_c.py
      mozillazg 79611 62003   0  6:18PM ttys009    0:00.00 grep test_c.py

    $ 2017-07-30 18:18:57,681 - INFO - exit grandchild process 79586

    $ ps -f |grep 79586
      mozillazg 79697 62003   0  6:19PM ttys009    0:00.00 grep 79586

    $ ps -f |grep test_c.py
      mozillazg 79565 62003   0  6:18PM ttys009    0:00.06 python test_c.py
      mozillazg 79741 62003   0  6:19PM ttys009    0:00.00 grep test_c.py


可以看到当结束了进程 ``79585`` 之后，它的子进程 ``79586`` 的父进程的 pid 就变成了 ``1`` ，
随后退出 ``79586`` 进程后，进程 ``79586`` 并没有出现一直维持僵尸进程状态的情况。



结语
----

希望本文能对你有所帮助。

参考资料
--------
-  `16.1. os — Miscellaneous operating system interfaces — Python 3.6.2
   documentation <https://docs.python.org/3/library/os.html#os._exit>`__
-  `16.1. os — Miscellaneous operating system interfaces — Python 3.6.2
   documentation <https://docs.python.org/3/library/os.html#os.waitpid>`__
-  `waitpid(3) - Linux man page <https://linux.die.net/man/3/waitpid>`__
-  `IBM Knowledgecenter - waitpid()--Wait for Specific Child
   Process <https://www.ibm.com/support/knowledgecenter/ssw_i5_54/apis/waitpid.htm>`__
-  `gunicorn/arbiter.py at 19.7.1 ·
   benoitc/gunicorn <https://github.com/benoitc/gunicorn/blob/19.7.1/gunicorn/arbiter.py#L506>`__
-  `cpython/forkserver.py at 13e96cc596d158b98996db3fa291086ea4afecd9 ·
   python/cpython <https://github.com/python/cpython/blob/13e96cc596d158b98996db3fa291086ea4afecd9/Lib/multiprocessing/forkserver.py#L198-L223>`__
-  `深入浅出---unix多进程编程之wait()和waitpid()函数 - wintree的专栏 -
   CSDN博客 <http://blog.csdn.net/wallwind/article/details/6998602>`__
-  `Zombie process - Wikipedia <https://en.wikipedia.org/wiki/Zombie_process>`__
- `Orphan process - Wikipedia <https://en.wikipedia.org/wiki/Orphan_process>`__
