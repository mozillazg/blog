Title: [django]自定义 model 在后台显示的名称
Date: 2013-04-13
Tags: python, django, verbose_name,verbose_name_plural
Slug: django-custom-model-display-name-on-admin-pages

默认情况下后台显示的 model 名称是依据 models.py 中的 class 名称来显示的。
下面要做的就是自定义 model 在后台的显示名称（比如显示为中文）。

只需在 model 类中定义 Meta 类并增加属性 verbose_name/verbose_name_plural 即可。

verbose_name 定义的是单数名称， verbose_name_plural 定义的是复数名称。

    :::python
    class Hello(models.Model):
        #...

        class Meta:
            verbose_name = u'software'
            verbose_name_plural = u'软件信息'

![image](/static/images/2013-04-13-002.png)


## 参考

[Model Meta options | Django documentation | Django](https://docs.djangoproject.com/en/dev/ref/models/options/#verbose-name)
