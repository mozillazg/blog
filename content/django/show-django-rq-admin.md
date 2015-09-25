title: 配置 django-rq 在 admin 后台显示队列管理页面
slug: how-to-configure-for-show-django-rq-admin
date: 2015-09-25
tags: django-rq

效果：

![django-rq-admin-1](/static/images/django/django-rq-admin-1.png)

![django-rq-admin-2](/static/images/django/django-rq-admin-2.png)

![django-rq-admin-2](/static/images/django/django-rq-admin-3.png)


详细步骤如下：

1. 配置 settings.py

        RQ_SHOW_ADMIN_LINK = True

2. 配置 urls.py

        urlpatterns += patterns(
            '',
            (r'^admin/django-rq/', include('django_rq.urls')),
        )

3. Done!

Demo 项目： [django_rq_admin](https://github.com/mozillazg/django-simple-projects/tree/master/projects/django_rq_admin)


## 参考资料

* [https://github.com/ui/django-rq](https://github.com/ui/django-rq)