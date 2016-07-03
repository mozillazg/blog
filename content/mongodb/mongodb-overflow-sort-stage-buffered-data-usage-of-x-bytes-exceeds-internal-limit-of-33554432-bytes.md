Title: mongodb: 解决 Overflow sort stage buffered data 错误
Date: 2016-07-02
Slug: mongodb-overflow-sort-stage-buffered-data-usage-of-x-bytes-exceeds-internal-limit-of-33554432-bytes

使用 pymongo 时有时会遇到提示如下的错误:

      File "/usr/local/lib/python2.7/dist-packages/pymongo/cursor.py", line 1090, in next
        if len(self.__data) or self._refresh():
      File "/usr/local/lib/python2.7/dist-packages/pymongo/cursor.py", line 1022, in _refresh
        self.__uuid_subtype))
      File "/usr/local/lib/python2.7/dist-packages/pymongo/cursor.py", line 958, in __send_message
        self.__compile_re)
      File "/usr/local/lib/python2.7/dist-packages/pymongo/helpers.py", line 113, in _unpack_response
        error_object)
    OperationFailure: database error: Executor error: Overflow sort stage buffered data usage of 33597009 bytes exceeds internal limit of 33554432 bytes

为什么会出现这样的错误呢？ 原来 mongodb 限制了在内存中进行 sort 操作（无法使用索引的情况下）时所使用的最大内存大小，默认是 32 M(33554432 bytes)。

如果要修改这个限制的话，可以通过如下的 mongo 命令进行修改，比如修改为 50 M(52428800 bytes):

    > use admin
    > db.adminCommand({setParameter: 1, internalQueryExecMaxBlockingSortBytes: 52428800})


## 参考资料

* [mongodb - How to increase buffered data limit? - Ask Ubuntu](http://askubuntu.com/questions/501937/how-to-increase-buffered-data-limit)
* [MongoDB Limits and Thresholds &mdash; MongoDB Manual 3.2](https://docs.mongodb.com/manual/reference/limits/#Sort-Operations)