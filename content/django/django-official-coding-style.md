Title: [django]官方编码规范
Date: 2013-02-01
Tags: django, python
Slug: django-offical-coding-style

请以最新的官方英文版为准：<https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/>

## 编码风格

当编写 Django 代码时，请遵循下列编码规范。

### Python 风格

* 除非另有规定，否则请遵循 [PEP 8](http://www.python.org/dev/peps/pep-0008) 风格指南。      
  你可以使用类似 [pep8](http://pypi.python.org/pypi/pep8) 的工具检查你的代码，
  但是，请记住 [PEP 8](http://www.python.org/dev/peps/pep-0008) 只是个指南，并非强制约束，因此应当以你所处项目/团队的风格为主。      
  一个比较大的例外就是，[PEP 8](http://www.python.org/dev/peps/pep-0008) 规定代码行长最长不能超过 79 个字符。问题是现在是 21 世纪了，我们有高分辨率的显示器可以显示超过 79 个字符的代码行。如果这这个约定让代码看起来很丑或难以阅读的话，那么就没必要限制行长不超过 79 个字符。

* 使用4个空格进行缩进。

* 使用下划线而不是小驼峰法（camelCase）命名变量、函数及方法名（比如，poll.get_unique_voters()，不要使用 poll.getUniqueVoters）。

* 使用首字母大写（InitialCaps）的方式命名类名（或能够返回类的工厂函数）。

* 文档字符串中，使用动词（action words）。比如：

        def foo():
            """
            Calculates something and returns the result.
            """
            pass
  反例：

        def foo():
            """
            Calculate something and return the result.
            """
            pass

### 模板风格

* 在模板中，大括号及标签内容之间使用一个（只需一个）空格。      
  应该这样：

        {{ foo }}
  别这样：

        {{foo}}

### 视图风格

* 在视图中，视图函数的第一个参数应该被命名为 request。       
  应该这样：

        def my_view(request, foo):
            # ...
  别这样：

        def my_view(req, foo):
            # ...

### 模型风格

* 字段名应该全部小写，使用下划线代替小驼峰法。
  应该这样：

        class Person(models.Model):
            first_name = models.CharField(max_length=20)
            last_name = models.CharField(max_length=40)
  别这样：

        class Person(models.Model):
            FirstName = models.CharField(max_length=20)
            Last_Name = models.CharField(max_length=40)

* `class Meta` 应该在字段被定义*后*才出现，使用一个空行分隔。
  应该这样：

        class Person(models.Model):
            first_name = models.CharField(max_length=20)
            last_name = models.CharField(max_length=40)

            class Meta:
                verbose_name_plural = 'people'
  别这样：

        class Person(models.Model):
            first_name = models.CharField(max_length=20)
            last_name = models.CharField(max_length=40)
            class Meta:
                verbose_name_plural = 'people'
  也别这样：

        class Person(models.Model):
            class Meta:
                verbose_name_plural = 'people'

            first_name = models.CharField(max_length=20)
            last_name = models.CharField(max_length=40)

* model 内的类和方法的定义顺序应该遵循如下顺序（不是所有项都是必需的）：       
  1\. 所有的数据库字段          
  2\. 自定义[管理器属性（manager attributes）](https://docs.djangoproject.com/en/dev/topics/db/managers/)         
  3\. `class Meta`          
  4\. `def __unicode__()`       
  5\. `def __str__()`       
  6\. `def save()`          
  7\. `def get_absolute_url()`          
  8\. 其他自定义方法        

* 如果一个 model 字段定义了 `choices`，那么定义的多元元组的名称应该全部大写。例如：      

        class MyModel(models.Model):
            DIRECTION_UP = 'U'
            DIRECTION_DOWN = 'D'
            DIRECTION_CHOICES = (
                (DIRECTION_UP, 'Up'),
                (DIRECTION_DOWN, 'Down'),
            )

### django.conf.settings 的使用

模块不常用的设置项被储存在 `django.conf.settings` 中

Modules should not in general use settings stored in `django.conf.settings` at the top level (i.e. evaluated when the module is imported). The explanation for this is as follows:

Manual configuration of settings (i.e. not relying on the `DJANGO_SETTINGS_MODULE` environment variable) is allowed and possible as follows:

    from django.conf import settings

    settings.configure({}, SOME_SETTING='foo')

However, if any setting is accessed before the settings.configure line, this will not work. (Internally, `settings` is a `LazyObject` which configures itself automatically when the settings are accessed if it has not already been configured).

So, if there is a module containing some code as follows:

    from django.conf import settings
    from django.core.urlresolvers import get_callable

    default_foo_view = get_callable(settings.FOO_VIEW)

...then importing this module will cause the settings object to be configured. That means that the ability for third parties to import the module at the top level is incompatible with the ability to configure the settings object manually, or makes it very difficult in some circumstances.

Instead of the above code, a level of laziness or indirection must be used, such as `django.utils.functional.LazyObject`, `django.utils.functional.lazy()` or `lambda`.

### Miscellaneous

* Mark all strings for internationalization; see the i18n documentation for details.
* Remove import statements that are no longer used when you change code. The most common tools for this task are pyflakes and pylint.
* Systematically remove all trailing whitespaces from your code as those add unnecessary bytes, add visual clutter to the patches and can also occasionally cause unnecessary merge conflicts. Some IDE’s can be configured to automatically remove them and most VCS tools can be set to highlight them in diff outputs. Note, however, that patches which only remove whitespace (or only make changes for nominal PEP 8 conformance) are likely to be rejected, since they only introduce noise rather than code improvement. Tidy up when you’re next changing code in the area.
* Please don’t put your name in the code you contribute. Our policy is to keep contributors’ names in the AUTHORS file distributed with Django – not scattered throughout the codebase itself. Feel free to include a change to the AUTHORS file in your patch if you make more than a single trivial change.
