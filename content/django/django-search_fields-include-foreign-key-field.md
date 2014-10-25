Title: [django]如何在 search_fields 中包含外键字段
Date: 2013-04-13
Tags: python, django, search_fields, foreign-key
Slug: django-search_fields-include-foreign-key-field

我们知道在 admin.py 中定义 search_fields 可以控制在后台管理界面中能够搜索的字段。

但是，当 search_fields 包含外键字段时，此时进行搜索会报错：

> TypeError at /admin/hello/foo/
>
> Related Field has invalid lookup: icontains

解决的办法是修改 search_fields 中的外键字段名称。

将 search_fields 中的外键字段改为 `foreign_key__related_fieldname` 这种形式就可以了。
这种用法适用于 ForeignKey 及 ManyToManyField 。

models.py

    :::python
    class Hello(models.Model):
        name = models.CharField(max_length=100)

        #...


    class Foo(models.Model):
        hello = models.ForeignKey(Hello)

admin.py

    :::python
    class FooAdmin(admin.ModelAdmin):
        search_fields = ('hello__name',)  # 搜索 Hello 中的 name 字段


## 参考

* [The Django admin site | Django documentation | Django](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)
