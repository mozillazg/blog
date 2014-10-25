Title: [database]Windows 下安装使用 MongoDB（hello world）
Date: 2013-02-25
Tags: MongoDB，数据库
Slug: hello-mongodb-on-windows


## 安装

从 <http://www.mongodb.org/downloads> 下载 mongodb 压缩包，
解压到某个目录下，假设最后的目录路径为：c:\mongodb\，将 `;c:\mongodb\bin` 追加到环境变量 path 中。

新建一个目录用来存放数据库文件，比如该目录为：c:\mongodb\data 。

## 使用

### 启动服务器

命令行下执行：

    :::console
    mongod --dbpath c:\mongodb\data

### hello world

命令行下执行：

    :::console
    mongo

进入数据库终端（默认是连接到 test 数据库）：

    :::console
    > var x = "hello world"
    > x
    hello world
    >

## 参考

* [The MongoDB Manual — MongoDB Manual](http://docs.mongodb.org/manual/)
* [结合使用 MongoDB 和 Django](http://www.ibm.com/developerworks/cn/opensource/os-django-mongo/)
