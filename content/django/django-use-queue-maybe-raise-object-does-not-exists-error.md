title: 解决在 Django 中使用 rq 或 celery 任务队列有时会出现 DoesNotExist 的问题
slug: django-use-queue-maybe-raise-object-not-exist-error
date: 2015-11-01
tags: rq, celery, django-rq

在 Django 中下面的代码有时会抛出 `DoesNotExist` 异常：

    @app.task
    def job1(pk):
        Foobar.objects.get(pk=pk)


    @transaction.atomic
    def foo(request):
        foobar = Foobar.objects.create(...)
        job1.delay(foobar.pk)
        ...
        return ...

上面的代码有时就会出现: `DoesNotExist: Foobar matching query does not exist.` 异常。
为什么为出现这种情况呢?

原来在这种情况下只在 view return 的时候 Django 才会提交数据库事物，如果 view 中有异常的话会回滚事物。
也就是说虽然我们通过 `create` 方法创建了记录同时得到了一个主键，但是在事物提交之前这条记录其实并没有
真实存在于数据库中，所以如果 job1 在 return 之前就立马执行了的话就会出现 `DoesNotExist` 异常。（
在实践中发现就算是使用 Django 默认的自动提交事物有时也会出现 `DoesNotExist` 异常）

解决办法就是，只在事物执行成功的时候才执行放入任务队列的操作。有一个第三方 app: [django-transaction-hooks](https://github.com/carljm/django-transaction-hooks)
可以很方便的帮助我们解决这个问题:

1. 安装: `pip install django-transaction-hooks`
2. 修改 settings 中 `DATABASES` 的值，将  `ENGINE` 替换为这个包内置的 engine。
   postgresql 替换为 `transaction_hooks.backends.postgresql_psycopg2`,
   mysql 替换为 `transaction_hooks.backends.mysql`,
   sqlite 替换为 `transaction_hooks.backends.sqlite3`,
   postgis 替换为 `transaction_hooks.backends.postgis` 比如：
   
        DATABASES = {
        'default': {
            'ENGINE': 'transaction_hooks.backends.postgresql_psycopg2',
            'NAME': 'foo',
            },
        }
    
3. 使用 `connection.on_commit` 来执行需要在事物成功提交时才执行的操作：
    
        connection.on_commit(lambda: job1.delay(foobar.pk))

详情请查看文档：<https://django-transaction-hooks.readthedocs.org>


## 参考资料

* 《High Performance Django》
* <http://celery.readthedocs.org/en/latest/userguide/tasks.html#database-transactions>