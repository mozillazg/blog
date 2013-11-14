Title: [linux]编译 aria2c 时，出现 C compiler cannot create executables 错误
Date: 2013-05-11
Tags: linux
Slug: linux-compile-aria2c-error-C-compiler-cannot-create-executables

编译安装 aria2c 时，出现了如下错误：

    [root@dev aria2-1.17.1]# ./configure
    checking for gcc... gcc
    checking whether the C compiler works... no
    configure: error: in `/root/temp/aria2-1.17.1':
    configure: error: C compiler cannot create executables
    See `config.log' for more details

解决办法： 清空 LIBS 及 CFLAGS 变量的值

    [root@dev aria2-1.17.1]# export LIBS=
    [root@dev aria2-1.17.1]# 
    [root@dev aria2-1.17.1]# export CFLAGS=
    [root@dev aria2-1.17.1]# ./configure
    checking for gcc... gcc
    checking whether the C compiler works... yes
