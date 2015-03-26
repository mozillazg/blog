[译] Peewee 快速上手
=============================

:date: 2015-03-26
:slug: peewee-quickstart-zh-cn


本文译自：http://docs.peewee-orm.com/en/latest/peewee/quickstart.html

以下为译文：


**note**: 如果你需要一个更详实的例子的话，可以参考使用 peewee 和 Flask 框架的一个教程： `创建一个 twitter 风格的 web app`__


__ http://docs.peewee-orm.com/en/latest/peewee/example.html#example-app


我 **强烈** 推荐你打开一个解释器 shell 会话并运行本文的代码。这种方式可以让你直观的感受到查询操作的效果。




定义 Model
-------------

Model 类，Field 以及 model 实例与数据库的对应关系如下：


=================  =========================
Thing              Corresponds to...
=================  =========================
Model 类           数据库表
Field 实例         数据库表字段
Model 实例         数据库表一行数据
=================  =========================


一般在项目中使用 peewee 的时候都会需要定义一个或多个 `Model`__ 类：

.. code-block:: python

    from peewee import *

    db = SqliteDatabase('people.db')

    class Person(Model):
        name = CharField()
        birthday = DateField()
        is_relative = BooleanField()

        class Meta:
            database = db  # 此 model 使用 "people.db" 数据库。

__ http://docs.peewee-orm.com/en/latest/peewee/api.html#Model

**note**: 你可能注意到了我们使用 ``Person`` 而不是 ``People`` 命名我们的 model。
这里有一个你应该遵守的约定——尽管这个表将会包含多个 people，但是我们总是使用 **单数名词** 来命名类名。

这里有一些用来指定数据存储类型的 `field types`__ . Peewee 会知道将 pythonic 结果转换为数据库识别的数据，所以你可以放心的在你的代码中使用 Python 类型。

__ http://docs.peewee-orm.com/en/latest/peewee/models.html#fields


在 peewee 中定义 `外键关系`__ 也是非常的容易的：

__ http://en.wikipedia.org/wiki/Foreign_key

.. code-block:: python

    class Pet(Model):
        owner = ForeignKeyField(Person, related_name='pets')
        name = CharField()
        animal_type = CharField()

        class Meta:
            database = db  # 此 model 使用 "people.db" 数据库。

现在我们已经定义了一下 model 了，下面可以连接数据库了。
虽然没必要显示的打开连接，但是这是一个好的习惯，因为它能立即暴露数据库库连接相关的各种错误，而不是在其他某个时候执行第一次查询操作的时候才被发现。
同样的在你处理完以后显示的关闭连接也是一个好的习惯——比如，一个 web app 可能会在接收到一个请求时打开连接，然后再它发送响应的时候关闭连接。

.. code-block:: python

    >>> db.connect()

下面我们将创建用于存储数据的表结构。下面的操作将创建相关的列，索引，sequences 以及外键约束：

.. code-block:: python

    >>> db.create_tables([Person, Pet])


存储数据
----------


让我们在数据库里存一些 people 数据。可以使用 save_ 和 create_ 方法来添加和更新 people 记录：


.. code-block:: python

    >>> from datetime import date
    >>> uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
    >>> uncle_bob.save()  # bob 现在已经存到数据库里了
    1

**note**: 当你调用 save_ 方法时，将返回生效的记录行数。

你也可以通过调用 create_ 方法来添加一个 person, 它将返回一个 model 实例。

.. code-block:: python

    >>> grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)
    >>> herb = Person.create(name='Herb', birthday=date(1950, 5, 5), is_relative=False)

为了更新一行数据，只需修改 model 实例然后调用 save_ 方法保存变更就可以了。下面我们将更改 Grandma 的名字然后把变更保存到数据中：

.. code-block:: python

    >>> grandma.name = 'Grandma L.'
    >>> grandma.save()  # 更新数据库中 grandma 的名字
    1


.. _save: http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.save
.. _create: http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.create



我们现在在数据库里已经有 3 个人了。让我们给他们一些 pet. grandma 不喜欢在房间里有动物，因此她一点也不想要， 但是 Herb 非常喜欢动物：

.. code-block:: python

    >>> bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
    >>> herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
    >>> herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
    >>> herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

过了很长一段时间后， Mittens 生病去世了。 我们需要把他从数据库中移除掉：


.. code-block:: python

    >>> herb_mittens.delete_instance()  # 他有个非常棒的人生
    1


**note**: `delete_instance()`__ 的返回值是被从数据库中移除的数据的总行数。

Uncle Bob 觉得太多的动物会弄脏 Herb 的屋子，因此他收养了 Fido：

.. code-block:: python

    >>> herb_fido.owner = uncle_bob
    >>> herb_fido.save()
    >>> bob_fido = herb_fido  # 为了更明确，我们重命名了变量


__ http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.delete_instance


检索数据
-----------

下面讲解如何通过查询的方式检索数据。关系型数据库非常适合进行特定的查询操作。


获取单条记录
``````````````
让我们从数据库中检索 Grandma 的数据。使用 `SelectQuery.get()`__ 从数据库中获取单条记录。

.. code-block:: python

    >>> grandma = Person.select().where(Person.name == 'Grandma L.').get()

我们也可以使用简便的 `Model.get()`__ 来实现相同的功能：

.. code-block:: python

    >>> grandma = Person.get(Person.name == 'Grandma L.')

__ http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.get
__ http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.get




罗列记录
```````````````

列出数据库中所有的 people 记录：

.. code-block:: python

    >>> for person in Person.select():
    ...     print person.name, person.is_relative
    ...
    Bob True
    Grandma L. True
    Herb False

让我们列出所有的猫以及他们主人的名字：

.. code-block:: python

    >>> query = Pet.select().where(Pet.animal_type == 'cat')
    >>> for pet in query:
    ...     print pet.name, pet.owner.name
    ...
    Kitty Bob
    Mittens Jr Herb


在上一个查询里有一个问题：因为我们访问了 ``pet.owner.name`` 但是我们并没有在我们原始的查询中包含这个值，
为了获取该 pet 的所有者，peewee 将执行一次额外的查询。这种行为将导致名为 `N + 1`__ 的问题，并且通常情况下应该避免这种问题。
 
__ http://docs.peewee-orm.com/en/latest/peewee/querying.html#nplusone


我们可以通过同时查询 Pet 和 Person 以及增加一个 join 的方式来避免这个额外的查询。

.. code-block:: python

    >>> query = (Pet
    ...          .select(Pet, Person)
    ...          .join(Person)
    ...          .where(Pet.animal_type == 'cat'))
    >>> for pet in query:
    ...     print pet.name, pet.owner.name
    ...
    Kitty Bob
    Mittens Jr Herb

让我们列出所有者是 Bob 的 pet:

.. code-block:: python

    >>> for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    ...     print pet.name
    ...
    Kitty
    Fido

我们能做的另一个非常酷的事情是获取 bob 所拥有的 pet. 因为我们已经有了一个表示 Bob 的对象，所以我们可以用下面的代码来实现：

.. code-block:: python

    >>> for pet in Pet.select().where(Pet.owner == uncle_bob):
    ...     print pet.name

可以通过增加一个 `order_by()`__ 语句的方式来确保它们是按字母顺序排序的：

.. code-block:: python

    >>> for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    ...     print pet.name
    ...
    Fido
    Kitty

__ http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.order_by


让我们按从年幼到年长的顺序列出所有的 people:

.. code-block:: python

    >>> for person in Person.select().order_by(Person.birthday.desc()):
    ...     print person.name, person.birthday
    ...
    Bob 1960-01-15
    Herb 1950-05-05
    Grandma L. 1935-03-01


现在让我们列出所有的 people 以及他们各自的 pet 的一些信息：

.. code-block:: python

    >>> for person in Person.select():
    ...     print person.name, person.pets.count(), 'pets'
    ...     for pet in person.pets:
    ...         print '    ', pet.name, pet.animal_type
    ...
    Bob 2 pets
        Kitty cat
        Fido dog
    Grandma L. 0 pets
    Herb 1 pets
        Mittens Jr cat

我们又一次遇到了 `N + 1`__ 查询的问题。我们可以通过执行 一个 JOIN 以及聚合记录的方式来避免这个问题：

.. code-block:: python

    >>> subquery = Pet.select(fn.COUNT(Pet.id)).where(Pet.owner == Person.id)
    >>> query = (Person
    ...          .select(Person, Pet, subquery.alias('pet_count'))
    ...          .join(Pet, JOIN.LEFT_OUTER)
    ...          .order_by(Person.name))

    >>> for person in query.aggregate_rows():   #  注意是调用的 `aggregate_rows()` 方法。
    ...     print person.name, person.pet_count, 'pets'
    ...     for pet in person.pets:
    ...         print '    ', pet.name, pet.animal_type
    ...
    Bob 2 pets
         Kitty cat
         Fido dog
    Grandma L. 0 pets
    Herb 1 pets
         Mittens Jr cat


尽管我们单独创建了一个子查询，但是实际上 **只执行了一条** 查询语句。

__ http://docs.peewee-orm.com/en/latest/peewee/querying.html#nplusone


最后，让我们再做一个复杂的查询。让我们列出所有生日满足如下条件的 people:

* 1940 之前(grandma)
* 1959 之后(bob)


.. code-block:: python


    >>> d1940 = date(1940, 1, 1)
    >>> d1960 = date(1960, 1, 1)
    >>> query = (Person
    ...          .select()
    ...          .where((Person.birthday < d1940) | (Person.birthday >= d1960)))
    ...
    >>> for person in query:
    ...     print person.name, person.birthday
    ...
    Bob 1960-01-15
    Grandma L. 1935-03-01


下面让我们找出生日在 1940 到 1960 之间的 people:

.. code-block:: python

    >>> query = (Person
    ...          .select()
    ...          .where((Person.birthday > d1940) & (Person.birthday < d1960)))
    ...
    >>> for person in query:
    ...     print person.name, person.birthday
    ...
    Herb 1950-05-05

最后一个查询。这次将使用 SQL 函数的方式找出名称以大写或小写 G 开头的所有 people:

.. code-block:: python

    >>> expression = (fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g')
    >>> for person in Person.select().where(expression):
    ...     print person.name
    ...
    Grandma L.

我们以及处理完数据库了，让我们关闭连接吧：

.. code-block:: python

    >>> db.close()


所有其他的 SQL 子句也都是可用的，比如：

* `group_by()`__
* `having()`__
* `limit()`__ 和 `offset()`__

查看文档中的 `Querying`__ 获取更多的信息。

__ http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.group_by
__ http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.having
__ http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.limit
__ http://docs.peewee-orm.com/en/latest/peewee/api.html#SelectQuery.offset
__ http://docs.peewee-orm.com/en/latest/peewee/querying.html#querying


作用于已存在的数据库
----------------------

如果你已经拥有了一个数据库，你可以使用 `pwiz, a model generator.`__ 自动生成 peewee models。
比如，我有一个名字叫 charles_blog 的 postgresql 数据库，我就可以这样运行::

    python -m pwiz -e postgresql charles_blog > blog_models.py

__ http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pwiz


下一步？
-----------

这里的内容只是用于快速上手。 如果你想找一个更完整的 web app 的示例的话，可以看一下  `Example app`__ .


__ http://docs.peewee-orm.com/en/latest/peewee/example.html#example-app