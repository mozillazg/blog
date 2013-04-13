Title: [django]线上部署后，访问 admin 时出现“DoesNotExist at /admin/ Site matching query does not exist.”错误
Date: 2013-02-19
Tags: django, python
Slug: django-online-server-admin-doesnotexist-at-admin


将 django 项目部署到服务器后，访问 admin 时出现如下错误：

    :::html
    DoesNotExist at /admin/
    Site matching query does not exist.

上网搜索后，参考 <http://stackoverflow.com/questions/9736975/django-admin-doesnotexist-at-admin> 修复了该问题，下面记录一下解决过程。

两种解决办法：

* 第一种办法是：编辑 settings.py 文件，从 `INSTALLED_APPS` 配置项中移除 `'django.contrib.sites',`。

* 第二种办法：通过 `python manage.py shell` 为 Site model 添加一条记录（将网站的域名添加进去）：

        :::console
        $ python manage.py shell
 
        >>> from django.contrib.sites.models import Site
        >>> Site.objects.create(pk=1, domain='tumblr.3sd.me', name='tumblr.3sd.me')
        <Site: tumblr.3sd.me>

我使用第二种办法解决了我的问题

## 参考

* [django admin DoesNotExist at /admin/ - Stack Overflow](http://stackoverflow.com/questions/9736975/django-admin-doesnotexist-at-admin)
