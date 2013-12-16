[django]修复 "dictionary update sequence element 0 has length 1, 2 is required"
###############################################################################

:date: 2013-10-13
:tags: python, django
:slug: django-dictionary-update-sequence-element-0-has-length-1-2-is-required

定义 url 路由时，下面的代码会导致出现标题中的错误：

.. code-block:: python

    url(r'^foo/$', 'view_func_name', 'foo')

原因是因为忘了写 ``name`` 这个关键字参数:

.. code-block:: python

    url(r'^foo/$', 'view_func_name', name='foo')
