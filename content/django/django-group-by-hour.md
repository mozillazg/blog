Title: [django]按小时分组统计数据
Date: 2013-09-29
Tags: django, python
Slug: django-group-by-hour

假设有以下 model:

    :::python
    class Foobar(models.Model):
        name = models.CharField(max_length=100)
        date_created = models.DateField(auto_now_add=True)

        def __unicode__(self):
            return self.name


按小时统计数量的代码如下：

    :::python
    from collections import defaultdict
    from django.db import connection
    from django.db.models import Count

    select = {'hour': connection.ops.date_trunc_sql('hour', 'date_created')}
    result = Foobar.objects.extra(select=select).values('hour').annotate(number=Count('id'))
    # [{'number': 10, 'hour': datetime.datetime(2013, 9, 28, 19, 0, 0},
    #  {'number': 12, 'hour': datetime.datetime(2013, 9, 29, 19, 0, 0}]

    result_new = []
    for x in result:
        date = x['hour']
        for y in result_new:
            if y['hour'].hour == date.hour:
                d = y
                break
        else:
            d = defaultdict(int)
            d['hour'] = date
            result_new.append(d)
        d['number'] += x.get('number', 0)
    result_new = sorted(result_new, key=lambda x: x['hour'].hour)
    # [{'number': 22, 'hour': datetime.datetime(2013, 9, 28, 19, 0, 0},


## 参考

* [python - Django annotate groupings by month - Stack Overflow](http://stackoverflow.com/questions/3543379/django-annotate-groupings-by-month)
