tinyq: 一个队列框架
=================================================
:slug: tinyq-a-queue-framework
:date: 2017-04-10
:tags: framework, queue

最近尝试着写了一个简单的队列框架，整体的功能类似 celery, rq 之类的队列框架。
下面简单的介绍一下。


安装
--------

| 项目地址： https://github.com/mozillazg/tinyq
| 安装：

::

    pip install tinyq

这个框架使用 redis 作为队列服务，所以同时也需要安装 redis 服务程序。


Hello World
--------------

1. 启动 redis 服务: ::

   $ redis-server

2. 增加一个 app.py 文件: ::

    from tinyq import Application

    app = Application()


    @app.task()
    def add(m, n):
        return m + n


3. 通过 python shell 增加几个 delay job: ::

       from app import app

       for m in range(10):
        for n in range(3):
            add.delay(m, n)

4. 启动 worker 消费队列中的 job: ::

    $ tinyq -l info
    2017-03-12 21:27:12,322 - WARNING - tinyq.runner[line:73 thread:MainThread(140736379601856) process:MainProcess(15388)] - Starting TinyQ worker, version 0.1.0...
    2017-03-12 21:27:12,446 - INFO - tinyq.worker[line:65 thread:Worker-2(123145554059264) process:MainProcess(15388)] - Got a job: <Job: id: 9687d9dd-30f4-4920-bd0c-924e672d9794, task_name: add>
    2017-03-12 21:27:12,447 - INFO - tinyq.worker[line:67 thread:Worker-2(123145554059264) process:MainProcess(15388)] - Finish run job <Job: id: 9687d9dd-30f4-4920-bd0c-924e672d9794, task_name: add>
    2017-03-12 21:27:12,500 - INFO - tinyq.worker[line:65 thread:Worker-5(123145569824768) process:MainProcess(15388)] - Got a job: <Job: id: 315f4ead-cedb-4b7a-b3c6-d328b0152e35, task_name: add>
    2017-03-12 21:27:12,501 - INFO - tinyq.worker[line:67 thread:Worker-5(123145569824768) process:MainProcess(15388)] - Finish run job <Job: id: 315f4ead-cedb-4b7a-b3c6-d328b0152e35, task_name: add>
    2017-03-12 21:27:12,610 - INFO - tinyq.worker[line:65 thread:Worker-1(123145548804096) process:MainProcess(15388)] - Got a job: <Job: id: a014ee87-0200-4b78-af25-6fe8dcca3f14, task_name: add>
    2017-03-12 21:27:12,610 - INFO - tinyq.worker[line:67 thread:Worker-1(123145548804096) process:MainProcess(15388)] - Finish run job <Job: id: a014ee87-0200-4b78-af25-6fe8dcca3f14, task_name: add>
    ^C2017-03-12 21:27:13,863 - WARNING - tinyq.runner[line:144 thread:MainThread(140736379601856) process:MainProcess(15388)] - Received stop signal, warm shutdown...
    2017-03-12 21:27:13,886 - WARNING - tinyq.runner[line:135 thread:Worker-2(123145554059264) process:MainProcess(15388)] - Exit worker Worker-2.
    2017-03-12 21:27:13,896 - WARNING - tinyq.runner[line:135 thread:Worker-7(123145580335104) process:MainProcess(15388)] - Exit worker Worker-7.
    2017-03-12 21:27:13,906 - WARNING - tinyq.runner[line:135 thread:Scheduler(123145538293760) process:MainProcess(15388)] - Exit worker Scheduler.
    2017-03-12 21:27:13,924 - WARNING - tinyq.runner[line:135 thread:Worker-5(123145569824768) process:MainProcess(15388)] - Exit worker Worker-5.
    2017-03-12 21:27:13,936 - WARNING - tinyq.runner[line:135 thread:Worker-0(123145543548928) process:MainProcess(15388)] - Exit worker Worker-0.
    2017-03-12 21:27:13,956 - WARNING - tinyq.runner[line:135 thread:Worker-4(123145564569600) process:MainProcess(15388)] - Exit worker Worker-4.
    2017-03-12 21:27:13,978 - WARNING - tinyq.runner[line:135 thread:Worker-6(123145575079936) process:MainProcess(15388)] - Exit worker Worker-6.
    2017-03-12 21:27:14,017 - WARNING - tinyq.runner[line:135 thread:Worker-1(123145548804096) process:MainProcess(15388)] - Exit worker Worker-1.
    2017-03-12 21:27:14,068 - WARNING - tinyq.runner[line:135 thread:Worker-3(123145559314432) process:MainProcess(15388)] - Exit worker Worker-3.
    2017-03-12 21:27:14,068 - WARNING - tinyq.runner[line:101 thread:MainThread(140736379601856) process:MainProcess(15388)] - Exit workers.
    $


功能
-------

通过上面的 Hello World 示例可以看出 tinyq 的功能类似 rq/celery。
还有一些 Hello World 中没有展示出来的功能:

* ``app = Application()``, 可以给 ``Application`` 传递一个参数来指定 redis 配置:
  ``app = Application('redis://192.168.99.100:2375/1')``
* app.py 也可以叫其他的名字，只要在启动 worker 的时候指定 ``--app`` 参数就可以了。
  比如有如下文件: ::

    $ cat test/hello.py

      tinyq_app = Application()

  那么 ``--app`` 参数的值就是 ``test.hello.tinyq_app`` ，
  关键点是告诉 worker ``Application`` 实例所在位置

* 装饰器 ``@app.task()`` 还有个 ``name`` 参数，用于指定 task 的名称（默认是被装饰的函数的名称）
* 既可以通过 ``add.delay`` 把操作放到队列中，也可以通过 ``add(m, n)`` 立即执行操作
* 通过 control + c 退出 worker 时会等待正在处理的 job 全部完成后再退出
* worker 还支持其他参数: ::

    $ tinyq -h
    usage: tinyq [-h] [-V] [-u URI] [-v] [-w WORKER_NUMBER] [-a APP]
                 [-l {debug,info,warn,error,critical}]

    Starts a TinyQ worker.

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -u URI, --uri URI     The Redis URI (default: redis://)
      -v, --verbose         Show more output
      -w WORKER_NUMBER, --worker-number WORKER_NUMBER
                            Worker number (default: 8)
      -a APP, --app APP     Application path (default: app.app)
      -l {debug,info,warn,error,critical}, --log-level {debug,info,warn,error,critical}
                            Logging level (default: warn)


That's all.
