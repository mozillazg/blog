[python]修复 python-gearman 出现 Received non-binary arguments 错误
==========================================================================

:slug: fix-python-gearman-raise-received-non-binary-arguments-errors
:date: 2015-04-20



今天第一次使用 python-gearman 就出现了 ``Received non-binary arguments`` 错误。

下面重现一下错误，当传入的 task_name 参数类型是 unicode 时就会报错::


    client.submit_job(u"task1")  # error: Received non-binary arguments


查看源码后发现，是因为 gearman client submit_job 的 task name 不支持 unicode, 把参数类型改成 str 或 bytes 就可以了： ::

    client.submit_job(b"task1")  # ok


参考资料
------------

* `python-gearman/protocol.py at 740a23f20f39f0f0d557e25afe998e56cc72a9bf · Yelp/python-gearman https://github.com/Yelp/python-gearman/blob/740a23f20f39f0f0d557e25afe998e56cc72a9bf/gearman/protocol.py#L246>`__