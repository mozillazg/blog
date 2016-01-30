title: 使用 sqlalchemy 时如何配置使用 postgresql 的 uuid 类型
slug: sqlalchemy-use-postgresql-uuid
date: 2016-01-30
tags: sqlalchemy, postgresql

在 sqlalchemy 中 postgresql 的 uuid 类型对象是： 
`sqlalchemy.dialects.postgresql.UUID`, 所以基本的用法是：

    from sqlalchemy.dialects.postgresql import UUID 
    
    id = Column(UUID)

下面重点要说的就是如何设置自动生成随机的 uuid。

第一种办法是，使用 python 的 `uuid` 模块生成 uuid:

    id = Column(UUID, default=lambda: str(uuid.uuid4()))


第二种办法（推荐）是，服务端去生成 uuid 之 `gen_random_uuid()`:

    from postgreql import text
    
    id = Column(UUID, server_default=text("gen_random_uuid()"))

`gen_random_uuid()` 并不是默认可用的，需要在数据库中安装 `pgcrypto` 模块（下面的操作在 postgresql 数据库控制台中操作）：

    # \c db_name
    # create extension pgcrypto;
    CREATE EXTENSION
    # select gen_random_uuid();
               gen_random_uuid            
    --------------------------------------
     52f3e12b-b42a-47df-80de-6bfd9396b87e
    (1 row)

第三种办法是，服务端去生成 uuid 之 `uuid_generate_v4()`:

    id = Column(UUID, server_default=text("uuid_generate_v4()"))

需要在数据库中安装 `uuid-ossp` 模块：

    # \c db_name
    # create extension "uuid-ossp";
    CREATE EXTENSION
    # select uuid_generate_v4();
               uuid_generate_v4           
    --------------------------------------
     53153822-8516-45d7-8804-9792439e449a
    (1 row)

## 参考资料

* [PostgreSQL &mdash; SQLAlchemy 1.1 Documentation](http://docs.sqlalchemy.org/en/rel_1_1/dialects/postgresql.html#sqlalchemy.dialects.postgresql.UUID)
* [Column Insert/Update Defaults &mdash; SQLAlchemy 1.1 Documentation](http://docs.sqlalchemy.org/en/rel_1_1/core/defaults.html#server-side-defaults)
* [How to set a column default to a PostgreSQL function using SQLAlchemy? - Stack Overflow](http://stackoverflow.com/a/20537690/1804866)
* [PostgreSQL: Documentation: 9.5: pgcrypto](http://www.postgresql.org/docs/9.5/static/pgcrypto.html)
* [PostgreSQL: Documentation: 9.5: uuid-ossp](http://www.postgresql.org/docs/9.5/static/uuid-ossp.html)