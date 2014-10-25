Title: [django]让 BigIntegerField 字段自增长
Date: 2013-06-03
Tags: django, python, BigIntegerField, auto-increment, mysql
Slug: django-let-bigintegerfield-auto-increment

默认的 id 字段是 IntegerField 属性，长度是 11。

现在要将它改为 BigIntegerField 属性，因为它的长度是更长。

    :::python
    class Foo(models.Model):
        id = models.BigIntegerField(primary_key=True)
        #...

更改后的数据库字段信息：

    :::bash
    mysql> desc foo_bar;
    +--------------+------------+------+-----+---------+-------+
    | Field        | Type       | Null | Key | Default | Extra |
    +--------------+------------+------+-----+---------+-------+
    | id           | bigint(20) | NO   | PRI | NULL    |       |

问题出来了，更改后的 id 没有自增长的功能。

解决办法就是自定义一个字段属性：

代码结构：

    :::bash
    foo   # app
    |-fields.py
    |-models.py

代码：

    :::python
    # fields.py
    from django.db.models import fields
    from south.modelsinspector import add_introspection_rules


    class BigIntegerAutoField(fields.BigIntegerField):
        def db_type(self, connection):
            if 'mysql' in connection.__class__.__module__:
                return 'bigint AUTO_INCREMENT'
            return super(BigIntegerAutoField, self).db_type(connection)

    add_introspection_rules([], ["^foo\.fields\.BigIntegerAutoField"])


    # models.py
    from .fields import BigIntegerAutoField


    class Bar(models.Model):
        id = BigIntegerAutoField(primary_key=True)
        # ...

结果：

    :::bash
    mysql> desc foo_bar;
    +--------------+------------+------+-----+---------+----------------+
    | Field        | Type       | Null | Key | Default | Extra          |
    +--------------+------------+------+-----+---------+----------------+
    | id           | bigint(20) | NO   | PRI | NULL    | auto_increment |


## 参考

* [python - Django BigInteger auto-increment field as primary key? - Stack Overflow](http://stackoverflow.com/questions/2672975/django-biginteger-auto-increment-field-as-primary-key)
