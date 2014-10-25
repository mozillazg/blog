Flask-SQLAlchemy 执行 exclude 查询
=====================================

:date: 2014-10-10
:tags: python, flask, flask-sqlalchemy
:slug: flask-sqlalchemy-exclude-query

通过 ``filter`` 间接实现：

.. code-block:: python

   # exclude name = 'jim'
    MyClass.query.filter(MyClass.name != 'jim')


参考资料
--------------

* `Querying — SQLAlchemy 0.8 Documentation`__
* `python - flask sqlalchemy querying a column with not equals - Stack Overflow`__

__ http://docs.sqlalchemy.org/en/rel_0_8/orm/query.html#sqlalchemy.orm.query.Query.filte
__ http://stackoverflow.com/questions/16093475/flask-sqlalchemy-querying-a-column-with-not-equals