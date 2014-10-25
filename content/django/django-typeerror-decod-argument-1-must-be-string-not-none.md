Title: [django] 创建后台超级用户时出现 TypeError: decode() argument 1 must be string, not None 错误
Date: 2013-02-19
Tags: python, django
Slug: django-typeerror-decod-argument-1-must-be-string-not-none


错误信息如下：

    :::console
    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Traceback (most recent call last):
      File "manage.py", line 10, in <module>
        execute_from_command_line(sys.argv)
      File "/usr/local/lib/python2.7/dist-packages/django/core/management/__init__.py", line 443, in execute_from_command_line

      ...

      File "/usr/local/lib/python2.7/dist-packages/django/contrib/auth/management/commands/createsuperuser.py", line 70, in handle
        default_username = get_default_username()
      File "/usr/local/lib/python2.7/dist-packages/django/contrib/auth/management/__init__.py", line 105, in get_default_username
        default_username = get_system_username()
      File "/usr/local/lib/python2.7/dist-packages/django/contrib/auth/management/__init__.py", line 85, in get_system_username
        return getpass.getuser().decode(locale.getdefaultlocale()[1])
    TypeError: decode() argument 1 must be string, not None

执行 `python manage.py createsuperuser` 也会报上面的错误。

解决办法：

设置正确的系统编码即可。

    :::console
    $ export LC_ALL=en_US.UTF-8
    $ python manage.py createsuperuser
    Username (leave blank to use 'hello'): admin
    E-mail address:

## 参考

* [BUG！！！======> syncdb 时 “ TypeError: decode() argument 1 must be string, not None ” - 事件轮询，回不到过去 - 博客园](http://www.cnblogs.com/wenjiashe521/archive/2012/08/24/2653773.html)
* [python - Django 1.4 defining user - Stack Overflow](http://stackoverflow.com/questions/10564215/django-1-4-defining-user)
* [Python os.getenv on OSX (Django 1.4) - Stack Overflow](http://stackoverflow.com/questions/9886178/python-os-getenv-on-osx-django-1-4)
