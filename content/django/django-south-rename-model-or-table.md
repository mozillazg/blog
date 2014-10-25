Title: [django]使用 South 重命名 model 名称
Date: 2013-06-05
Tags: django, python, south
Slug: django-south-rename-model-or-table

本文将讲述如何使用 South 重命名表名。

假设应用 foobar 有个 model:

    :::python
    class Foo(models.Model):
        foo = models.IntegerField()

想要将 model Foo 改名为 Bar。

1. 改好 models.py

        :::python
        class Bar(models.Model):
            foo = models.IntegerField()

2. 执行 south 命令

        :::bash
        # python manage.py schemamigration yourapp rename_model_foo_to_bar --empty
        # 本例是
        python manage.py schemamigration foobar rename_model_foo_to_bar --empty

3. 更改生成的 000x_xxx.py 文件

        :::python
        class Migration(SchemaMigration):

            def forwards(self, orm):
                # 更改表名
                # db.rename_table('yourapp_foo', 'yourapp_bar')
                db.rename_table('foobar_foo', 'foobar_bar')


            def backwards(self, orm):
                # 撤销更改
                # db.rename_table('yourapp_bar', 'yourapp_foo')
                db.rename_table('foobar_bar', 'foobar_foo')


## 参考

* [Easiest way to rename a model using Django/South? - Stack Overflow](http://stackoverflow.com/questions/2862979/easiest-way-to-rename-a-model-using-django-south?rq=1)
