Title: [database] postgresql 常用操作
Date: 2014-06-05
Tags: postpresql, psql
Slug: hello-postgresql



## 安装

    sudo apt-get install postgresql-client
    sudo apt-get install postgresql

## 启动

    sudo service postgresql start

## 进入控制台

    sudo -u postgres psql

或

    psql -U dbuser -d exampledb -h 127.0.0.1 -p 5432

退出

    postgres=# \q


## 创建用户 

    sudo -u postgres createuser dbuser

或

    sudo -u postgres psql
    postgres=# CREATE USER dbuser WITH PASSWORD 'password';

查看所有用户

    postgres=# \du

更改密码

    postgres=# \password dbuser
    postgres=# \q

删除用户

    postgres=# drop user dbuser;

## 创建数据库

    postgres=# CREATE DATABASE exampledb OWNER dbuser;
    postgres=# GRANT ALL PRIVILEGES ON DATABASE exampledb to dbuser;
    postgres=# \c exampledb;
    postgres=# ALTER SCHEMA public OWNER to dbuser;
    postgres=# GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dbuser;
    postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dbuser;

或

    sudo -u postgres createdb -O dbuser exampledb

查看所有数据库

    postgres=# \l

## 切换数据库

    postgres=# \c exampledb

## 查看表

    postgres=# \d

查看表结构

    postgres=# \d user_tab1

## 常用控制台命令

    \password           设置密码。
    \q                  退出。
    \h                  查看SQL命令的解释，比如\h select。
    \?                  查看psql命令列表。
    \l                  列出所有数据库。
    \c [database_name]  连接其他数据库。
    \d                  列出当前数据库的所有表格。
    \d [table_name]     列出某一张表格的结构。
    \du                 列出所有用户。
    \e                  打开文本编辑器。
    \conninfo           列出当前数据库和连接的信息。

## 基本的 SQL 语句


    # 创建新表
    CREATE TABLE user_tbl(name VARCHAR(20), signup_date DATE);

    # 插入数据
    INSERT INTO user_tbl(name, signup_date) VALUES('张三', '2013-12-22');

    # 查询记录
    SELECT * FROM user_tbl;

    # 更新数据
    UPDATE user_tbl set name = '李四' WHERE name = '张三';

    # 删除记录
    DELETE FROM user_tbl WHERE name = '李四' ;

    # 添加字段
    ALTER TABLE user_tbl ADD email VARCHAR(40);

    # 更改字段类型
    ALTER TABLE user_tbl ALTER COLUMN signup_date SET NOT NULL;
    
    # 设置字段默认值（注意字符串使用单引号）
    ALTER TABLE user_tbl ALTER COLUMN email SET DEFAULT 'example@example.com';
    
    # 去除字段默认值
    ALTER TABLE user_tbl ALTER email DROP DEFAULT;

    # 重命名字段
    ALTER TABLE user_tbl RENAME COLUMN signup_date TO signup;

    # 删除字段
    ALTER TABLE user_tbl DROP COLUMN email;

    # 表重命名
    ALTER TABLE user_tbl RENAME TO backup_tbl;

    # 删除表
    DROP TABLE IF EXISTS backup_tbl;
    
    # 删除库
    \c hello2;
    DROP DATABASE IF EXISTS hello;

从上面的命令可以看出基本的 SQL 语句跟 MySQL 是一样的。


## 备份、恢复

* pg_dump 备份
* pg_dumpall 备份所有数据库
* pg_restore 恢复
* psql exampledb < exampledb.sql  导入数据

example:

    pg_dump --format=t -d db_name -U user_name -W -h 127.0.0.1 > dump.sql
    pg_restore -d db_name -h 127.0.0.1 -U user_name < dump.sql
    # 注意要加 -U 并且一定要是 db_name 的 owner


## Peer authentication failed for user "user_name"

    $ pg_dump --format=t -d db_name -U user_name 
    pg_dump: [archiver (db)] connection to database "db_name" failed: FATAL:  Peer authentication failed for user "user_name"
    $ # 指定 hostname 即可
    $ pg_dump --format=t -d db_name -U user_name -h 127.0.0.1


## 参考资料

* [PostgreSQL新手入门 - 阮一峰的网络日志](http://www.ruanyifeng.com/blog/2013/12/getting_started_with_postgresql.html)
* <http://www.postgresql.org/docs>
