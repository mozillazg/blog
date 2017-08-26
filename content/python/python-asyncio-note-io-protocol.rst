asyncio 学习笔记：使用抽象类 Protocol 实现异步 I/O
==================================================

:slug: python-asyncio-note-io-protocol
:date: 2017-08-26
:tags: asyncio

本文是 https://pymotw.com/3/asyncio/io_protocol.html
的学习笔记，强烈推荐直接阅读原文。

这次将用两个程序介绍使用 asyncio 实现一个简单的 echo 服务端和客户端程序

echo 服务端程序
---------------

首先导入必需的一些模块，设置一下 asyncio 和
logging，然后再创建一个事件循环对象.

.. code:: python

    # asyncio_echo_server_protocol.py
    import asyncio
    import logging
    import sys


    SERVER_ADDRESS = ('localhost', 10000)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stderr,
    )
    log = logging.getLogger('main')

    event_loop = asyncio.get_event_loop()

| 然后定义一个继承 ``asyncio.Protocol`` 的子类，用来处理与客户端的通信。
| ``protocol`` 的方法是基于服务端 socket 事件来触发的。

.. code:: python

    class EchoServer(asyncio.Protocol):

| 每当有一个新的客户端连接的时候，就会触发调用 ``connection_made()``
  方法。 ``transport`` 参数
| 是一个 ``asyncio.Transport`` 实例对象，这个对象抽象了一系列使用 socket
  进行异步 I/O 操作的方法。不同的通信协议提供了不同的 transport
  实现，但是它们都有同样的 API.
| 比如，有一些 transport 类用来与 socket
  通信，有些用来跟子进程通过管道通信。
| 可以通过 ``get_extra_info()`` 获取进来的客户端的地址信息。

.. code:: python

        def connection_made(self, transport):
            self.transport = transport
            self.address = transport.get_extra_info('peername')
            self.log = logging.getLogger(
                'EchoServer_{}_{}'.format(*self.address)
            )
            self.log.debug('connection accepted')

连接建立以后，当有数据从客户端发到服务端的时候会使用传输过来的数据调用
``data_received()``
方法。这里我们记录一下收到的数据，然后立即发收到的数据通过
``transport.write()`` 发回客户端。

.. code:: python

    def data_received(self, data):
            self.log.debug('received {!r}'.format(data))
            self.transport.write(data)
            self.log.debug('sent {!r}'.format(data))

一些 transport 支持一个特殊的 end-of-file 标识符(\ ``EOF``)。当遇到一个
``EOF`` 的时候，\ ``eof_received()``
方法会被调用。在本次实现中，\ ``EOF``
会被发送会客户端，表示这个信号已经被收到。因为不是所有的 transport
都支持这个 ``EOF`` ，这个协议会首先询问 transport 是否可以安全的发送
``EOF`` .

.. code:: python

        def eof_received(self):
            self.log.debug('received EOF')
            if self.transport.can_write_eof():
                self.transport.write_eof()

当一个连接被关闭的时候，无论是正常关闭还是因为一个错误导致的关闭，协议的
``connection_lost()``
方法都会被调用，如果是因为出错，参数中会包含一个相关的异常对象，否则这个对象就是
``None``.

.. code:: python

        def connection_lost(self, error):
            if error:
                self.log.error('ERROR: {}'.format(error))
            else:
                self.log.debug('closing')
            super().connection_lost(error)

需要两步来启动这个服务器。首先，应用告诉事件循环创建使用 protocol 类和
hostname 以及 socket 监听的端口信息来创建一个新的 server 对象。
``create_server()`` 方法是一个 coroutine,
所以它的结果必须通过事件循环来处理这样才能真正的启动服务器。这个
coroutine 完成的时候会返回一个 与事件循环相关联的 ``asyncio.Server``
实例.

.. code:: python

    factory = event_loop.create_server(EchoServer, *SERVER_ADDRESS)
    server = event_loop.run_until_complete(factory)
    log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

| 然后这个事件循环需要被运行，以便接收客户端请求以及处理相关事件。
| 对于一个长时间运行的服务器程序来说， ``run_forever()``
  方法是最简便的实现这个功能的方法。
| 当事件循环被停止的时候，无论是通过应用程序代码还是通过进程信号停止的，server
  都可以被关闭以便能够正确的清理 socket 资源

.. code:: python

    try:
        event_loop.run_forever()
    finally:
        log.debug('closing server')
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        log.debug('closing event loop')
        event_loop.close()

echo 客户端
-----------

使用 protocol 类实现一个客户端的代码跟实现一个服务器端非常的相似.

.. code:: python

    # asyncio_echo_client_protocol.py
    import asyncio
    import functools
    import logging
    import sys

    MESSAGES = [
        b'This is the message. ',
        b'It will be sent ',
        b'in parts.',
    ]
    SERVER_ADDRESS = ('localhost', 10000)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stderr,
    )
    log = logging.getLogger('main')

    event_loop = asyncio.get_event_loop()

| 客户端 protocol 类定义了跟服务器端相同的方法，但是是不同的实现。
| ``future`` 参数是一个 ``Future``
  实例，用来作为客户端已经完成了一次接收来只服务端数据操作的信号。

.. code:: python

    class EchoClient(asyncio.Protocol):
        def __init__(self, messages, future):
            super().__init__()
            self.messages = messages
            self.log = logging.getLogger('EchoClient')
            self.f = future

当客户端成功连接到服务器时，会立即开始通信。客户端一次发送了一堆数据，因为网络等原因可能会把多个消息合并到一个消息中。当所有消息都送达的时候，将发送一个
``EOF``\ 。

虽然看起你所有的数据都立即被发送了，事实上 transport
对象会缓冲发出去的数据并且会设置一个回调来传输最终的数据，当 socket
的缓冲区准备好可以发送的时候会调用这个回调。这些都是由 transport
来实现的，所以应用代码可以按照 I/O 操作就像看起来那么发生的样子来实现.

.. code:: python

        def connection_made(self, transport):
            self.transport = transport
            self.address = transport.get_extra_info('peername')
            self.log.debug(
                'connectiong to {} port {}'.format(*self.address)
            )
            # 也可以使用 transport.writelines()
            # 这里使用 transport.write() 是为了方便
            # 记录发送的每一行内容
            for msg in self.messages:
                transport.write(msg)
                self.log.debug('sending {!r}'.format(msg))

            if transport.can_write_eof():
                transport.write_eof()

当接收到来着服务器端的响应时，将会把这个响应记录下来

.. code:: python

        def data_received(self, data):
            self.log.debug('received {!r}'.format(data))

无论是收到 end-of-file 标记还是服务器端断开了连接，本地 transport
对象都将关闭并且 future 对象都会被通过设置一个结果值的方式标记为已完成。

.. code:: python

        def eof_received(self):
            self.log.debug('received EOF')
            self.transport.close()
            if not self.f.done():
                self.f.set_result(True)

        def connnection_lost(self, exc):
            self.log.debug('server closed connection')
            self.transport.close()
            if not self.f.done():
                self.f.set_result(True)
            super().connectiong_lost(exc)

然后创建所需的 future, 以及客户端 coroutine

.. code:: python

    client_completed = asyncio.Future()
    client_factory = functools.partial(
        EchoClient,
        messages=MESSAGES,
        future=client_completed
    )
    factory_coroutine = event_loop.create_connection(
        client_factory,
        *SERVER_ADDRESS,
    )

然后使用两次 wait 来处理客户端发送完成并退出的操作

.. code:: python

    log.debug('waiting for client to complete')
    try:
        event_loop.run_until_complete(factory_coroutine)
        event_loop.run_until_complete(client_completed)
    finally:
        log.debug('closing event loop')
        event_loop.close()

输出
----

在一个窗口运行服务端程序，然后在另一个窗口中运行三次客户端程序，客户端程序的输出如下:

::

    $ python3.6 asyncio_echo_client_protocol.py
    asyncio: Using selector: KqueueSelector
    main: waiting for client to complete
    EchoClient: connectiong to ::1 port 10000
    EchoClient: sending b'This is the message. '
    EchoClient: sending b'It will be sent '
    EchoClient: sending b'in parts.'
    EchoClient: received b'This is the message. It will be sent in parts.'
    EchoClient: received EOF
    main: closing event loop

    $ python3.6 asyncio_echo_client_protocol.py
    asyncio: Using selector: KqueueSelector
    main: waiting for client to complete
    EchoClient: connectiong to ::1 port 10000
    EchoClient: sending b'This is the message. '
    EchoClient: sending b'It will be sent '
    EchoClient: sending b'in parts.'
    EchoClient: received b'This is the message. It will be sent in parts.'
    EchoClient: received EOF
    main: closing event loop

    $ python3.6 asyncio_echo_client_protocol.py
    asyncio: Using selector: KqueueSelector
    main: waiting for client to complete
    EchoClient: connectiong to ::1 port 10000
    EchoClient: sending b'This is the message. '
    EchoClient: sending b'It will be sent '
    EchoClient: sending b'in parts.'
    EchoClient: received b'This is the message. It will be sent '
    EchoClient: received b'in parts.'
    EchoClient: received EOF
    main: closing event loop

尽管客户端是分批发送的数据，但是服务器端其实有时收到的其实是合并后的整个数据。

::

    $ asyncio_echo_server_protocol.py
    asyncio: Using selector: KqueueSelector
    main: starting up on localhost port 10000
    EchoServer_::1_56353: connection accepted
    EchoServer_::1_56353: received b'This is the message. It will be sent in parts.'
    EchoServer_::1_56353: sent b'This is the message. It will be sent in parts.'
    EchoServer_::1_56353: received EOF
    EchoServer_::1_56353: closing

    EchoServer_::1_56354: connection accepted
    EchoServer_::1_56354: received b'This is the message. It will be sent in parts.'
    EchoServer_::1_56354: sent b'This is the message. It will be sent in parts.'
    EchoServer_::1_56354: received EOF
    EchoServer_::1_56354: closing

    EchoServer_::1_56355: connection accepted
    EchoServer_::1_56355: received b'This is the message. It will be sent '
    EchoServer_::1_56355: sent b'This is the message. It will be sent '
    EchoServer_::1_56355: received b'in parts.'
    EchoServer_::1_56355: sent b'in parts.'
    EchoServer_::1_56355: received EOF
    EchoServer_::1_56355: closing

完整代码
--------

服务端代码
~~~~~~~~~~

.. code:: python

    # asyncio_echo_server_protocol.py
    import asyncio
    import logging
    import sys


    SERVER_ADDRESS = ('localhost', 10000)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stderr,
    )
    log = logging.getLogger('main')

    event_loop = asyncio.get_event_loop()


    class EchoServer(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            self.address = transport.get_extra_info('peername')
            self.log = logging.getLogger(
                'EchoServer_{}_{}'.format(*self.address)
            )
            self.log.debug('connection accepted')

        def data_received(self, data):
            self.log.debug('received {!r}'.format(data))
            self.transport.write(data)
            self.log.debug('sent {!r}'.format(data))

        def eof_received(self):
            self.log.debug('received EOF')
            if self.transport.can_write_eof():
                self.transport.write_eof()

        def connection_lost(self, error):
            if error:
                self.log.error('ERROR: {}'.format(error))
            else:
                self.log.debug('closing')
            super().connection_lost(error)


    factory = event_loop.create_server(EchoServer, *SERVER_ADDRESS)
    server = event_loop.run_until_complete(factory)
    log.debug('starting up on {} port {}'.format(*SERVER_ADDRESS))

    try:
        event_loop.run_forever()
    finally:
        log.debug('closing server')
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        log.debug('closing event loop')
        event_loop.close()

客户端代码
~~~~~~~~~~

::

    # asyncio_echo_client_protocol.py
    import asyncio
    import functools
    import logging
    import sys

    MESSAGES = [
        b'This is the message. ',
        b'It will be sent ',
        b'in parts.',
    ]
    SERVER_ADDRESS = ('localhost', 10000)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(name)s: %(message)s',
        stream=sys.stderr,
    )
    log = logging.getLogger('main')

    event_loop = asyncio.get_event_loop()


    class EchoClient(asyncio.Protocol):
        def __init__(self, messages, future):
            super().__init__()
            self.messages = messages
            self.log = logging.getLogger('EchoClient')
            self.f = future

        def connection_made(self, transport):
            self.transport = transport
            self.address = transport.get_extra_info('peername')
            self.log.debug(
                'connectiong to {} port {}'.format(*self.address)
            )
            # 也可以使用 transport.writelines()
            # 这里使用 transport.write() 是为了方便
            # 记录发送的每一行内容
            for msg in self.messages:
                transport.write(msg)
                self.log.debug('sending {!r}'.format(msg))

            if transport.can_write_eof():
                transport.write_eof()

        def data_received(self, data):
            self.log.debug('received {!r}'.format(data))

        def eof_received(self):
            self.log.debug('received EOF')
            self.transport.close()
            if not self.f.done():
                self.f.set_result(True)

        def connnection_lost(self, exc):
            self.log.debug('server closed connection')
            self.transport.close()
            if not self.f.done():
                self.f.set_result(True)
            super().connectiong_lost(exc)


    client_completed = asyncio.Future()
    client_factory = functools.partial(
        EchoClient,
        messages=MESSAGES,
        future=client_completed
    )
    factory_coroutine = event_loop.create_connection(
        client_factory,
        *SERVER_ADDRESS,
    )

    log.debug('waiting for client to complete')
    try:
        event_loop.run_until_complete(factory_coroutine)
        event_loop.run_until_complete(client_completed)
    finally:
        log.debug('closing event loop')
        event_loop.close()

参考资料
--------

-  `Asynchronous I/O with Protocol Class Abstractions — PyMOTW
   3 <https://pymotw.com/3/asyncio/io_protocol.html>`__
-  `18.5.4. Transports and protocols (callback based API) — Python 3.6.2
   documentation <https://docs.python.org/3.6/library/asyncio-protocol.html>`__
