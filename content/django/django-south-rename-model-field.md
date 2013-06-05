Title: [django]使用 South 重命名 model 字段名
Date: 2013-06-05
Tags: django, python, south
Slug: django-south-rename-model-field

本文将讲述如何使用 South 重命名表的字段名。

假设应用 foobar 有个 model:

    :::python
    class Foo(models.Model):
        foo = models.IntegerField()

想要将 foo 字段名改为 bar。

1. 改好 models.py

        :::python
        class Foo(models.Model):
            bar = models.IntegerField()

2. 执行 south 命令

        :::bash
        # python manage.py schemamigration yourapp rename_field_foo_to_bar --empty
        # 本例是
        python manage.py schemamigration foobar rename_field_foo_to_bar --empty

3. 更改生成的 000x_xxx.py 文件

        :::python
        class Migration(SchemaMigration):

            def forwards(self, orm):
                # 更改列名
                # db.rename_column('yourapp_foo', 'oldname', 'newname')
                db.rename_column('foobar_foo', 'foo', 'bar')


            def backwards(self, orm):
                # 撤销更改
                # db.rename_column('yourapp_foo', 'newname', 'oldname')
                db.rename_column('foobar_foo', 'bar', 'foo')


## 参考

* [Django - How to rename a model field using South? - Stack Overflow](http://stackoverflow.com/questions/3235995/django-how-to-rename-a-model-field-using-south)
