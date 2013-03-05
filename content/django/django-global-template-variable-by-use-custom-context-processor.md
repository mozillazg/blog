Title: [django]使用自定义 context processor 实现模板全局变量
Date: 2013-01-23
Tags: python, django
Slug: django-global-template-variable-by-use-custom-context-processor


本文使用的是 django 1.4.3。


## 写一个 context processor 函数

可以把这个函数放在项目的任何地方，本文是放在应用目录下的 context\_processors.py 文件中：

    :::python
    from hello.models import Category


    def categories(request):  # 只有一个参数（HttpRequeset 对象）
        all_categories = Category.objects.all()
        context = {'categories': all_categories}

        return context  # 返回值必须是个字典

注意：context processor 函数只有一个参数，即 HttpRequest 对象，并且函数的返回值必须是个字典。

## 修改 settings 文件

修改 TEMPLATE\_CONTEXT\_PROCESSORS 选项值，添加新建的 context processor 函数。
如果没有 TEMPLATE\_CONTEXT\_PROCESSORS 这一项的话，需要把它添加到 settings 文件中。
各版本的 django 的 TEMPLATE\_CONTEXT\_PROCESSORS 的默认值不一样，具体见 [TEMPLATE\_CONTEXT\_PROCESSORS](https://docs.djangoproject.com/en/1.4/ref/settings/#template-context-processors)。

    :::python
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'hello.context_processors.categories',  # 自定义的 context processors 函数
    )

## 在 views 中使用

    :::python
    from django.template import RequestContext
    from django.template import loader


    # 第一种用法
    def index(request):
        return render_to_response('index.html', {'foo': 'bar'},
                                  context_instance=RequestContext(request))

    # 第二种用法
    def hello(request):
        t = loader.get_template('index.html')
        c = RequestContext(request, {'foo': 'bar'})
        return HttpResponse(t.render(c))

## 模板中使用定义的变量

    :::html+django
    Categories:
    <ul>
      {# 自定义的 context processor 函数的返回值是：{'categories': all_categories}，该字典的 key 可以直接在模板中作为变量使用 #}
      {% for category in categories %}
        <li>{{ category.title }}</li>
      {% endfor %}
    </ul>

结果：

> Categories:
>
>    * python
>    * django

示例项目下载：[mysite.tar.gz](/static/downloads/2013.01.23.mysite.tar.gz)，django 版本：1.4.3。


##参考

* [Django “Global” Template Variable — matthewphiong blog](http://matthewphiong.com/django-global-template-variable)
* [django.template.RequestContext](https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.RequestContext)
* [Writing your own context processors](https://docs.djangoproject.com/en/dev/ref/templates/api/#writing-your-own-context-processors)
* [TEMPLATE\_CONTEXT\_PROCESSORS](https://docs.djangoproject.com/en/1.4/ref/settings/#template-context-processors)
* [How do I make a variable available to all my templates?](https://docs.djangoproject.com/en/dev/faq/usage/#how-do-i-make-a-variable-available-to-all-my-templates)
