[django]通过自定义 aggregate 的方式让 Count 支持 SQL 函数
==================================================================================

:date: 2015-04-01
:slug: django-let-count-support-sql-expression-through-custom-aggregates-on-django-1.8


本文的代码是基于 Django 1.8 的，可能并不适用于其他版本的 Django 。

默认情况下 ``Count`` 并不支持 SQL 函数，比如 `count(date(field_name))` 。
下面将讲述通过自定义 aggregate 的方式让 count 支持 SQL 函数。

.. code-block:: python

    from django.db.models.aggregates import Count
    from django.db.models.fields import IntegerField


    class CountWithFunc(Count):
        template = '%(function)s(%(distinct)s%(expression)s)'

        def __init__(self, expression, distinct=False, **extra):
            extra.update({'expression': expression})
            super(Count, self).__init__(
                'pk', distinct='DISTINCT ' if distinct else '',
                output_field=IntegerField(), **extra
            )
    
    Event.objects.values('name').annotate(
        count=CountWithFunc("date(created_at)", distinct=True)
    )
    # == SELECT name, COUNT(DISTINCT date(created_at)) AS count FROM event GROUP BY name



参考资料
--------

* `django/aggregates.py at 1.8c1 · django/django <https://github.com/django/django/blob/1.8c1/django/db/models/aggregates.py>`__
* `custom aggregates on django | coder . cl（其他版本可以参考这个） <http://coder.cl/2011/09/custom-aggregates-on-django/>`__