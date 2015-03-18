title:修复安装 psycopg2 时出现“pg_config executable not found”错误
slug: fix-install-psycopg2-raise-pg_config-excutable-not-found
tag: psycopg2, postgresql
date: 2015-03-15

错误详情：

    Running setup.py egg_info for package psycopg2
        
        Error: pg_config executable not found.
        
        Please add the directory containing pg_config to the PATH
        or specify the full executable path with the option:
        
            python setup.py build_ext --pg-config /path/to/pg_config build ...
        
        or with the pg_config option in 'setup.cfg'.

出错的原因是因为找不到 `pg_config` 命令。

在我的机器上 `pg_config` 程序在 `/usr/pgsql-9.4/bin/` 目录下，只需让 `pg_config` 命令可以被找到就可以了：

    ln -s /usr/pgsql-9.4/bin/pg_config /usr/bin/pg_config

