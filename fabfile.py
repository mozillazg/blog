#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import task
from fabric.api import local
from fabric.api import lcd
from fabric.api import settings


@task
def make_html():
    """生成 html 文件"""
    local('pelican content -o output -s pelicanconf.py')


@task
def re_make_html():
    """重新生成 html 文件（删除旧 html 文件）"""
    local('pelican -d output')
    local('pelican content -o output -s pelicanconf.py')


@task
def auto_reload():
    """生成 html 文件，并监视文件变化。
    有变化时，再次生成 html 文件
    """
    local('pelican content -o output -s pelicanconf.py -r')


@task
def push():
    """发布到 github"""
    with settings(warn_only=True):
        local('git add -A')
        local('git commit -m "push"')
        local('git push')
        with lcd('output'):
            local('git add -A')
            local('git commit -m "push"')
            local('git push')

@task
def server():
    """运行一个简单的 http 服务器"""
    with lcd('output'):
        local('python -m SimpleHTTPServer')
