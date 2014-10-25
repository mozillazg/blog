#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import task
from fabric.api import local
from fabric.api import lcd
from fabric.api import settings


@task
def make_html():
    """generate the web site"""
    with settings(warn_only=True):
        local('pelican content -o output -s pelicanconf.py -D')


@task
def re_make_html():
    """regenerate the web site"""
    with settings(warn_only=True):
        local('pelican -d output')
        local('pelican content -o output -s pelicanconf.py -D')


@task
def auto_reload():
    """generate the web site(auto reload)"""
    with settings(warn_only=True):
        local('pelican content -o output -s pelicanconf.py -r -D')


@task
def push():
    """push to github"""
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
    """run http server at http://0.0.0.0:8000"""
    with settings(warn_only=True):
        with lcd('output'):
            local('python -m SimpleHTTPServer')
