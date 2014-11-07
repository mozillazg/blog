解决 SQLAlchemy 中使用 sqlite 时 BigInteger 不支持 AUTOINCREMENT 的问题
==================================================================================

:date: 2014-11-05
:tags: SQLAlchemy
:slug: sqlalchemy-fix-BigInteger-AUTOINCREMENT-don't-work-when-use-sqlite

默认情况下，在 SQLAlchemy 中使用 sqlite 作为数据库时， ``BigInteger`` 不支持自动增长（AUTOINCREMENT），插入数据时会报如下错误::

    Query Error: AUTOINCREMENT is only allowed on an INTEGER PRIMARY KEY Unable to execute statement

可以通过使用 ``compiles`` 对 ``sqlite`` 下的 ``BigInteger`` 做特殊处理，让它实际上执行的是 ``Integer`` 相关操作:

.. code-block:: python

    from sqlalchemy import BigInteger
    from sqlalchemy.ext.compiler import compiles


    @compiles(BigInteger, 'sqlite')
    def bi_c(element, compiler, **kw):
        return "INTEGER"


参考资料
-----------------

* `zzzeek / sqlalchemy / issues / #2074 - Map BigInteger type to INTEGER to allow AUTOINCREMENT to work —— Bitbucket`__
* `Custom SQL Constructs and Compilation Extension —— SQLAlchemy 0.9 Documentation`__
 
__ https://bitbucket.org/zzzeek/sqlalchemy/issue/2074/map-biginteger-type-to-integer-to-allow

__ http://docs.sqlalchemy.org/en/rel_0_9/core/compiler.html?highlight=ext.compiler#sqlalchemy.ext.compiler.compiles