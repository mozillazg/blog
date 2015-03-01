Title: [linux]查看通过 yum 安装的包的文件安装位置
Date: 2015-02-28
Slug: linux-find-files-from-installed-yum-package
Tags: yum

可以通过 `yum-utils` 工具查看所安装的包的文件位置

    $ sudo yum install yum-utils
    $ sudo repoquery --list python27
    /usr/bin/pydoc27
    /usr/bin/python2.7
    /usr/share/doc/python27-2.7.9
    /usr/share/doc/python27-2.7.9/LICENSE
    /usr/share/doc/python27-2.7.9/README
    /usr/share/man/man1/python2.1.gz
    /usr/share/man/man1/python2.7.1.gz

