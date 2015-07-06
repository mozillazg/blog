配置应用在 django admin 中显示的名称和顺序
--------------------------------------------- 

:date: 2015-07-06
:slug: django-how-to-change-app-name-and-sort-app-on-admin-site


在 Django 1.7 之前，要想修改应用在 admin 中的名称的话，必须得 hack Django 代码。
好消息是 Django 1.7+ 支持 `配置应用的名称等信息 <https://docs.djangoproject.com/en/1.8/ref/applications/#configuring-applications>`__ 了。先看效果:

|image|

下面详细讲一下配置方法。

1. 定义一个继承 AppConfig 的子类::

        # foo/apps.py
        from django.apps import AppConfig
        
        class FooConfig(AppConfig):
            name = 'foo'  # app 名称，可以 import 的路径, 比如 foo.bar.foobar
            verbose_name = '1名称1'   # 后台显示的名称

2. 然后应用配置，有两种方式:

   1. 在 ``__init__.py`` 中指定 ``default_app_config`` ::

            # foo/__init__.py
            default_app_config = 'foo.apps.FooConfig'

   2. 配置 ``INSTALLED_APPS`` ::
   
            INSTALLED_APPS = (
                # ...
                'foo.apps.FooConfig',
                # ....
           )
            
Demo 下载： https://github.com/mozillazg/django-simple-projects/tree/master/projects/custom_app_name


参考资料
~~~~~~~~~~~

* `Applications | Django documentation | Django <https://docs.djangoproject.com/en/1.8/ref/applications/#configuring-applications>`__

.. |image| image:: /static/images/django/2015-07/app-config-01.png