title: 如何在 centos 7 上安装 postgresql 9.5
slug: install-postgresql-9.5-on-centos-7
tags: centos, postgresql
date: 2016-01-26


1. 安装 yum 源（地址从 <http://yum.postgresql.org/repopackages.php> 获取）

        sudo yum install http://yum.postgresql.org/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-2.noarch.rpm

2. 安装 `postgresql95-server` 和 `postgresql95-contrib`

        sudo yum install postgresql95-server postgresql95-contrib
   安装后，可执行文件在 `/usr/pgsql-9.5/bin/`， 数据和配置文件在 `/var/lib/pgsql/9.5/data/`

3. 初始化数据:

        sudo /usr/pgsql-9.5/bin/postgresql95-setup initdb

4. 默认不支持密码认证，修改 `pg_hab.conf` 将 `ident` 替换为 `md5` （可选）

        sudo vim /var/lib/pgsql/9.5/data/pg_hba.conf


5. 微调其他配置项（可选）

        sudo vim /var/lib/pgsql/9.5/data/postgresql.conf

6. 启动服务：

        sudo systemctl start postgresql-9.5.service

7. 开机自动启动:

        sudo systemctl enable postgresql-9.5.service


## 参考

* [PostgreSQL: Linux downloads \(Red Hat family\)](http://www.postgresql.org/download/linux/redhat/)
* [PostgreSQL: Documentation: 9.5: The pg_hba.conf File](http://www.postgresql.org/docs/9.5/static/auth-pg-hba-conf.html)