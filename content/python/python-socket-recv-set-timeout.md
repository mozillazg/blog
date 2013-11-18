Title: [python]指定 Socket recv 方法的超时时间
Date: 2013-11-18
Tags: python, socket
Slug: python-socket-recv-set-timeout

使用 `select` 来变相实现超时功能：

    :::python
    import select
    import socket

    HOST = '127.0.0.1'
    PORT = 8000
    timeout = 60 * 1   # 1 分钟

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall('msg')
    # 设置 recv 超时时间
    s.setblocking(0)
    ready = select.select([s], [], [], timeout)
    if ready[0]:
        # 接收结果
        data = s.recv(1024).strip('\x00')

## 参考

* [How to set timeout on python's socket recv method? - Stack Overflow](http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method)
