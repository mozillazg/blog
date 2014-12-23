[python] redis-py 模块使用时需要注意的一些事情
=================================================

:date: 2014-12-21
:slug: python-redis-py-notes


Redis 类 与 StrictRedis 类
-------------------------------

``Redis`` 类 与 ``StrictRedis`` 类方法的一些差异（``StrictRedis`` 实现的是标准 redis 命令）：

========  ===============================================  ==================================================
命令        Redis                                            StrictRedis
========  ===============================================  ==================================================
SETEX     ``setex(name, value, time)``                     ``setex(name, time, value)``
ZADD      ``zadd(name, *args, **kwargs)``                  ``zadd(name, *args, **kwargs)``

          * ``args``: name1, score1, name2, score2,...     * ``args``: score1, name1, score2, name2,...
          * ``kwargs``: name1=score1, name2=score2,...     * ``kwargs``: score1=name1, score2=name2,...
LREM      ``lrem(name, value, num=0)``                     ``lrem(name, count, value)``
========  ===============================================  ==================================================


ResponseError: wrong number of arguments for 'xxx' command
-----------------------------------------------------------------

当使用 ``*args``, ``**kwargs`` 参数时容易出现这个 ``ResponseError`` 错误。
使用前需要先检查 ``args`` 和 ``kwargs`` 是否为空::

    if keys:
        r.hdel('name', *keys)


参考资料
-----------

* https://github.com/andymccurdy/redis-py
* http://redis-py.readthedocs.org/en/latest/