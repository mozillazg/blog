Title: Cygwin 中的软件包管理工具： apt-cyg
Date: 2013-06-23
Tags: Cygwin
Slug: cygwin-install-packages-by-apt-cyg

apt-cyg 可以在 Cygwin 中实现类似 linux 下的 `yum` 或 `apt-get` 的功能。

## 主页

<http://code.google.com/p/apt-cyg/>

## 安装

    :::bash
    $ svn --force export http://apt-cyg.googlecode.com/svn/trunk/ /bin/
    $ chmod +x /bin/apt-cyg

## 使用

* `apt-cyg install <package names>      # 安装软件包`

        :::bash
        apt-cyg install bind-utils

* `apt-cyg remove <package names>      # 移除软件包`
* `apt-cyg update     # 更新 setup.ini 文件`
* `apt-cyg show      # 列出已安装的软件包`
* `apt-cyg find <pattern(s)>     # 查找名称匹配的软件包`
* `apt-cyg describe <pattern(s)>     # 查找描述匹配的软件包`
* `apt-cyg packageof <commands or files>     # 定位命令或文件属于哪个软件包`

        :::bash
        $ apt-cyg packageof dig
        Found usr/bin/dig in the package bind-utils

* `apt-cyg     # 显示帮助信息`

        :::bash
        $ apt-cyg
        apt-cyg: Installs and removes Cygwin packages.
        "apt-cyg install <package names>" to install packages
        "apt-cyg remove <package names>" to remove packages
        "apt-cyg update" to update setup.ini
        "apt-cyg show" to show installed packages
        "apt-cyg find <patterns>" to find packages matching patterns
        "apt-cyg describe <patterns>" to describe packages matching patterns
        "apt-cyg packageof <commands or files>" to locate parent packages
        Options:
        --mirror, -m <url> : set mirror
        --cache, -c <dir>  : set cache
        --file, -f <file>  : read package names from file
        --noupdate, -u     : don't update setup.ini from mirror
        --help
        --version

