
让我们一起来构建一个 Web 服务器（三）
================================================================

:slug: let-us-build-a-web-server-part-3-zh-cn
:date: 2015-08-04
:modified: 2015-08-27
:tags: server, http, fork, lsbaws


本文译自： http://ruslanspivak.com/lsbaws-part3/


    “当我们必须要发明创造的时候学到的东西最多” —— Piaget


在 `第二部分`_ 你创建了一个能够处理基本的 GET 请求的微型 WSGI 服务器。
同时我向你提了一个问题，“如何才能让你的服务器在同一时刻能够处理多个请求？”
在本篇文章中你可以找到答案。那么，系好安全带，加足马力吧。
你将会有一趟非常快速的旅程。
确保你已经准备好了你的 Linux, Mac OS X （或任一 \*nix 系统）以及 Python 。
本文所有的源代码都已经放在 `Github <https://github.com/rspivak/lsbaws/blob/master/part3/>`__ 上了。


首先，让我们来回顾一下一个非常基础的 Web 服务器看起来是啥样的，
以及这个服务器需要做些什么才能服务来自客户端的请求。
你在 `第一部分`_ 和 `第二部分`_ 创建的服务器是个一次只能处理一个客户端请求的循环服务器。
在它处理完正在处理的客户端请求之前，它是无法接受新的连接的。
一些客户端可能会不高兴，因为它们必须得排队等待，
对于那些非常繁忙的服务器，这个等待可能会是个非常漫长的过程。

|lsbaws_part3_it1.png|



下面是循环服务器 `webserver3a.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3a.py>`__ 代码:

.. code-block:: python

    #####################################################################
    # Iterative server - webserver3a.py                                 #
    #                                                                   #
    # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X  #
    #####################################################################
    import socket

    SERVER_ADDRESS = (HOST, PORT) = '', 8888
    REQUEST_QUEUE_SIZE = 5


    def handle_request(client_connection):
        request = client_connection.recv(1024)
        print(request.decode())
        http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """
        client_connection.sendall(http_response)


    def serve_forever():
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(SERVER_ADDRESS)
        listen_socket.listen(REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port} ...'.format(port=PORT))

        while True:
            client_connection, client_address = listen_socket.accept()
            handle_request(client_connection)
            client_connection.close()

    if __name__ == '__main__':
        serve_forever()


为了观察你的服务器一次只能处理一个客户端请求的现象，
服务器代码需要做一点修改，在发送响应信息给客户端后的地方增加了
一个 60 秒的延时。这一行的更改是为了告诉服务器进程需要休息 60 秒。

|lsbaws_part3_it2.png|


下面是包含休息代码的服务器代码 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__ :

.. code-block:: python


        #########################################################################
        # Iterative server - webserver3b.py                                     #
        #                                                                       #
        # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X      #
        #                                                                       #
        # - Server sleeps for 60 seconds after sending a response to a client   #
        #########################################################################
        import socket
        import time

        SERVER_ADDRESS = (HOST, PORT) = '', 8888
        REQUEST_QUEUE_SIZE = 5


        def handle_request(client_connection):
            request = client_connection.recv(1024)
            print(request.decode())
            http_response = b"""\
        HTTP/1.1 200 OK

        Hello, World!
        """
            client_connection.sendall(http_response)
            time.sleep(60)  # sleep and block the process for 60 seconds


        def serve_forever():
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listen_socket.bind(SERVER_ADDRESS)
            listen_socket.listen(REQUEST_QUEUE_SIZE)
            print('Serving HTTP on port {port} ...'.format(port=PORT))

            while True:
                client_connection, client_address = listen_socket.accept()
                handle_request(client_connection)
                client_connection.close()

        if __name__ == '__main__':
            serve_forever()


用以下方式启动服务器： ::

    $ python webserver3b.py



现在打开一个新的终端窗口，然后执行 ``curl`` 命令。
你应该会看到屏幕上打印了 "Hello, World!" 字符串： ::

    $ curl http://localhost:8888/hello
    Hello, World!

然后立即打开第二个终端窗口并执行相同的 ``curl`` 命令： ::

    $ curl http://localhost:8888/hello

如果你在 60 秒内做完了这些操作的话，第二个 ``curl`` 应该不会立马
输出任何的的信息，只是会阻塞在那里。
服务器应该也没有在它的标准输出中答应新的请求 body 信息。
下面是这种现象在我的 Mac 电脑上的样子（右下角用黄色高亮的窗口显示第二个 ``curl`` 命令阻塞了，
正在等待连接能够被服务器接受）： 

|lsbaws_part3_it3.png|

在你等了足够长的时间后（大于 60 秒）你应该会看到第一个 ``curl``  结束
以及第二个 ``curl`` 在屏幕上打印了 "Hello, World!"，然后阻塞 60 秒，之后再结束： 

|lsbaws_part3_it4.png|

它的工作方式是，服务器完成对第一个 ``curl`` 客户端的请求后，只有等它休息完 60 秒之后才会
开始处理第二个请求。这将导致出现顺序，或一步一步的循环，或在这里是一次只能处理一个客户端请求。


让我们抽出一点时间来说一下关于客户端和服务器之间的通信方面的东西。
为了让两个程序能够在网络进行中进行通信，它们需要使用套接字（socket）。
你已经在 `第一部分`_ 和 `第二部分`_ 中见过 socket 了。但是什么是一个 socket 呢？

|lsbaws_part3_it_socket.png|


一个 socket 是一个通信端点的抽象概念，
它允许你的程序通过文件描述与另一个程序进行通信。
在这篇文章中，我会特别讲述在 Linux/Mac OS X 上的  TCP/IP socket。
需要理解一个重要的概念，那就是 TCP socket 对。


    一个 TCP 连接的 socket 对是一个 4 元组，这个元组标识了一个 TCP 连接的两个端点：
    本地 IP 地址，本地端口，远程 IP 地址，以及远程端口。
    一个套接字对唯一标识了网络上每个 TCP 连接。
    一个 IP 地址和一个端口号这个两个值标识了每个端点，通常被叫做一个套接字。 [1]_


|lsbaws_part3_it_socketpair.png|


因此，元组 ``{10.10.10.2:49152, 12.12.12.3:8888}`` 是一个套接字对，它唯一标识了
客户端 上的一个 TCP 连接的两个端点。
元组 ``{12.12.12.3:8888, 10.10.10.2:49152}`` 是一个套接字对，它唯一标识了
服务端 上的一个 TCP 连接的两个端点。这个两个值标识了一个 TCP 连接的服务端端点，
IP 地址 12.12.12.3 和端口 8888 在这里被归为一个套接字（客户端端点有相同的应用）。


一个服务器通常通过创建一个套接字,然后开始接受来自客户端的请求，它的常规顺序如下：


|lsbaws_part3_it_server_socket_sequence.png|


1. 服务器创建一个 TCP/IP socket。这个用的是下面的 Python 语句来实现的： ::

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


2. 服务器可能会设置一些 socket 选项（这是可选的，但是你能在上面的服务器代码中看到它,只是为了在你决定杀死或重启服务器的时候能够立即就可以一遍又一遍的重复使用相同的地址）。::

    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

3. 然后，服务器绑定这个地址. ``bind`` 函数在 socket 上分配一个本地协议地址。对于 TCP 则是，调用 ``bind`` 让你指定一个端口号，一个 IP 地址，这两个都要或都不需要指定。::

    listen_socket.bind(SERVER_ADDRESS)

4. 然后，服务器把这个 socket 设定为一个监听 socket ::

    listen_socket.listen(REQUEST_QUEUE_SIZE)


这个 ``listen`` 方法只需要在服务器端进行调用。
它告诉内核，它应该接受目标为这个 socket 的接入连接请求。


这样做以后，服务器就开始在一个循环内一次接受来自一个客户端的连接。
当有一个可用的连接的时候， ``accept`` 调用返回连接的客户端的套接字。
然后，服务器从这个连接的客户端的套接字中读取请求数据，
在它的标准输出上答应这个数据，然后给客户端发送回一条消息。
然后，服务器关闭了这个客户端连接，它准备再次开始接受来的新客户端的连接。


下面是一个客户端与服务器通过 TCP/IP 进行通信需要做的事情：

|lsbaws_part3_it_client_socket_sequence.png|


下面是客户端连接你的服务器，发送一个请求然后答应响应的一段示例代码：

.. code-block:: python

     import socket

     # create a socket and connect to a server
     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     sock.connect(('localhost', 8888))

     # send and receive some data
     sock.sendall(b'test')
     data = sock.recv(1024)
     print(data.decode())


创建完套接字后，客户端需要连接服务器. 可以通过调用 ``connect`` 实现这个功能： ::

    sock.connect(('localhost', 8888))

客户端只需要提供想要连接的服务器的远程 IP 地址或主机名以及远程端口号就可以了。


你可能已经注意到了，客户端没有调用 ``bind``  和 ``accept``。
客户不需要调用 ``bind`` 是因为客户端不关系本地 IP 地址和本地端口号。
当客户端调用 ``connect`` 时，内核里的 TCP/IP 协议栈会分配本地 IP 地址和本地端口号。
这个本地端口叫做 **临时端口** 或者 短命端口 :)。

|lsbaws_part3_it_ephemeral_port.png|



服务器上的端口标识了一个知名(well-know)服务，客户端连接的端口叫做一个知名端口（比如，HTTP 的 80 端口， SSH 的 22 端口）。
起一个 Python shell 然后发起一个到你本地运行的服务器的客户端连接，
然后查看为你创建的套接字分配了什么样的临时端口（在尝试下面的例子前需要先启动服务器 `webserver3a.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3a.py>`__ 或 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__ ）： ::

    >>> import socket
    >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    >>> sock.connect(('localhost', 8888))
    >>> host, port = sock.getsockname()[:2]
    >>> host, port
    ('127.0.0.1', 60589)


在上面的例子中，内核给那个套接字分配了一个临时端口 60589。


在回答 `第二部分`_ 的问题前我还需要快速讲一下其他一些重要的概念。
你很快就会看到为什么它们是重要的。
这两个概念是 *进程* 和 *文件描述符* 。


什么是进程？一个进程只是一个正在执行的程序的实例。
比如说，当服务器代码被执行的时候，它被加载到内存里，然后这个正在执行的程序的实例就叫做进程。
内核记录了有关这个进程的一大串的信息—— 比如进程的 ID ——为了方便跟踪这个进程。
当你运行你的循环服务器 `webserver3a.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3a.py>`__ 或 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__ 的时候，你只是运行了一个进程。

|lsbaws_part3_it_server_process.png|



在终端窗口中启动服务器 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__  : ::

    $ python webserver3b.py



在另一个不同的终端窗口中使用 ``ps`` 命令来获取刚才那个进程的一些信息: ::

    $ ps | grep webserver3b | grep -v grep
    7182 ttys003    0:00.04 python webserver3b.py


``ps`` 命令告诉你你确实只是运行了一个 Python 进程 webserver3b 。
当一个进程被创建的时候，内核给它分配了一个进程 ID, PID。
在 UNIX 中，每个用户进程同时也有一个父进程，这个进程有它自己的进程 ID 叫做父进程 ID 或缩写为 PPID。
一般情况下，我假定你运行了一个 BASH shell ，然后当你启用服务器的时候，
一个新的进程被创建并且有一个 PID，同时它的父 PID 其实就是那个 BASH shel 的 PID。

|lsbaws_part3_it_ppid_pid.png|


亲自试一下，然后看看具体是什么情况。
再次启动你的 Python shell ，这将创建一个新的进程，
然后通过调用 `os.getpid() <https://docs.python.org/2.7/library/os.html#os.getpid>`__ 和 `os.getppid() <https://docs.python.org/2.7/library/os.html#os.getppid>`__ 来获取这个  Python shell 进程的 PID 和父 PID（你的 BASH shell 的 PID）。
然后在另一个终端窗口中运行 ``ps`` 和 ``grep`` 命令来获取 PPID（父进程 ID，在我的这里是 3148）。
在下面的截图中你可以看到一个父子关系的例子，
它展示的是在我的 Mac OS X 机器上子 Python shell 进程与父 BASH shell 进程之间的父子关系：

|lsbaws_part3_it_pid_ppid_screenshot.png|


另一个非常重要并且需要了解的概念是 **文件描述符** 。
那么，什么是文件描述符呢？
一个文件描述符是一个正整数，
当一个进程打开一个存在的文件，创建一个新文件或创建一个新的套接字的时候，内核返回一个正整数给进程，这个正整数就是文件描述符。
你可能听说过，在 UNIX 中一切皆文件。
内核通过文件描述符来索引一个进程打开的文件。
当你需要读或写一个文件时，你需要用文件描述符来标记它。
Python 给了你一些更高级别的对象用来处理文件（和套接字），
你不需要使用文件描述符来标识一个文件。
下面展示了在 Unix 中文件和套接字是如何被标识的：通过它们的整数文件描述符。


|lsbaws_part3_it_process_descriptors.png|



默认情况下，UNIX shell 给一个进程的标准输出分配的文件描述符是 0，
标准输入的文件描述符是 1，标准错误的文件描述符是 2。

|lsbaws_part3_it_default_descriptors.png|


正如我前面提到的，尽管 Python 给了你一个更高级别的文件或类文件对象用来进行操作，
你依然可以使用对象的 ``fileno()`` 方法来获取分配给这个文件的文件描述符。
返回到你的 Python shell 看看你怎样才能做到这样： ::

    >>> import sys
    >>> sys.stdin
    <open file '<stdin>', mode 'r' at 0x102beb0c0>
    >>> sys.stdin.fileno()
    0
    >>> sys.stdout.fileno()
    1
    >>> sys.stderr.fileno()
    2


当你在 Python 中处理文件和套接字的时候，你通常需要使用一个高级别的
file/socket 对象。
但是在这里你可能需要多次直接使用文件描述符。
下面的例子展示了你可以通过调用一个 `write <https://docs.python.org/2.7/library/os.html#os.write>`__ 系统并把文件描述符正数作为一个参数
的方式来写入一个字符串到标准输出： ::

    >>> import sys
    >>> import os
    >>> res = os.write(sys.stdout.fileno(), 'hello\n')
    hello


这里是个非常有意思的地方——这应该不会让你感到特别的惊讶，因为你已经知道在 UNIX
中万物皆文件——你的套接字也有一个分配给它的文件描述符。
在说一遍，当你在 Python 中创建一个套接字的时候，
你得到了一个对象和一个正整数，
你也可以通过直接访问我之前提过的 ``fileno()`` 方法的方式得到这个套接字的整数文件描述符。 ::

    >>> import socket
    >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    >>> sock.fileno()
    3

还有一件需要提及的事情是：在第二个例子中的循环服务器 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__ 中你已经知道了，当服务器进程正在休眠 60 秒的时候，你仍然能够用第二个 ``curl`` 命令连接服务器吗？当然可以，只是 ``curl`` 将不会立即输出任何信息，它只是会阻塞在那里。
但是，为什么当时服务器并没有在 ``accept`` 接受一个连接，而客户端却没有立即被拒绝连接，却依然能够连接服务器？
答案是套接字对象的 ``listen`` 方法以及它的  ``BACKLOG`` 参数，在代码里面我调用的是 ``REQUEST_QUEUE_SIZE`` 。 
``BACKLOG`` 参数指定了内核中接入连接请求的队列大小。   
当服务器 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__ 正在休眠的时候，你可以用第二个 ``curl`` 命令
连接服务器，是因为内核中用于该服务器套接字的接入连接请求队列还有足够的可用空间。


虽然加大 ``BACKLOG`` 参数的值并不能把你的服务器变成一个可以一次处理多个客户端请求的服务器，但是，对于非常繁忙的服务器来说，有一个足够大
的 backlog 参数是非常重要的，这样 ``accept`` 调用就不用等待有新的连接被建立，可以直接从队列中拿取新的连接，然后开始没有延时的处理这个客户端请求。



哇哦！你已经了解到很多知识了。让我们快速回顾一下你目前说学到的东西（
如果这些你都非常熟悉的话，那就再加深一下）。


|lsbaws_part3_checkpoint.png|


* 循环服务器
* 服务器 socket 创建顺序（socket, bind, listen, accept）
* 客户端链接创建顺序（socket, connect）
* 套接字对
* 套接字
* 临时端口和知名端口
* 进程
* 进程 ID（PID），父进程 ID（PPID），以及父子关系。
* 文件描述符
* ``listen`` socket 方法的 ``BACKLOG`` 参数的含义



现在，我已经准备号回答 `第二部分`_ 的问题了：“如何让你的服务器在同一时刻
处理多个请求？” 或者换一种方式“如何写一个并发服务器？”

|lsbaws_part3_conc2_service_clients.png|


在 Unix 下写一个并发服务器的最简单的方法是使用 `fork() <https://docs.python.org/2.7/library/os.html#os.fork>`__ 系统调用。

|lsbaws_part3_fork.png|


下面是一个新的并发服务器 `webserver3c.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3c.py>`__ 的代码，这个服务器能够同时处理多个客户端请求（同上一个服务器 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__ 一样，每个子进程都会休息 60 秒 ）：

|lsbaws_part3_it2.png|

.. code-block:: python

    ###########################################################################
    # Concurrent server - webserver3c.py                                      #
    #                                                                         #
    # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X        #
    #                                                                         #
    # - Child process sleeps for 60 seconds after handling a client's request #
    # - Parent and child processes close duplicate descriptors                #
    #                                                                         #
    ###########################################################################
    import os
    import socket
    import time

    SERVER_ADDRESS = (HOST, PORT) = '', 8888
    REQUEST_QUEUE_SIZE = 5


    def handle_request(client_connection):
        request = client_connection.recv(1024)
        print(
            'Child PID: {pid}. Parent PID {ppid}'.format(
                pid=os.getpid(),
                ppid=os.getppid(),
            )
        )
        print(request.decode())
        http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """
        client_connection.sendall(http_response)
        time.sleep(60)


    def serve_forever():
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(SERVER_ADDRESS)
        listen_socket.listen(REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port} ...'.format(port=PORT))
        print('Parent PID (PPID): {pid}\n'.format(pid=os.getpid()))

        while True:
            client_connection, client_address = listen_socket.accept()
            pid = os.fork()
            if pid == 0:  # child
                listen_socket.close()  # close child copy
                handle_request(client_connection)
                client_connection.close()
                os._exit(0)  # child exits here
            else:  # parent
                client_connection.close()  # close parent copy and loop over

    if __name__ == '__main__':
        serve_forever()


在深入讨论 fork 是如何工作前，先试一下吧，看看服务器是否真的能够同时处理多个客户端发送过来的请求，
而不是想它的同胞 `webserver3a.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3a.py>`__ 和 `webserver3b.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3b.py>`__ 那样无法处理。
在命令行下用以下命令启动服务器： ::

    $ python webserver3c.py


然后尝试你之前试过的那两条同样的命令，现在尽管服务器的子进程在服务了一个客户端请求后会休眠 60 秒，但是仍然不
影响其它的客户端，因为它们是由完全没有依赖的不同进程服务的。你可以看到你的 curl 命令立即输出了 “Hello, World!”，
然后卡住了 60 秒。你可以继续执行 n 条 curl 命令（嗯，差不多是你想执行多少就多少）所有的这些命令都将立即输出服务器的响应“Hello, World”，没有肉眼可见的延迟。试试吧。


为了理解 `fork() <https://docs.python.org/2.7/library/os.html#os.fork>`__ 有一点很长的重要那就是，你调用了一次 fork 但是它返回了两次：一次在父进程，一次在子进程。
当你 fork 一个新进程时，返回给子进程的进程 ID 是 0。当 fork 在父进程中返回时，它返回的是子进程的 PID。

|lsbaws_part3_conc2_how_fork_works.png|



我仍然记得当我第一次研究 fork 并尝试它的时候我有多么的着迷。它对我看起来就像魔法一样。

我当时正在阅读一段连续的代码，然后“嘭！”：那段代码克隆了它自己，现在同时运行了两个具有相同代码的实例。
我当时真的认为这就是魔法。


当一个父进程 fork 一个新的子进程时，子进程获得了一份父进程的文件描述符的拷贝：

|lsbaws_part3_conc2_shared_descriptors.png|


你可能已经看到了，在上面代码中父进程关闭了客户端连接： ::

    else:  # parent
        client_connection.close()  # close parent copy and loop over

如果父进程已经关掉了这个 socket 那么子进程是怎么做仍然可以从客户端 socet 中读取到数据呢？
答案就在上图总。内核使用描述符引用计数来决定是否需要关闭一个 socket。
只有当某个 socket 的描述符引用计数变成 0 的时候才会关闭这个 socket。
当你的服务器创建一个子进程的时候，子进程获得了父进程的文件描述符拷贝，内核将这些描述符的引用计数也相应的增加了。
在有一个父进程和一个子进程的情况下，关联者客户端 socket 的描述符引用计数就会是 2，
当父进程想在上面的代码中那样关闭了客户端 socket 链接的时候，引用计数就会减少变成 1，但是
仍然还没达到让内核关闭这个 socket 的条件。
子进程也需要关闭来自父进程监听的 socket 拷贝，因为子进程不关心接收新的客户端请求，
它只关心处理来自已建立连接的客户端连接： ::


    listen_socket.close()  # close child copy


我将会在稍后讲述如果你不关闭描述符副本时话会发生什么。


正如你在这个并发服务器源码中说发现的那样，服务器的父进程现在只有一个角色，那就是
接收一个新的客户端连接， fork 一个新的子进程用来处理这个请求，然后循环以便接收另一个客户端的连接，
没有其他多余的事情了。服务器的父进程不会处理客户端请求 —— 它的子进程会去处理。


说点额外的事情。当我们说两个事件是并发执行的时候，具体说的是什么意思呢？

|lsbaws_part3_conc2_concurrent_events.png|


当我们说两个事件是并发执行的时候，通常我们的意思是，它们是同时发生的。
简短的定义当然非常好，但是你也应该记住复杂的定义：


    如果你没法通过观察程序来知道哪个是先执行的，那么这两个事件就是并发执行的。[2]_

又到了概况你目前所学知识的时间了。


|lsbaws_part3_checkpoint.png|



* 在 Unix 下写并发服务器的最简单的方法是调用系统内的 `fork() <https://docs.python.org/2.7/library/os.html#os.fork>`__ 方法
* 当一个进程 fork 了一个新的进程的时候，它就变成了那个新 fork 的子进程的父进程。
* 在调用 fork 后父子进程共享相同的文件描述符。
* 内核使用描述符引用计数来决定是否需要关闭文件/socket 
* 服务器的父进程现在只有一个角色，那就是接收一个新的客户端连接， fork 一个新的子进程用来处理这个请求，然后循环以便接收另一个客户端的连接。



让我们来看一下，如果你没有在父子进程中关闭 socket 描述符副本会发生什么。
下面是一个修改版的并发服务器，它没有关闭描述符副本，
`webserver3d.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3d.py>`__ ：

.. code-block:: python

    ###########################################################################
    # Concurrent server - webserver3d.py                                      #
    #                                                                         #
    # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X        #
    ###########################################################################
    import os
    import socket

    SERVER_ADDRESS = (HOST, PORT) = '', 8888
    REQUEST_QUEUE_SIZE = 5


    def handle_request(client_connection):
        request = client_connection.recv(1024)
        http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """
        client_connection.sendall(http_response)


    def serve_forever():
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(SERVER_ADDRESS)
        listen_socket.listen(REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port} ...'.format(port=PORT))

        clients = []
        while True:
            client_connection, client_address = listen_socket.accept()
            # store the reference otherwise it's garbage collected
            # on the next loop run
            clients.append(client_connection)
            pid = os.fork()
            if pid == 0:  # child
                listen_socket.close()  # close child copy
                handle_request(client_connection)
                client_connection.close()
                os._exit(0)  # child exits here
            else:  # parent
                # client_connection.close()
                print(len(clients))

    if __name__ == '__main__':
        serve_forever()



用以下方式启动服务器： ::

    $ python webserver3d.py

使用 ``curl`` 命令来连接服务器： ::

    $ curl http://localhost:8888/hello
    Hello, World!


好了，curl 打印了来自并发服务器的响应，但是它并没有立即退出而是卡住那儿了。
发生什么事情了？服务器不再休息 60 了：它的子进程还在处理客户端请求，
关闭客户端连接然后退出，但是客户端 curl 仍然没有退出。

|lsbaws_part3_conc3_child_is_active.png|


那么，为什么 curl 没有退出呢？原因就是文件描述符副本。
当子进程关闭客户端连接的时候，内核减少了那个客户端 socket 的引用计数，此时计数变成了 1。
虽然服务器的子进程退出了，但是客户端 socket 并没有被内核关闭，因为此时该 socket 描述符的引用计数还不是 0，
结果终止包（在 TCP/IP 中被叫做 FIN）并没有被发送给客户端，可以说是客户端就会一直在线。
这里还有另外一个问题。如果你的长时间运行的服务器没有关闭文件描述符副本的话，
它最终将用尽所有可用的文件描述符：

|lsbaws_part3_conc3_out_of_descriptors.png|


使用 ctrl + c 停止你的服务器 `webserver3d.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3d.py>`__ ，然后通过在 shell 中输入内置的 ``ulimit`` 命令来查看服务器进程默认可用的资源： ::

    $ ulimit -a
    core file size          (blocks, -c) 0
    data seg size           (kbytes, -d) unlimited
    scheduling priority             (-e) 0
    file size               (blocks, -f) unlimited
    pending signals                 (-i) 3842
    max locked memory       (kbytes, -l) 64
    max memory size         (kbytes, -m) unlimited
    open files                      (-n) 1024
    pipe size            (512 bytes, -p) 8
    POSIX message queues     (bytes, -q) 819200
    real-time priority              (-r) 0
    stack size              (kbytes, -s) 8192
    cpu time               (seconds, -t) unlimited
    max user processes              (-u) 3842
    virtual memory          (kbytes, -v) unlimited
    file locks                      (-x) unlimited



正如你在上面看到的，服务器进程在我的 Ubuntu 上最大可打开的文件描述符（open files）数目是 1024。


现在我们来看一下如果你的服务器没有关闭描述符副本，它是怎么样用尽可用的文件描述符的。
在一个已有的或新开的终端窗口中，设置最大可打开的文件描述符数目为 256： ::

    $ ulimit -n 256


在你刚执行 ``$ ulimit -n 256`` 命令的那个终端中启动服务器 `webserver3d.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3d.py>`__ : ::

    $ python webserver3d.py


然后使用下面的客户端 `client3.py <https://github.com/rspivak/lsbaws/blob/master/part3/client3.py>`__ 测试这个服务器。

.. code-block:: python


    #####################################################################
    # Test client - client3.py                                          #
    #                                                                   #
    # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X  #
    #####################################################################
    import argparse
    import errno
    import os
    import socket


    SERVER_ADDRESS = 'localhost', 8888
    REQUEST = b"""\
    GET /hello HTTP/1.1
    Host: localhost:8888

    """


    def main(max_clients, max_conns):
        socks = []
        for client_num in range(max_clients):
            pid = os.fork()
            if pid == 0:
                for connection_num in range(max_conns):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(SERVER_ADDRESS)
                    sock.sendall(REQUEST)
                    socks.append(sock)
                    print(connection_num)
                    os._exit(0)


    if __name__ == '__main__':
        parser = argparse.ArgumentParser(
            description='Test client for LSBAWS.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            '--max-conns',
            type=int,
            default=1024,
            help='Maximum number of connections per client.'
        )
        parser.add_argument(
            '--max-clients',
            type=int,
            default=1,
            help='Maximum number of clients.'
        )
        args = parser.parse_args()
        main(args.max_clients, args.max_conns)



在一个新的终端窗口中，启动 `client3.py <https://github.com/rspivak/lsbaws/blob/master/part3/client3.py>`__ 并告诉它同时创建 300 个连接到服务器的连接： ::

    $ python client3.py --max-clients=300


很快你的服务器就会爆炸。下面是我机子上的异常信息的截图：

|lsbaws_part3_conc3_too_many_fds_exc.png|


教训已经非常清晰了——你的服务器应该关闭描述符副本。但是，就算你关闭了描述符副本，
你仍然还没有跳出丛林，因为你的服务器还有另一个问题，这个问题就是僵尸进程！

|lsbaws_part3_conc3_zombies.png|


是的，你的服务器代码实际上创建了一些僵尸进程。
让我们来看一下是怎么回事。再次启动你的服务器： ::

    $ python webserver3d.py


在另一个终端窗口中执行下面的 ``curl`` 命令： ::

    $ curl http://localhost:8888/hello


现在使用 ps 命令来显示正在运行的 Python 进程。
下面是我的 Ubuntu 上的 ``ps`` 命令输出： ::

    $ ps auxw | grep -i python | grep -v grep
    vagrant   9099  0.0  1.2  31804  6256 pts/0    S+   16:33   0:00 python webserver3d.py
    vagrant   9102  0.0  0.0      0     0 pts/0    Z+   16:33   0:00 [python] <defunct>


你有注意到第二行吗？上面说进程 PID 为 9102 的进程状态是 **Z+** ，进程名称是 **<defunct>** 。
这就是我们的僵尸进程了。僵尸进程的问题是你没法杀死它们。


|lsbaws_part3_conc3_kill_zombie.png|


就算你想尝试通过使用 ``$ kill -9`` 的方式来杀死僵尸进程也没有用，它们仍然能够活下来。你可以自己试试看。



僵尸进程究竟是什么呢？为什么我们的服务器会创建它们？
僵尸进程是指一个已经终止了的进程，但是它的父进程并没有等待它，也没有收到它的终止状态。
当一个子进程在它的父进程之前退出时，内核会把这个子进程转换为僵尸进程，同时存储该进程的一下信息方便它的父进程之后来恢复它。
存储的信息通常包括进程 ID,进程终止状态，以及进程的资源使用情况。
好的，因此僵尸进程服务一个特殊的目的，但是如果你的服务器没有照顾好这些僵尸进程的话，你的系统将会变得拥堵不堪。
让我们来看看这是怎么发生的。
首先，停止你正在运行的服务器，然后在一个新的终端窗口总，使用 ``ulimit`` 命令设置 max user processes 为 400（确保设置的 open files 足够高，也可以设置为 500）： ::


    $ ulimit -u 400$ ulimit -n 500


在你刚才输入 ``$ ulimit -u 400`` 命令的窗口启动 `webserver3d.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3d.py>`__  服务器： ::

    $ python webserver3d.py


在另一个新的终端窗口中，启动 `client3.py <https://github.com/rspivak/lsbaws/blob/master/part3/client3.py>`__ 并告诉它同时创建 500 个连接： ::

    $ python client3.py --max-clients=500


很快，你的服务器就会崩溃并抛出 ``OSError: Resource temporarily unavailable`` 的异常信息，
当它尝试创建一个新的子进程，但是却没法创建成功，因为它已经超出了允许创建的最大子进程数量。
下面是我机子上关于异常信息的截图：

|lsbaws_part3_conc3_resource_unavailable.png|

如你所见，如果你的长久运行的服务器不好好照看好僵尸进程的话，它们就会导致出现问题。
我将会简短的讨论一下服务器应该如何处理僵尸进程问题。


让我们来回顾一下你目前已经了解到的知识点：

|lsbaws_part3_checkpoint.png|

* 如果你没有关闭描述符副本，客户端将不会退出，因为客户端连接还没有被关闭。
* 如果你没有关闭描述符副本，你那长时间运行的服务器最终将耗尽所有可用的文件描述符（``max open files``）。
* 当你 fork 一个子进程然后退出，同时父进程没有等待( ``wait`` )子进程完成退出操作，父进程就收集不到子进程的退出状态，子进程最终就会变成一个僵尸进程。
* 僵尸是需要吃东西的。我咱们这里，它们吃内存。如果不管这些僵尸进程的话，你的服务器将最终耗尽所有可用的进程（``max user processes``）
* 你无法 ``kill`` 一个僵尸进程，你需要等( ``wait`` )它完成退出操作。


那么，你应该如何处理僵尸进程呢？
你需要修改你的服务器代码 ``wait`` 等待所有的僵尸进程直到得到它们的退出状态。
你可以通过修改你的服务器去调用一个 `wait <https://docs.python.org/2.7/library/os.html#os.wait>`__ 系统调用的方式来达到这个目的。
不幸的是，理想跟现实是有差距的，因为如果你调用 ``wait`` 然后又没有已经退出的子进程的话，调用 ``wait`` 将阻塞你的服务器， 这就阻止你的服务器处理新的客户端连接请求。
难道就没有其他选项了吗？有的，一种解决办法就是联合使用 ``signal handler`` 和 ``wait`` 系统调用。

|lsbaws_part3_conc4_signaling.png|


下面展示了是它如何工作。当一个子进程退出的时候，内核发送了一个 ``SIGCHLD`` 信号。
父进程可以设置一个用于异步接收 ``SIGCHLD`` 事件的信号处理器，并且这个处理可以 wait 子进程以便收集它的终止状态，
这样就可以阻止僵尸进程的发生了。

|lsbaws_part_conc4_sigchld_async.png|

随便说一句，一个异步事件意味着父进程事先并不知道那个事件会发生。



修改你的服务器代码，设置一个 ``SIGCHLD`` 时间处理器，在这个时间处理器中 wait 子进程终止。
可用的 `webserver3e.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3e.py>`__ 代码如下：

.. code-block:: python

    ###########################################################################
    # Concurrent server - webserver3e.py                                      #
    #                                                                         #
    # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X        #
    ###########################################################################
    import os
    import signal
    import socket
    import time

    SERVER_ADDRESS = (HOST, PORT) = '', 8888
    REQUEST_QUEUE_SIZE = 5


    def grim_reaper(signum, frame):
        pid, status = os.wait()
        print(
            'Child {pid} terminated with status {status}'
            '\n'.format(pid=pid, status=status)
        )


    def handle_request(client_connection):
        request = client_connection.recv(1024)
        print(request.decode())
        http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """
        client_connection.sendall(http_response)
        # sleep to allow the parent to loop over to 'accept' and block there
        time.sleep(3)


    def serve_forever():
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(SERVER_ADDRESS)
        listen_socket.listen(REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port} ...'.format(port=PORT))

        signal.signal(signal.SIGCHLD, grim_reaper)

        while True:
            client_connection, client_address = listen_socket.accept()
            pid = os.fork()
            if pid == 0:  # child
                listen_socket.close()  # close child copy
                handle_request(client_connection)
                client_connection.close()
                os._exit(0)
            else:  # parent
                client_connection.close()

    if __name__ == '__main__':
        serve_forever()


启动服务器：::

    $ python webserver3e.py


使用你的老朋友 ``curl`` 向修改后的并发服务器发送一个请求: ::

    $ curl http://localhost:8888/hello

看一下服务器：

|lsbaws_part3_conc4_eintr.png|


发生了什么？ accept 调用是吧了，并报了个 ``EINTR`` 错误。

|lsbaws_part3_conc4_eintr_error.png|


当子进程退出，触发 ``SIGCHLD`` 事件时，激活了时间信号处理器，然后父进程阻塞在了 accept 调用这个地方，

当信号处理器处理完成以后， accept 系统调用也跟着中断了：

|lsbaws_part3_conc4_eintr_accept.png|


别担心，这是个非常简单问题很容易解决。你要做到的就是重新开始 accept 系统调用。

下面是修改版本的服务器 `webserver3f.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3f.py>`__ ，这个版本解决了这个问题：

.. code-block:: python

    ###########################################################################
    # Concurrent server - webserver3f.py                                      #
    #                                                                         #
    # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X        #
    ###########################################################################
    import errno
    import os
    import signal
    import socket

    SERVER_ADDRESS = (HOST, PORT) = '', 8888
    REQUEST_QUEUE_SIZE = 1024


    def grim_reaper(signum, frame):
        pid, status = os.wait()


    def handle_request(client_connection):
        request = client_connection.recv(1024)
        print(request.decode())
        http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """
        client_connection.sendall(http_response)


    def serve_forever():
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(SERVER_ADDRESS)
        listen_socket.listen(REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port} ...'.format(port=PORT))

        signal.signal(signal.SIGCHLD, grim_reaper)

        while True:
            try:
                client_connection, client_address = listen_socket.accept()
            except IOError as e:
                code, msg = e.args
                # restart 'accept' if it was interrupted
                if code == errno.EINTR:
                    continue
                else:
                    raise

            pid = os.fork()
            if pid == 0:  # child
                listen_socket.close()  # close child copy
                handle_request(client_connection)
                client_connection.close()
                os._exit(0)
            else:  # parent
                client_connection.close()  # close parent copy and loop over


    if __name__ == '__main__':
        serve_forever()



启动更新后的 `webserver3f.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3f.py>`__ : ::

    $ python webserver3f.py


使用 ``curl`` 向修改过的并发服务器发送一个请求：

    $ curl http://localhost:8888/hello



看到了没？ 不再有  EINTR 异常了。现在，验证一下，不再有僵尸了，而且你的 ``SIGCHLD`` 事件处理器通过 wait 调用来处理子进程的终止事件。为了验证这个，只需要运行 ps 命令，然后你可以看一下应该不再有状态为 **Z+** 的 Python 僵尸进程了（不再有 **<default>** 进程）。太棒了！不再有僵尸进程的日子安全感终于有保障了。

|lsbaws_part3_checkpoint.png|


* 如果你 fork 了一个子进程，但是却没有 wait 它，它就会变成一个僵尸进程。
* 使用 ``SIGCHLD`` 事件处理器来异步 wait 终止的子进程以便收集它的终止状态，
* 当使用事件处理器的时候，你需要考虑到系统可能会中断，这样的话你就需求为这个场景做些准备。



好了，目前来看一起都很棒。没问题，是吧？嗯，确实如此。
再试试 `webserver3f.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3f.py>`__ ，不过这次不是使用 ``curl`` 制造一个请求，而是使用 `client3.py <https://github.com/rspivak/lsbaws/blob/master/part3/client3.py>`__ 创建 128 个同时发生的连接：::

    $ python client3.py --max-clients 128

现在再一次执行 ``ps`` 命令 ::

    $ ps auxw | grep -i python | grep -v grep


看呐，哦，天哪，僵尸进程又回来了！

|lsbaws_part3_conc5_zombies_again.png|



这次又怎么了呢？当你运行了 128 个同步的客户端时，同时就建立了 128 条连接，服务器上处理请求和退出的子进程大多数都在同一时触发大量的 ``SIGCHLD`` 信号被发送给父进程。
问题就是这些信号并不是按队列进行处理的，这样的话，你的服务器进程就会错过一些信号，这会遗留一下无人照看的僵尸进程。

|lsbaws_part3_conc5_signals_not_queued.png|


解决这个问题的方法是设置一个 ``SIGCHLD`` 事件处理器，
不使用 ``wait`` 而是调用 `waitpid <https://docs.python.org/2.7/library/os.html#os.waitpid>`__ 系统调用并在循环中使用 ``WNOHANG`` 选项，确保所有终止的子进程都被照顾到了。
下面是修改后的服务器代码， `webserver3g.py <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3g.py>`__ :

.. code-block:: python


    ###########################################################################
    # Concurrent server - webserver3g.py                                      #
    #                                                                         #
    # Tested with Python 2.7.9 & Python 3.4 on Ubuntu 14.04 & Mac OS X        #
    ###########################################################################
    import errno
    import os
    import signal
    import socket

    SERVER_ADDRESS = (HOST, PORT) = '', 8888
    REQUEST_QUEUE_SIZE = 1024


    def grim_reaper(signum, frame):
        while True:
            try:
                pid, status = os.waitpid(
                    -1,          # Wait for any child process
                     os.WNOHANG  # Do not block and return EWOULDBLOCK error
                )
            except OSError:
                return

            if pid == 0:  # no more zombies
                return


    def handle_request(client_connection):
        request = client_connection.recv(1024)
        print(request.decode())
        http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World!
    """
        client_connection.sendall(http_response)


    def serve_forever():
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(SERVER_ADDRESS)
        listen_socket.listen(REQUEST_QUEUE_SIZE)
        print('Serving HTTP on port {port} ...'.format(port=PORT))

        signal.signal(signal.SIGCHLD, grim_reaper)

        while True:
            try:
                client_connection, client_address = listen_socket.accept()
            except IOError as e:
                code, msg = e.args
                # restart 'accept' if it was interrupted
                if code == errno.EINTR:
                    continue
                else:
                    raise

            pid = os.fork()
            if pid == 0:  # child
                listen_socket.close()  # close child copy
                handle_request(client_connection)
                client_connection.close()
                os._exit(0)
            else:  # parent
                client_connection.close()  # close parent copy and loop over

    if __name__ == '__main__':
        serve_forever()

启动服务器:  ::

    $ python webserver3g.py


使用测试客户端 `client3.py <https://github.com/rspivak/lsbaws/blob/master/part3/client3.py>`__:  ::

    $ python client3.py --max-clients 128


现在验证一下已经不再有僵尸进程了。耶！没有僵尸进程的生活是如此的美好 :)

|lsbaws_part3_conc5_no_zombies.png|


恭喜！这可真是个漫长的旅程，但是我希望你能喜欢它。
现在你已经有了你自己的简单的并发服务器，这些代码可以作为你将来开发产品级 Web 服务器的基础。



我要给你留一个练习，那就是将的 `第二部分`_ 的 WSGI 服务器更新为并发服务器。
你可以从 `这里 <https://github.com/rspivak/lsbaws/blob/master/part3/webserver3h.py>`__ 得到最终的修改版。但是，只在你完成你的版本后才能查看我的代码。
你已经具备了完成这项工作的所必需的所有信息了。所以，放手去做吧：）



下一步是什么？正如 Josh Billings 说过的，


    “像一张邮票一样 —— 坚持一件事情直到你到达终点。”

开始征服基础知识。质疑你已经知道的。同时总是深入挖掘。


    “如果你只学习方法，你将束缚于你的方法。但是，如果你学会了原理，你就可以发明你自己的方法。” —— Ralph Waldo Emerson

下面是一些我选出的覆盖本文大部分知识的书籍。它们将帮助你拓宽和加深我提到的知识点。
我高度推荐的你按照这个方式去获得这些数：从你的朋友那里借这些书，从你当地的图书馆里借，
或者干脆从亚马逊上购买。它们是守护者：


* `UNIX网络编程 卷1：套接字联网API（第3版） <http://book.douban.com/subject/4859464/>`__
* `UNIX环境高级编程（第3版） <http://book.douban.com/subject/25900403/>`__
* `Linux/UNIX系统编程手册 <http://book.douban.com/subject/25809330/>`__
* `TCP/IP详解 卷1：协议（第2版） <http://book.douban.com/subject/3571433/>`__
* `The Little Book of SEMAPHORES (2nd Edition): The Ins and Outs of Concurrency Control and Common Mistakes <http://book.douban.com/subject/3666232/>`__ 也可以从作者的网站上获取免费版本。


.. [1] `UNIX网络编程 卷1：套接字联网API（第3版） <http://book.douban.com/subject/4859464/>`__
.. [2] `The Little Book of SEMAPHORES (2nd Edition): The Ins and Outs of Concurrency Control and Common Mistakes <http://book.douban.com/subject/3666232/>`__ 



.. _第一部分: http://mozillazg.com/2015/06/let-us-build-a-web-server-part-1-zh-cn.html
.. _第二部分: http://mozillazg.com/2015/06/let-us-build-a-web-server-part-2-zh-cn.html


.. |lsbaws_part3_it1.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it1.png
.. |lsbaws_part3_it2.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it2.png
.. |lsbaws_part3_it3.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it3.png
.. |lsbaws_part3_it4.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it4.png
.. |lsbaws_part3_it_socket.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_socket.png
.. |lsbaws_part3_it_socketpair.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_socket.png
.. |lsbaws_part3_it_server_socket_sequence.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_server_socket_sequence.png
.. |lsbaws_part3_it_client_socket_sequence.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_client_socket_sequence.png
.. |lsbaws_part3_it_ephemeral_port.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_ephemeral_port.png
.. |lsbaws_part3_it_server_process.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_server_process.png
.. |lsbaws_part3_it_ppid_pid.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_ppid_pid.png
.. |lsbaws_part3_it_pid_ppid_screenshot.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_pid_ppid_screenshot.png
.. |lsbaws_part3_it_process_descriptors.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_process_descriptors.png
.. |lsbaws_part3_it_default_descriptors.png| image:: /static/images/lsbaws-part3/lsbaws_part3_it_default_descriptors.png
.. |lsbaws_part3_checkpoint.png| image:: /static/images/lsbaws-part3/lsbaws_part3_checkpoint.png
.. |lsbaws_part3_conc2_service_clients.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc2_service_clients.png
.. |lsbaws_part3_fork.png| image:: /static/images/lsbaws-part3/lsbaws_part3_fork.png
.. |lsbaws_part3_it2 (1).png| image:: /static/images/lsbaws-part3/lsbaws_part3_it2 (1).png
.. |lsbaws_part3_conc2_how_fork_works.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc2_how_fork_works.png
.. |lsbaws_part3_conc2_shared_descriptors.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc2_shared_descriptors.png
.. |lsbaws_part3_conc2_concurrent_events.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc2_concurrent_events.png
.. |lsbaws_part3_conc3_child_is_active.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc3_child_is_active.png
.. |lsbaws_part3_conc3_out_of_descriptors.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc3_out_of_descriptors.png
.. |lsbaws_part3_conc3_too_many_fds_exc.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc3_too_many_fds_exc.png
.. |lsbaws_part3_conc3_zombies.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc3_zombies.png
.. |lsbaws_part3_conc3_kill_zombie.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc3_kill_zombie.png
.. |lsbaws_part3_conc3_resource_unavailable.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc3_resource_unavailable.png
.. |lsbaws_part3_conc4_signaling.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc4_signaling.png
.. |lsbaws_part_conc4_sigchld_async.png| image:: /static/images/lsbaws-part3/lsbaws_part_conc4_sigchld_async.png
.. |lsbaws_part3_conc4_eintr.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc4_eintr.png
.. |lsbaws_part3_conc4_eintr_error.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc4_eintr_error.png
.. |lsbaws_part3_conc4_eintr_accept.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc4_eintr_accept.png
.. |lsbaws_part3_conc5_zombies_again.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc5_zombies_again.png
.. |lsbaws_part3_conc5_signals_not_queued.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc5_signals_not_queued.png
.. |lsbaws_part3_conc5_no_zombies.png| image:: /static/images/lsbaws-part3/lsbaws_part3_conc5_no_zombies.png