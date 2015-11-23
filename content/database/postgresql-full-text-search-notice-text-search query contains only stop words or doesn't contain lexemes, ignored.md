title: postgresql 全文检索功能搜索中文提示 “text-search query contains only stop words or doesn't contain lexemes, ignored”的解决办法
date: 2015-11-23
slug: postgresql-full-text-search-search-chinese-notice-text-search-query-contains-only-stop-words-or-doesn-t-contain-lexemes-ignored
tags: postgresql


![](/static/images/postgresql/tumblr_inline_nwxibtWTJU1rrl2l6_500.png)

图片来源: [http://derpinews.tumblr.com/post/132078326118/were-back](http://derpinews.tumblr.com/post/132078326118/were-back)

最近使用了一下 postgresql 的 full text search 功能，在开发机器上可以实现简单的搜索中文的功能，
但是到其他服务器上后总是出现可以搜索英文但是搜索中文却没有结果的情况。
通过在 postgres 的 shell 中执行程序生成的搜索语句后发现：当搜索条件是中文时，总是提示：

    NOTICE:  text-search query contains only stop words or doesn't contain lexemes, ignored


通过大半天的查资料，验证之后，终于解决了这个问题。如果你也出现类似问题的话，可以检查是否有一样的问题：
数据库编码不是 `UTF-8` 之类的支持中文的编码。

P.S. 如果搜索英文也有这个问题的话，可以把搜索时的解释器由 `english` 改成 `simple`:


    postgres=# SELECT to_tsvector('somthing') @@ to_tsquery('english', 's:*');
    NOTICE:  text-search query contains only stop words or doesn't contain lexemes, ignored
     ?column? 
    ----------
     f
    (1 row)

    postgres=# SELECT to_tsvector('somthing') @@ to_tsquery('simple', 's:*');
     ?column? 
    ----------
     t
    (1 row)

<!--
##解析器

english -> simple 。如果你搜索时使用的解释器是 `english` 的话改成 `simple` 或者安装的其他支持中文的解释器:
-->



## 数据库编码

默认 postgresql 内的数据库编码是 `SQL_ASCII` 编码，这个导致进行全文检索的时候没法搜索中文。
请看下面这个两个数据库，一个是 `SQL_ASCII` 编码，一个是 `UTF8` 编码。
相同的搜索语句结果也不一样：

    postgres=# \l
                                      List of databases
       Name    |  Owner   | Encoding  |   Collate   |    Ctype    |   Access privileges   
    -----------+----------+-----------+-------------+-------------+-----------------------
     db1  | owner | UTF8      | en_US.UTF-8 | en_US.UTF-8 | =Tc/owner         +
               |          |           |             |             | owner=CTc/owner
     db2     | owner   | SQL_ASCII | C           | C           | =Tc/owner           +


    postgres=# \c db1
    db1=#
    db1=# SELECT to_tsvector('我们') @@ to_tsquery('我:*');
     ?column? 
    ----------
     t
    (1 row)

    db1=# 
    
    db1=# \c db2
    db2=#
    db2=# SELECT to_tsvector('我们') @@ to_tsquery('我:*');
    NOTICE:  text-search query contains only stop words or doesn't contain lexemes, ignored
     ?column? 
    ----------
     f
    (1 row)

    db2=# 


下面讲一下如何将数据库转换为 `UTF-8` 编码。

### 修改数据库 Encoding, Collate, Ctype


1. 备份要转换的数据库:

        pg_dump --format=t -d db_name -U user_name -W -h 127.0.0.1 > dump.sql
    
2. 更新 `template1` 的编码:

        update pg_database set encoding = 6, datcollate = 'en_US.UTF8', datctype = 'en_US.UTF8' where datname = 'template1';
    
3. drop 原有的数据库或者改名:

        /* 改名 */
        ALTER DATABASE db_name RENAME TO db_name_bak;
        /* 删除 */
        drop database db_name;

4. 重新创建数据库，指定编码：

        CREATE DATABASE db_name WITH ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8' owner user_name TEMPLATE=template1;

5. 数据库权限:

        GRANT ALL PRIVILEGES ON DATABASE db_name to user_name;

        \c db_name;
        ALTER SCHEMA public OWNER to user_name;
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO user_name;
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user_name;

6. 恢复数据库数据：

        pg_restore -d db_name -h 127.0.0.1 -U user_name < dump.sql

7. 现在再试一下应该已经可以正常搜索中文了。



## 参考资料

* <http://stackoverflow.com/questions/16736891/pgerror-error-new-encoding-utf8-is-incompatible>
* <http://www.postgresql.org/docs/9.4/static/multibyte.html>
* <http://stackoverflow.com/questions/380924/how-can-i-change-database-encoding-for-a-postgresql-database-using-sql-or-phppga>
* <https://coderwall.com/p/j-_mia/make-postgres-default-to-utf8>
* <https://github.com/wvanbergen/scoped_search/issues/23>
* <https://github.com/ckan/ckan/pull/1838>
* <https://ruby-china.org/topics/14607>
* <https://github.com/kvesteri/sqlalchemy-searchable/issues/33>


