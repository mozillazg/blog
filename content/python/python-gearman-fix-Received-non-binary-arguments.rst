[python]修复 python-gearman 出现 Received non-binary arguments 错误
==========================================================================

:slug: fix-python-gearman-raise-received-non-binary-arguments-errors
:date: 2015-04-20



今天第一次使用 python-gearman 就出现了 ``Received non-binary arguments`` 错误。

下面重现一下错误，当传入的参数类型是 unicode 时就会报错::


    client.submit_job("task1")  # error: Received non-binary arguments


查看源码后发现，是因为 gearman client submit_job 不支持 unicode, 把参数类型改成 str 或 bytes 就可以了： ::

    client.submit_job(b"task1")  # ok


参考资料
------------

* https://github.com/Yelp/python-gearman/blob/master/gearman/protocol.py#L246