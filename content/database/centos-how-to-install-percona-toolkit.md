Title: [linux] CentOS 下安装 percona-toolkit
Date: 2014-03-24
Tags: centos, mysql
Slug: centos-how-to-install-percona-toolkit

[percona-toolkit](http://www.percona.com/doc/percona-toolkit/) 是一组高级命令行工具的集合，
用来执行各种复杂和麻烦的 MySQL 操作。

下面记录一下在 CentOS 下如何通过 rpm 安装 percona-toolkit:

1. 安装依赖             
    ``yum install perl perl-IO-Socket-SSL perl-Time-HiRes``

2. 下载 rpm 包             
    ``wget percona.com/get/percona-toolkit.rpm``

3. 安装 rpm 包         
   ``rpm -ivh percona-toolkit-*.rpm``


---EOF---
