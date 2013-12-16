[django]修复 "TypeError: delete() got an unexpected keyword argument 'using'"
###############################################################################

:date: 2013-10-13
:tags: python, django
:slug: django-TypeError-delete-got-an-unexpected-keyword-argument-using

调用 delete 方法时，下面的代码会导致出现标题中的错误：

.. code-block:: python

    Foo.objects.filter(name='foo').delete(using='writedb')


原因是因为只有单个查询结果对象的 ``delete`` 方法拥有 ``using`` 参数，
而查询结果集对象的 ``delete`` 方法没有 ``using`` 关键字参数:

.. code-block:: python

    foos = Foo.objects.filter(name='foo')
    for foo in foos:
        foos.delete(using='writedb')
