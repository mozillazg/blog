Title: [django]使用 nginx + fastcgi 部署 django
Date: 2013-01-31
Tags: python, django, nginx, fastcgi
Slug: django-deploying-with-fastcgi-nginx

本文测试环境：linux mint，python 2.7，django 1.4

## 安装依赖

安装 nginx

$ sudo apt-get install nginx


## 设置 django

本例中项目名为 bbs:

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

    TEMPLATE_DIRS = (
        '/var/www/bbs/templates',  # 这里要是绝对路径
    )

    STATIC_ROOT = '/var/www/bbs/static'

配置 wsgi.py:

    import os
    import sys

    sys.path.append('/var/www/bbs/')  # 项目目录的绝对路径

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbs.settings")


本例中使用 /var/www/bbs/static/ 保存静态文件，使用命令
`python manage.py collectstatic` 收集静态文件 <del>，然后将输出的静态文件保存到
 /var/www/bbs/static/ 目录下</del>。

最终 /var/www/bbs/static/ 目录结构应该类似（admin 目录及其目录下文件一定要有）：

    $ tree static -d
    static
    |-- admin
    |   |-- css
    |   |-- img
    |   |   `-- gis
    |   `-- js
    |       `-- admin
    `-- css

## 配置 nginx

    $ vim /etc/nginx/conf.d/bbs.conf

    server {
        listen   80;
        server_name bbs.com;
        access_log /var/log/nginx/bbs.access.log;
        error_log /var/log/nginx/bbs.error.log;

        location / {
            # host and port to fastcgi server
            fastcgi_pass 127.0.0.1:8081;  # host:port
            fastcgi_param PATH_INFO $fastcgi_script_name;
            fastcgi_param REQUEST_METHOD $request_method;
            fastcgi_param QUERY_STRING $query_string;
            fastcgi_param CONTENT_TYPE $content_type;
            fastcgi_param CONTENT_LENGTH $content_length;
            fastcgi_pass_header Authorization;
            fastcgi_intercept_errors off;
            fastcgi_param SERVER_PROTOCOL $server_protocol;
            fastcgi_param SERVER_PORT $server_port;
            fastcgi_param SERVER_NAME $server_name;
            }

        location /static/ {  # STATIC_URL
            alias /var/www/bbs/static/;  # STATIC_ROOT 
        }

        location /meida/ {  # MEDIA_URL
            alias /var/www/bbs/media/;  # MEDIA_ROOT 
        }

        # 如果 admin 文件夹在 static 目录下，可以不配置下面项
        location /static/admin/ {  # admin static file
            alias /var/www/bbs/static/admin/;
        }
    }

以 fastcgi 的形式运行 django 项目（注意：这里的 host 及 port 要与上面配置的一样）：

    $ python manage.py runfcgi host=127.0.0.1 port=8081

终止 fastcgi 话，查看相关进程然后结束掉即可：


    $ ps aux | grep cgi
    mzg       2500  0.0  5.0  34860 12480 ?        S    15:43   0:00 python manage.py runfcgi host=127.0.0.1 port=8081
    mzg       2501  0.0  4.7  34860 11784 ?        S    15:43   0:00 python manage.py runfcgi host=127.0.0.1 port=8081
    mzg       2502  0.0  4.7  34860 11788 ?        S    15:43   0:00 python manage.py runfcgi host=127.0.0.1 port=8081

    $ sudo kill 2500
    $ ps aux | grep cgi
    mzg       2745  0.0  0.3   5128   876 pts/1    S+   16:05   0:00 grep --colour=auto cgi

测试环境的话，由于域名是虚构的，所以要配置 /etc/hosts 添加 `127.0.0.1  bbs.com `：

    $ sudo vim /etc/hosts
    $ tail /etc/hosts
    127.0.0.1   bbs.com

更改目录权限：

    $ sudo chown www-data:www-data /var/www/bbs -R

启动 nginx 服务

    $ service nginx restart

结果：

![前台](/static/images/2013-1-django-deploying-nginx-01.png)

![后台](/static/images/2013-1-django-deploying-nginx-02.png)

后续 linux 相关的工作暂且不表：

* <del>配置项目目录访问权限</del>
* 配置 iptables ，开放 80 端口

测试项目及配置文件可以从 [这个代码仓库](https://github.com/mozillazg/django-simple-projects/tree/master/projects/bbs) 中获取。

## 参考

* [How to use Django with FastCGI, SCGI, or AJP | Django documentation](https://docs.djangoproject.com/en/dev/howto/deployment/fastcgi/)
* [David McLaughlin » Complete guide to deploying django on Ubuntu with nginx, FastCGI and MySQL](http://www.dmclaughlin.com/2008/11/03/complete-guide-to-deploying-django-on-ubuntu-with-nginx-fastcgi-and-mysql/)
