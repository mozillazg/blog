Title: [django]按月分组统计数据
Date: 2013-09-29
Tags: django, python
Slug: django-group-by-month

假设有以下 model:

    :::python
    class Foobar(models.Model):
        name = models.CharField(max_length=100)
        date_created = models.DateField(auto_now_add=True)

        def __unicode__(self):
            return self.name


按月统计数量的代码如下：

    :::python
    from django.db import connection
    from django.db.models import Count

    select = {'month': connection.ops.date_trunc_sql('month', 'date_created')}
    Foobar.objects.extra(select=select).values('month').annotate(number=Count('id'))
    # [{'number': 10, 'month': datetime.datetime(2013, 9, 1, 0, 0)}]


## 参考

* [python - Django annotate groupings by month - Stack Overflow](http://stackoverflow.com/questions/3543379/django-annotate-groupings-by-month)
