Title: 在 CentOS 6 上编译安装 git 2.x
Slug: install-git-2-on-centos-6
Date: 2015-08-15

CentOS 6 上通过 yum 安装的是 git 1.x 版本，
本文将讲述如何在 CentOS 6 上编译安装 git 2.x 。下面是详细步骤:

1. 安装编译所需的环境依赖

    sudo yum -y install wget curl-devel expat-devel gettext-devel openssl-devel zlib-devel perl-ExtUtils-MakeMaker gcc asciidoc xmlto docbook2x
    
    # 解决编译时出现的 /bin/sh: line 1: docbook2x-texi: command not found
    ln -s /usr/bin/db2x_docbook2texi /usr/bin/docbook2x-texi

2. 下载 [git 2.x 源码包](https://www.kernel.org/pub/software/scm/git/)

    cd /tmp
    wget https://www.kernel.org/pub/software/scm/git/git-2.5.0.tar.gz

3. 解压，编译，安装

    cd /tmp
    tar zxvf git-2.5.0.tar.gz 
    cd git-2.5.0/
    make configure
    ./configure --prefix=/usr/local
    make all doc info
    make install install-doc install-html install-info

4. 配置 `PATH` 环境变量

    echo 'export PATH=/usr/local/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc

5. ;)

    $ git --version
    git version 2.5.0


## 参考资料

* [Git - Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)