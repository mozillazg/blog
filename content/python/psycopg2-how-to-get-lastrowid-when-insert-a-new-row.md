title: psycopg2 插入数据时如何获取新纪录的主键
slug: psycopg2-how-to-get-lastrowid-when-insert-a-new-row
date: 2016-02-15
tags: psycopg2, postgresql

默认情况下，使用 psycopg2 时 `cursor.lastrowid` 并不会返回新纪录的主键。
[文档](http://initd.org/psycopg/docs/cursor.html?highlight=lastrowid#cursor.lastrowid) 中是这样解释的：

> cursor.lastrowid
>
> This read-only attribute provides the OID of the last row inserted by the cursor.
> If the table wasn’t created with OID support or the last operation is not a single record insert,
> the attribute is set to None.
>
> Note
>
> PostgreSQL currently advices to not create OIDs on the tables and the default for `CREATE TABLE`
> is to not support them. The `INSERT ... RETURNING` syntax available from
> PostgreSQL 8.3 allows more flexibility.

根据文档，我们可以是用 `INSERT ... RETURNING` 的方式来获取主键：

    exampledb=> INSERT INTO users (username) VALUES ('hello') RETURNING id;
     id
    ----
     11
    (1 row)

    INSERT 0 1

python 中这样用：

    >>> cursor.execute("INSERT INTO users (username) VALUES ('hello') RETURNING id;")
    >>> cursor.fetchone()
    (11,)


## 参考资料

* [PEP 0249 -- Python Database API Specification v2.0 | Python.org](https://www.python.org/dev/peps/pep-0249/#lastrowid)
* [The cursor class — Psycopg 2.6.2.dev0 documentation](http://initd.org/psycopg/docs/cursor.html?highlight=lastrowid#cursor.lastrowid)
