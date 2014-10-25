Title: [python]第三方模块 python-dateutil：扩展并增强 datetime 模块的功能
Date: 2013-06-09
Tags: python-third-party-model, python, python-dateutil, dateutil, datetime
Slug: python-third-party-model-python-dateutil

## 简介

> 扩展并增强 datetime 模块的功能。支持 Python 2.3+。

## 主页

<http://labix.org/python-dateutil>

## 文档

<http://labix.org/python-dateutil>

## 安装

    :::bash
    pip install python-dateutil

    # or
    # download from https://pypi.python.org/pypi/python-dateutil
    python setup.py install

## 简单使用

获取历史上的今天，上个月的今天，下个月的今天 [link](http://labix.org/python-dateutil#head-6a1472b7c74e5b8bab7784f11214250d34e09aa5)：

    :::python
    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>>
    >>> today
    datetime.date(2013, 6, 9)
    >>>
    >>> today + relativedelta(years=-1)
    datetime.date(2012, 6, 9)
    >>>
    >>> today + relativedelta(months=-1)
    datetime.date(2013, 5, 9)
    >>>
    >>> today + relativedelta(months=1)
    datetime.date(2013, 7, 9)

更多用法请查看官方文档：<https://pypi.python.org/pypi/python-dateutil>
