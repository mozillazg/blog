Title: [python]指定 Socket connect 方法的超时时间
Date: 2013-11-18
Tags: python, socket
Slug: python-socket-connect-set-timeout

通过设置 `socket.settimeout` 来实现超时功能：

    :::python
    import select
    import socket

    HOST = '127.0.0.1'
    PORT = 8000
    timeout = 60 * 1   # 1 分钟

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置连接超时
    s.settimeout(10)
    s.connect((HOST, PORT))
    # 恢复默认超时设置
    s.settimeout(None)
    s.connect((HOST, PORT))
    s.sendall('msg')

## 参考

* [Python socket connection timeout - Stack Overflow](http://stackoverflow.com/questions/3432102/python-socket-connection-timeout)
