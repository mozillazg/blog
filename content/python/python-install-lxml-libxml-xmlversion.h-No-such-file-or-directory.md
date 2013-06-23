Title: [python]解决编译安装 lxml 时提示：libxml/xmlversion.h:No such file or directory
Date: 2013-06-23
Tags: python, lxml, libxml, libxslt
Slug: python-install-lxml-libxml-xmlversion.h-No-such-file-or-directory


编译安装 lxml 时，出现了如下错误：

> libxml/xmlversion.h: No such file or directory


出现这个错误是因为有些依赖包没有安装：

* libxml2
* libxml2-dev
* libxslt
* libxslt-dev

只要安装好要上面的依赖包就可以了
