[django] 使用 Q 对象构建复杂的查询语句
==========================================

:slug: django-the-power-of-q-objects-and-how-to-use-q-object
:date: 2015-11-07

本文将讲述如何在 Django 项目中使用 ``Q`` 构建复杂的查询条件。
假设有如下的 model:

.. code-block:: python

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

然后我们创建了一些数据：

.. code-block:: python

    Question.objects.create(
        question_text='what are you doing',
        pub_date=datetime.datetime(2015, 11,7)
    )
    Question.objects.create(
        question_text='what is wrong with you',
        pub_date=datetime.datetime(2014, 11, 7)
    )
    Question.objects.create(
        question_text='who are you',
        pub_date=datetime.datetime(2015, 10, 7)
    )
    Question.objects.create(
        question_text='who am i',
        pub_date=datetime.datetime(2014, 10, 7)
    )

    >>> Question.objects.all()
    [<Question: what are you doing>, <Question: what is wrong with you>,
     <Question: who are you>, <Question: who am i>]

AND 查询
-----------

将多个 ``Q`` 对象作为非关键参数或使用 ``&`` 联结即可实现 ``AND`` 查询:

.. code-block:: python

    # Q(...)
    >>> Question.objects.filter(Q(question_text__contains='you'))
    [<Question: what are you doing>, <Question: what is wrong with you>, <Question: who are you>]

    # Q(...), Q(...)
    >>> Question.objects.filter(Q(question_text__contains='you'), Q(question_text__contains='what'))
    [<Question: what are you doing>, <Question: what is wrong with you>]

    # Q(...) & Q(...)
    >>> Question.objects.filter(Q(question_text__contains='you') & Q(question_text__contains='what'))
    [<Question: what are you doing>, <Question: what is wrong with you>]


OR 查询
------------

使用 ``|`` 联结两个 ``Q`` 对象即可实现 ``OR`` 查询:

.. code-block:: python

    # Q(...) | Q(...)
    >>> Question.objects.filter(Q(question_text__contains='you') | Q(question_text__contains='who'))
    [<Question: what are you doing>, <Question: what is wrong with you>, <Question: who are you>, <Question: who am i>]


NOT 查询
------------

使用 ``~Q(...)`` 客户实现 ``NOT`` 查询:

.. code-block:: python

    # ~Q(...)
    >>> Question.objects.filter(~Q(question_text__contains='you'))
    [<Question: who am i>]


与关键字参数共用
----------------

记得要把 ``Q`` 对象放前面:

.. code-block:: python

    # Q(...), key=value
    >>> Question.objects.filter(Q(question_text__contains='you'), question_text__contains='who')
    [<Question: who are you>]


OR, AND, NOT 多条件查询
-------------------------

这几个条件可以自由组合使用:

.. code-block:: python

    # (A OR B) AND C AND (NOT D)
    >>> Question.objects.filter((Q(question_text__contains='you') | Q(question_text__contains='who')) & Q(question_text__contains='what') & ~Q(question_text__contains='are'))
    [<Question: what is wrong with you>]


动态构建查询条件
-------------------

比如你定义了一个包含一些 ``Q`` 对象的列表，如何使用这个列表构建 ``AND`` 或 ``OR`` 查询呢？
可以使用 ``operator`` 和 ``reduce``：

.. code-block:: python

    >>> lst = [Q(question_text__contains='you'), Q(question_text__contains='who')]

    # OR
    >>> Question.objects.filter(reduce(operator.or_, lst))
    [<Question: what are you doing>, <Question: what is wrong with you>, <Question: who are you>, <Question: who am i>]

    # AND
    >>> Question.objects.filter(reduce(operator.and_, lst))
    [<Question: who are you>]

这个列表也可能是根据用户的输入来构建的，比如简单的搜索功能（搜索一个文章的标题或内容或作者名称包含某个关键字）:

.. code-block:: python

    q = request.GET.get('q', '').strip()
    lst = []
    if q:
        for key in ['title__contains', 'content__contains',
                    'author__name__contains']:
            q_obj = Q(**{key: q})
            lst.append(q_obj)
    queryset = Entry.objects.filter(reduce(operator.or_, lst))



参考资料
-----------

* `Parerga und Paralipomena » Blog Archive » The power of django’s Q objects <http://www.michelepasin.org/blog/2010/07/20/the-power-of-djangos-q-objects/>`__
* `Making queries | Django documentation | Django <https://docs.djangoproject.com/en/1.8/topics/db/queries/#complex-lookups-with-q-objects>`__
* `QuerySet API reference | Django documentation | Django <https://docs.djangoproject.com/en/1.8/ref/models/querysets/#django.db.models.Q>`__
* `django/tests.py at master · django/django · GitHub <https://github.com/django/django/blob/master/tests/or_lookups/tests.py>`__
* `9.9. operator — Standard operators as functions — Python 2.7.10 documentation <https://docs.python.org/2/library/operator.html#operator.and_>`__
* `2. Built-in Functions — Python 2.7.10 documentation <https://docs.python.org/2/library/functions.html#reduce>`__