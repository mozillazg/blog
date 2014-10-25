Title: [python]设置 gunicorn 绑定多个地址
Date: 2013-07-08
Tags: python, gunicorn
Slug: python-gunicorn-multiple-address

[TOC]

有两种方式可以设置 gunicorn  绑定多个地址。

## 命令行参数

    :::bash
    gunicorn -b unix:/tmp/gunicorn.sock -b 127.0.0.1:8000 wsgi:app

    gunicorn --bind unix:/tmp/gunicorn.sock --bind 127.0.0.1:8000 wsgi:app

## 配置文件

    :::python
    bind = 'unix:/tmp/gunicorn.sock','127.0.0.1:8000','0.0.0.0:1234'


## 参考

* [Congiuration - gunicorn documentation](http://docs.gunicorn.org/en/latest/configure.html)
* [allows gunicorn to bind to multiple address - b7b51ad - benoitc/gunicorn - GitHub](https://github.com/benoitc/gunicorn/commit/b7b51adf13e92044211b267ba07e3498585f219a)
