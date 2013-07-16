Title: mysql 基于 master-master 的双机热备配置
Date: 2013-06-21
Tags: mysql, replication
Slug: mysql-master-master

[TOC]

master-master 就是两台服务器互为主从：          
master1-slave(master2) && master2-slave(master1)

* master1: 192.168.100.191
* master2: 192.168.100.166


## master1-slave(master2)

**mysql 版本最好一致**

### 设置 master1

1. 创建给 slave 登录用的用户名密码:

        :::bash
        mysql> GRANT REPLICATION SLAVE ON *.* TO 'backup'@'192.168.100.166' IDENTIFIED BY 'yNZE7fK9*@aMA?*ppF';

        # humanreadable
        mysql> # grant replication slave on *.* to 'backup'@'192.168.100.166' identified by 'yNZE7fK9*@aMA?*ppF';

        mysql> create database hello default charset utf8;

2. 配置 my.cnf

        :::bash
        # vim /etc/my.cnf
        [mysqld]
        server-id=1    #主机id，整数
        #开启二进制日志，并且名称为 /var/lib/mysql/mysql-bin.***
        # 如果是个路径则，保存到该路径下(log-bin=/var/log/mysql-bin.log  -> /var/log/mysql-bin.***)
        log-bin=mysql-bin
        read-only=0  #主机读写权限，读写都可以
        binlog-do-db=hello   #记录日志的数据库：需要的备份数据，多个写多行
        # binlog-do-db=hello2
        binlog-ignore-db=mysql #不记录日志的数据库：不需要备份的数据库，多个写多行
        binlog-ignore-db=test
        binlog-ignore-db=information_schema
        # 自增字段奇数递增，防止冲突（1, 3, 5, ...,）
        auto-increment-increment = 2  # 每次递增的步长
        auto-increment-offset = 1  # 初始值

    重启 mysql: `serivce mysqld restart`


3. 导出数据库

    锁定数据库，不要退出 mysql shell

        :::bash
        mysql>FLUSH TABLES WITH READ LOCK;
        mysql># flush tables with read lock;
    新开一个终端，导出数据库

        :::bash
        mysqldump --master-data -uroot -p hello > hello.sql

    查看主服务器的状态

        :::bash
        mysql> show master status\G;
        *************************** 1. row ***************************
                    File: mysql-bin.000001
                Position: 98
            Binlog_Do_DB: hello
        Binlog_Ignore_DB: mysql,test,information_schema
        1 row in set (0.00 sec)

        ERROR: 
        No query specified
    记下 Position 和 File 的值。
    解锁

        :::bash
        mysql> UNLOCK TABLES;
        mysql> # unlock tables;


### 设置 slave(master2)

1. 编辑 my.cnf

        :::bash
        # vim /etc/my.cnf

        [mysqld]
        server-id=2
        log-bin=mysql-bin
        master-host=192.168.100.191  # master1
        master-user=backup  # 刚才在 master1 上设置的用户名密码
        master-password=yNZE7fK9*@aMA?*ppF  # password
        master-port=3306   # master1 mysql port
        master-connect-retry=60 #如果从服务器发现主服务器断掉，重新连接的时间差(秒)
        replicate-do-db =hello #只复制某个库，多个写多行
        replicate-ignore-db=mysql #不复制某个库
        replicate-ignore-db=test
        replicate-ignore-db=information_schema
        relay-log=mysqld-relay-bin  # 开启日志中继
        log-slave-updates  # slave将复制事件写进自己的二进制日志
        #5.5
        #log-slave-updates = ON
        #5.1
        #log-slave-updates = 1

        # 自增字段奇数递增，防止冲突（1, 3, 5, ...,）
        auto-increment-increment = 2  # 每次递增的步长
        auto-increment-offset = 1  # 初始值

2. 导入 master 导出的数据库：


        :::bash
        mysql> create database hello default charset utf8;
        mysql -uroot -p hello < hello.sql

3. 配置 master 信息：

        :::bash
        mysql> slave stop;

        mysql> CHANGE MASTER TO
        -> MASTER_HOST='192.168.100.191', //主服务器的IP地址
        -> MASTER_USER='backup', //同步数据库的用户
        -> MASTER_PASSWORD='yNZE7fK9*@aMA?*ppF', //同步数据库的密码
        -> MASTER_LOG_FILE='mysql-bin.000001', //主服务器二进制日志的文件名(前面要求记住的 File 参数)
        -> MASTER_LOG_POS=98; //日志文件的开始位置(前面要求记住的 Position 参数)

        mysql> CHANGE MASTER TO MASTER_HOST='192.168.100.191', MASTER_USER='backup', MASTER_PASSWORD='yNZE7fK9*@aMA?*ppF', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=98;

        mysql > slave start;


    重启 master, slave: `service mysqld restart`

    查看 slave 状态：

    进入 slave mysql:

        :::bash
        mysql> show slave status\G;
        *************************** 1. row ***************************
                    Slave_IO_State: Connecting to master
                        Master_Host: 192.168.100.191
                        Master_User: backup
                        Master_Port: 3306
                    Connect_Retry: 60
                    Master_Log_File: mysql-bin.000001
                Read_Master_Log_Pos: 98
                    Relay_Log_File: mysqld-relay-bin.000001
                    Relay_Log_Pos: 98
            Relay_Master_Log_File: mysql-bin.000001
                Slave_IO_Running: Yes
                Slave_SQL_Running: Yes
                    Replicate_Do_DB: hello
                Replicate_Ignore_DB: mysql,test,information_schema
                Exec_Master_Log_Pos: 98
                    Relay_Log_Space: 98
                    Until_Log_Pos: 0
            Seconds_Behind_Master: NULL
        1 row in set (0.00 sec)

    注意一定要有下面两项，没有的话查看错误日志(less /var/log/mysqld.log)：

                Slave_IO_Running: Yes
                Slave_SQL_Running: Yes

4. 测试

    master 服务器

        :::bash
        mysql> use hello;
        Database changed
        mysql> create table test(id int);
        mysql> insert int test set id=1;

        mysql> show master status\G;
        *************************** 1. row ***************************
                    File: mysql-bin.000002  # 注意这里
                Position: 276    # 注意这里
            Binlog_Do_DB: hello
        Binlog_Ignore_DB: mysql,test,information_schema
        1 row in set (0.00 sec)


    slave 服务器

        :::bash
        mysql> use hello;
        mysql> show tables;
        +-----------------+
        | Tables_in_hello |
        +-----------------+
        | test            | 
        +-----------------+
        1 row in set (0.00 sec)

        mysql> select * from test;
        +------+
        | id   |
        +------+
        |    1 | 
        +------+
        1 row in set (0.00 sec)

        mysql> show slave status\G;
        *************************** 1. row ***************************
                    Slave_IO_State: Waiting for master to send event
                        Master_Host: 192.168.100.191
                        Master_User: backup
                        Master_Port: 3306
                    Connect_Retry: 60
                    Master_Log_File: mysql-bin.000002  # 跟 master 一样
                Read_Master_Log_Pos: 276  # 跟 master 一样
                    Relay_Log_File: mysqld-relay-bin.000003
                    Relay_Log_Pos: 413
            Relay_Master_Log_File: mysql-bin.000002
                Slave_IO_Running: Yes
                Slave_SQL_Running: Yes
                    Replicate_Do_DB: hello
                Replicate_Ignore_DB: mysql,test,information_schema
                        Last_Errno: 0
                        Last_Error: 
                    Skip_Counter: 0
                Exec_Master_Log_Pos: 276
                    Relay_Log_Space: 413
            Seconds_Behind_Master: 0
        1 row in set (0.00 sec)


## master2-slave(master1)



### master2:

    :::bash
    mysql> grant replication slave on *.* to 'backup'@'192.168.100.191' identified by 'yNZE7fK9*@aMA?*ppF';
    mysql> flush tables with read lock;
    mysql> show master status\G;
    *************************** 1. row ***************************
                File: mysql-bin.000002
            Position: 276
        Binlog_Do_DB: 
    Binlog_Ignore_DB: 
    mysql> unlock tables;

vim /etc/my.cnf:

    :::bash
    # as master
    #开启二进制日志，并且名称为 /var/log/mysql/mysql-bin.***
    log-bin=mysql-bin
    read-only=0  #主机读写权限，读写都可以
    binlog-do-db=hello   #记录日志的数据库：需要的备份数据，多个写多行
    binlog-ignore-db=mysql #不记录日志的数据库：不需要备份的数据库，多个写多行
    binlog-ignore-db=test
    binlog-ignore-db=information_schema

    # 自增字段偶数递增，防止冲突（2, 4, 6, ...,）
    auto-increment-increment = 2  # 每次递增的步长
    auto-increment-offset = 2  # 初始值

service mysqld restart

#### slave:

    :::bash
    mysql> slave stop;

    mysql>  CHANGE MASTER TO MASTER_HOST='192.168.100.166', MASTER_USER='backup', MASTER_PASSWORD='yNZE7fK9*@aMA?*ppF', MASTER_LOG_FILE='mysql-bin.000002, MASTER_LOG_POS=276';

    mysql> slave start;

vim /etc/my.cnf

    :::bash
    # as slave
    master-host=192.168.100.166  # master
    master-user=backup  # 刚才在 master1 上设置的用户名密码
    master-password=yNZE7fK9*@aMA?*ppF  # password
    master-port=3306   # master1 mysql port
    master-connect-retry=60 #如果从服务器发现主服务器断掉，重新连接的时间差(秒)
    replicate-do-db =hello #只复制某个库，多个写多行
    replicate-ignore-db=mysql #不复制某个库
    replicate-ignore-db=test
    replicate-ignore-db=information_schema
    relay-log=mysqld-relay-bin  # 开启日志中继
    log-slave-updates  # slave将复制事件写进自己的二进制日志

serivce mysqld restart


#### 测试

master2:

    :::bash
    mysql> use hello;    
    mysql> insert into test set id=2;
    mysql> select * from test;
    +------+
    | id   |
    +------+
    |    1 | 
    |    2 | 
    +------+
    2 rows in set (0.00 sec)
    mysql> show master status\G;
    *************************** 1. row ***************************
                File: mysql-bin.000003
            Position: 187
        Binlog_Do_DB: hello
    Binlog_Ignore_DB: mysql,test,information_schema
    1 row in set (0.00 sec)

slave:

    :::bash
    mysql> show slave status \G;
    *************************** 1. row ***************************
                Slave_IO_State: Waiting for master to send event
                    Master_Host: 192.168.100.166
                    Master_User: backup
                    Master_Port: 3306
                Connect_Retry: 60
                Master_Log_File: mysql-bin.000003
            Read_Master_Log_Pos: 187
                Relay_Log_File: mysqld-relay-bin.000003
                Relay_Log_Pos: 324
        Relay_Master_Log_File: mysql-bin.000003
            Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
                Replicate_Do_DB: hello
            Replicate_Ignore_DB: mysql,test,information_schema
                    Last_Errno: 0
                    Last_Error: 
                Skip_Counter: 0
            Exec_Master_Log_Pos: 187
                Relay_Log_Space: 324
                Until_Condition: None
                Until_Log_File: 
                Until_Log_Pos: 0
        Seconds_Behind_Master: 0

    mysql> use hello;

    mysql> select * from test;
    +------+
    | id   |
    +------+
    |    1 | 
    |    2 | 
    +------+
    2 rows in set (0.00 sec)

<!--less /var/log/mysqld.log-->


最后的配置文件

master1:

    :::bash
    # /etc/my.cnf
    [mysqld]

    # as master
    server-id=1    #主机id，整数
    #开启二进制日志，并且名称为 /var/lib/mysql/mysql-bin.***
    log-bin=mysql-bin
    read-only=0  #主机读写权限，读写都可以
    binlog-do-db=hello   #记录日志的数据库：需要的备份数据，多个写多行
    # binlog-do-db=hello2
    binlog-ignore-db=mysql #不记录日志的数据库：不需要备份的数据库，多个写多行
    binlog-ignore-db=test
    binlog-ignore-db=information_schema

    # as slave
    master-host=192.168.100.166  # master
    master-user=backup  # 刚才在 master1 上设置的用户名密码
    master-password=yNZE7fK9*@aMA?*ppF  # password
    master-port=3306   # master1 mysql port
    master-connect-retry=60 #如果从服务器发现主服务器断掉，重新连接的时间差(秒)
    replicate-do-db =hello #只复制某个库，多个写多行
    replicate-ignore-db=mysql #不复制某个库
    replicate-ignore-db=test
    replicate-ignore-db=information_schema
    relay-log=mysqld-relay-bin  # 开启日志中继
    log-slave-updates  # slave将复制事件写进自己的二进制日志

    # 自增字段奇数递增，防止冲突（1, 3, 5, ...,）
    auto-increment-increment = 2  # 每次递增的步长
    auto-increment-offset = 1  # 初始值

master2:

    :::bash
    # /etc/my.cnf
    [mysqld]

    # as slave
    server-id=2
    log-bin=mysql-bin
    master-host=192.168.100.191  # master1
    master-user=backup  # 刚才在 master1 上设置的用户名密码
    master-password=yNZE7fK9*@aMA?*ppF  # password
    master-port=3306   # master1 mysql port
    master-connect-retry=60 #如果从服务器发现主服务器断掉，重新连接的时间差(秒)
    replicate-do-db =hello #只复制某个库，多个写多行
    replicate-ignore-db=mysql #不复制某个库
    replicate-ignore-db=test
    replicate-ignore-db=information_schema
    relay-log=mysqld-relay-bin  # 开启日志中继
    log-slave-updates  # 示slave将复制事件写进自己的二进制日志

    # as master
    #开启二进制日志，并且名称为 /var/lib/mysql/mysql-bin.***
    log-bin=mysql-bin
    read-only=0  #主机读写权限，读写都可以
    binlog-do-db=hello   #记录日志的数据库：需要的备份数据，多个写多行
    # binlog-do-db=hello2
    binlog-ignore-db=mysql #不记录日志的数据库：不需要备份的数据库，多个写多行
    binlog-ignore-db=test
    binlog-ignore-db=information_schema

    # 自增字段偶数递增，防止冲突（2, 4, 6, ...,）
    auto-increment-increment = 2  # 每次递增的步长
    auto-increment-offset = 2  # 初始值



## 参考

* [MYSQL 主从服务器配置 | 无影的博客](http://www.d5s.cn/archives/95)
* [Mysql 数据库双机热备的配置 - 51CTO.COM](http://database.51cto.com/art/200510/8434.htm)
* [MySQL Master-Master Replication of ALL databases. How? - Server Fault](http://serverfault.com/questions/268627/mysql-master-master-replication-of-all-databases-how)
* [MySQL :: MySQL 5.1 Reference Manual :: 16 Replication](http://dev.mysql.com/doc/refman/5.1/en/replication.html)
* [MySqL的主从复制和读写分离 - ZhouLS的个人空间 - 开源中国社区](file:///D:/Settings/Mozilla/ScrapBook/data/20130522165305/index.html)
* [高性能Mysql主从架构的复制原理及配置详解 - guisu，程序人生。 - 博客频道 - CSDN.NET](http://blog.csdn.net/hguisu/article/details/7325124)
* [MySQL master slave 安装部署及常见问题-桥-搜狐博客](http://mvbridge.blog.sohu.com/172644721.html)
<!--* [)-->
<!--https://groups.google.com/forum/#!topic/django-users/0RiRw6jlnAs-->
* [三台Mysql实现数据同步及主从模式 - 情感个人博客站 - Powered by Sablog-X](http://blog.phpok.com/archives/29/)
* [MYSQL中的auto_increment_increment和auto_increment_offset - 朝着梦想 渐行前进 - 博客频道 - CSDN.NET](http://blog.csdn.net/wh62592855/article/details/6726724)
* [auto increment - How is the MySQL auto_increment step size determined - Stack Overflow](http://stackoverflow.com/questions/8262863/how-is-the-mysql-auto-increment-step-size-determined)
* [MySQL :: MySQL 5.1 Reference Manual :: 16.1.3.2 Replication Master Options and Variables](http://dev.mysql.com/doc/refman/5.1/en/replication-options-master.html#sysvar_auto_increment_increment)
