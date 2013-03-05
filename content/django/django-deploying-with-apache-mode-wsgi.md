Title: [django]使用 apache + mod_wsgi 部署 django
Date: 2013-01-31
Tags: python, django, apache, mod_wsgi
Slug: django-deploying-with-apache-mode-wsgi

本文测试环境：linux mint，python 2.7，django 1.4

## 安装依赖

    :::console
    $ sudo apt-get install apache2
    $ sudo apt-get install libapache2-mod-wsgi

## 设置 django

本例中项目名为 bbs:

    :::console
    $ pwd
    /var/www/bbs

    $ tree . -d
    .
    |-- bb  # 应用
    |-- bbs  # settings.py wsgi.py
    |-- static  # 静态文件
    |   `-- css
    `-- templates  # TEMPLATE_DIRS

配置 settings：

    :::python
    TEMPLATE_DIRS = (
        '/var/www/bbs/templates',  # 这里要是绝对路径
    )

    STATIC_ROOT = '/var/www/bbs/static'

配置 wsgi.py:

    :::python
    import os
    import sys

    sys.path.append('/var/www/bbs/')  # 项目目录的绝对路径

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbs.settings")

本例中使用 /var/www/bbs/static/ 保存静态文件，使用命令
`python manage.py collectstatic` 收集静态文件。

最终 /var/www/bbs/static/ 目录结构应该类似（admin 目录及其目录下文件一定要有）：

    :::console
    $ tree static -d
    static
    |-- admin
    |   |-- css
    |   |-- img
    |   |   `-- gis
    |   `-- js
    |       `-- admin
    `-- css

## 配置 apache

    :::console
    $ sudo vim /etc/apache2/conf.d/bbs.conf


    WSGIPythonPath /var/www/bbs
    <VirtualHost *:80>
        ServerName bbs.com

        Alias /static/ /var/www/bbs/static/

        <Directory /var/www/bbs/static>
        Order deny,allow
        Allow from all
        </Directory>

        WSGIScriptAlias / /var/www/bbs/bbs/wsgi.py
        <Directory /var/www/bbs/bbs>
        <Files wsgi.py>
        Order allow,deny
        Allow from all
        </Files>
        </Directory>
    </VirtualHost>

更改目录权限：

    :::console
    $ sudo chown www-data:www-data /var/www/bbs -R

启动 apache 服务

    :::console
    $ service apache2 restart


结果：

![前台](/static/images/2013-1-django-deploying-apache-01.png)

![后台](/static/images/2013-1-django-deploying-apache-02.png)

后续 linux 相关的工作暂且不表：

* <del>配置项目目录访问权限<del>
* 配置 iptables ，开放 80 端口

测试项目及配置文件可以从 [这个代码仓库](https://github.com/mozillazg/django-simple-projects/tree/master/projects/bbs) 中获取。

## 参考

* [How to use Django with Apache and mod_wsgi | Django documentation](https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/)
* [IntegrationWithDjango - modwsgi - How to use Django with mod_wsgi. - Python WSGI adapter module for Apache.](http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango)
