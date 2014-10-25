Title: [django]按天分组统计数据
Date: 2013-09-29
Tags: django, python
Slug: django-group-by-day

假设有以下 model:

    :::python
    class Foobar(models.Model):
        name = models.CharField(max_length=100)
        date_created = models.DateField(auto_now_add=True)

        def __unicode__(self):
            return self.name


按天统计数量的代码如下：

    :::python
    from django.db import connection
    from django.db.models import Count

    select = {'day': connection.ops.date_trunc_sql('day', 'date_created')}
    Foobar.objects.extra(select=select).values('day').annotate(number=Count('id'))
    # [{'number': 10, 'day': datetime.datetime(2013, 9, 29, 0, 0, 0}]


## 参考

* [python - Django annotate groupings by month - Stack Overflow](http://stackoverflow.com/questions/3543379/django-annotate-groupings-by-month)
