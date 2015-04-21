

Received non-binary arguments

今天使用 python-gearman 是出现了 Received non-binary arguments 错误： ::

client.submit_job("task1")  # error: Received non-binary arguments


查看源码后发现，是因为 gearman client 不支持 unicode, 把参数类型改成 str 或 bytes 就可以了： ::

client.submit_job(b"task1")  # ok



https://github.com/Yelp/python-gearman/blob/master/gearman/protocol.py#L246