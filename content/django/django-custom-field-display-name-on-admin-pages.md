Title: [django]自定义字段在后台显示的名称
Date: 2013-04-13
Tags: python, django, verbose_name
Slug: django-custom-field-display-name-on-admin-pages

默认情况下后台显示的字段名称是依据 models.py 中的字段名来显示的。
下面要做的就是自定义字段在后台的显示名称（比如显示为中文）。

只需在定义字段的时候定义参数 verbose_name 的值即可。

对于普通字段：

    :::python
    name = models.CharField(u'软件名称', max_length=200)

对于 OneToOneField, ForeignKey 及 ManyToManyField ：

    :::python
    foo = models.OneToOneField(Foo, verbose_name=u'foobar')

    software = models.ForeignKey(SoftWare, verbose_name=u'软件名称')

    author = models.ManyToManyField(Author, verbose_name=u'作者')

这样之后，后台就会会显示我们定义的名称。

![image](/static/images/2013-04-13-001.png)

## 参考

[Models | Django documentation | Django](https://docs.djangoproject.com/en/dev/topics/db/models/#verbose-field-names)
