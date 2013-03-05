Title: [django] Variables and attributes may not begin with underscores
Date: 2013-01-17
Author: mozillazg
Category: django
Tags: python, django
Slug: django-variables-and-attributes-may-not-begin-with-underscores

当尝试在模板中**调用以下划线开头的对象时**，会报如下类似错误：

> TemplateSyntaxError at /
>
> Variables and attributes may not begin with underscores: 'user.\_meta.get\_field('name').help\_text'

解决方法就是，将调用以下划线开头的对象的操作封装到模板过滤器中。

## 如何创建自定义模板过滤器

在 models.py 文件所在目录新建一个 templatetags 目录:

    hello/
        models.py
        templatetags/
            hello_extras.py
            __init__.py
        views.py

hello\_extras.py 中保存着我们自定义的模板过滤器。

在 hello\_extras.py 文件的开头需要包含如下代码：


    :::python
    from django import template

    register = template.Library()

本例中我们将定义一个 help\_text 过滤器，用于获取 models 中字段的 help\_text 的值，所以 hello\_extras.py 的内容为：

    :::python
    from django import template

    register = template.Library()


    @register.filter
    def help_text(value, arg):
        return value._meta.get_field(arg).help_text

在模板中使用自定义过滤器时，要记得导入过滤器：

    :::django
    {% load hello_extras %}

本例的模板文件：

    :::html+django
    {% load hello_extras %}

    {% for user in users %}
      <p>{{ user|help_text:"name" }}： {{ user.name }}</p>
    {% endfor %}

models 文件节选：

    :::python
    class User(models.Model):
        name = models.CharField(max_length=50, help_text=u'姓名')

模板渲染结果：

> 姓名：tom
>
> 姓名：jim
>
> 姓名：eric

测试项目下载：[mysite.tar.gz](/static/downloads/2013.01.17.mysite.tar.gz) ，测试环境：django 1.4.3。

## 参考

* [access django model fields label and help_text - Stack Overflow](http://stackoverflow.com/questions/4279905/access-django-model-fields-label-and-help-text)
* [Model name of objects in django templates - Stack Overflow](http://stackoverflow.com/questions/6571649/model-name-of-objects-in-django-templates)
* [Custom template tags and filters | Django documentation | Django](https://docs.djangoproject.com/en/dev/howto/custom-template-tags/)
