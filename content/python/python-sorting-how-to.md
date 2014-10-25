Title: [python]排序（Sorting Mini-HOW TO）
Date: 2013-03-03
Tags: python, sorting, sort, sorted
Slug: python-sorting-how-to

本文整理自 [HowTo/Sorting - Python Wiki][1]，如有不妥之处，请翻阅英文原文。

Python 内置的 `sort()` 方法可以实现对列表的原地排序功能。内置的 `sorted()` 函数则不会修改原列表，而是生成一个经过排序的新列表。

下面总结一些常用的排序方法。


## 基本排序

最简单的方法就是使用 `sorted()` 函数，它将返回一个经过排序的新列表：

    :::python
    >>> sorted([5, 2, 3, 1, 4])
    [1, 2, 3, 4, 5]

你也可以使用 `list.sort()` 方法， 但是它会修改原列表，所以一般使用 `sorted()`。如果你不再需要原始列表的话，用用 `list.sort()` 也无妨。

    :::python
    >>> a = [5, 2, 3, 1, 4]
    >>> a.sort()
    >>> a
    [1, 2, 3, 4, 5]

另一个不同点是，`list.sort()` 方法只能作用于列表，而 `sorted()` 函数则接受任何可迭代对象。

    :::python
    >>> sorted({1: 'D', 2: 'B', 3: 'B', 4: 'E', 5: 'A'})
    [1, 2, 3, 4, 5]


## Key 函数

从 Python 2.4 开始， `list.sort()` 及 `sorted()` 增加了一个 `key` 参数，该参数接受一个函数作为它的值，可以通过那个函数定义排序应该遵循的规则。

比如，对字符串做不区分大小写的排序：

    :::python
    >>> sorted("This is a test string from Andrew".split(), key=str.lower)
    ['a', 'Andrew', 'from', 'is', 'string', 'test', 'This']

    >>> # 对照
    >>> sorted("This is a test string from Andrew".split())
    ['Andrew', 'This', 'a', 'from', 'is', 'string', 'test']

`key` 参数的值必须是个函数，该函数有一个参数（列表元素）并且返回一个用来排序的 key（按这个 key 进行排序）。

一般通过使用对象的某个索引作为 key 的值来对复杂对象进行排序。比如对一个多维数组进行排序：

    :::python
    >>> student_tuples = [
            ('john', 'A', 15),
            ('jane', 'B', 12),
            ('dave', 'B', 10),
    ]
    # 按列表元素（元组）的第3个值排序
    >>> sorted(student_tuples, key=lambda student: student[2])   # sort by age
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

这个技术也可以用来按对象的属性值进行排序。比如：

    :::python
    >>> class Student:
            def __init__(self, name, grade, age):
                    self.name = name
                    self.grade = grade
                    self.age = age
            def __repr__(self):
                    return repr((self.name, self.grade, self.age))

    >>> student_objects = [
            Student('john', 'A', 15),
            Student('jane', 'B', 12),
            Student('dave', 'B', 10),
    ]
    # 按 age 属性的值排序
    >>> sorted(student_objects, key=lambda student: student.age)   # sort by age
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]


## Operator 模块函数

由于 key 参数比较常用，所以 Python 内置了一些用来简单、快速生成相关函数的方法。
[operator 模块][2] 提供了 [itemgetter][3]，[attrgetter][4]，
以及从 Python 2.6 开始提供的 [methodcaller][5] 函数。

使用这些函数，上面的例子将变得更简单、更快速：

    :::python
    >>> from operator import itemgetter, attrgetter

    >>> student_tuples = [
            ('john', 'A', 15),
            ('jane', 'B', 12),
            ('dave', 'B', 10),
    ]
    >>> sorted(student_tuples, key=itemgetter(2))  # 按元素索引排序
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

    >>> class Student:
            def __init__(self, name, grade, age):
                    self.name = name
                    self.grade = grade
                    self.age = age
            def __repr__(self):
                    return repr((self.name, self.grade, self.age))

    >>> student_objects = [
            Student('john', 'A', 15),
            Student('jane', 'B', 12),
            Student('dave', 'B', 10),
    ]
    >>> sorted(student_objects, key=attrgetter('age'))  # 按对象属性排序
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

通过 operator 模块提供的函数还可以实现多重排序的功能。比如，先按 grade 排序再按 age 排序：

    :::python
    >>> sorted(student_tuples, key=itemgetter(1,2))
    [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

    >>> sorted(student_objects, key=attrgetter('grade', 'age'))
    [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

[methodcaller][5]
函数可以让元素调用一个方法，然后按方法的返回值进行排序：

    :::python
    >>> words = ['b', 'a', 'abase', 'alfalfa']
    >>> sorted(words, key=methodcaller('count', 'a'))  # word.count('a')
    ['b', 'a', 'abase', 'alfalfa']

    # 等价于
    >>> sorted(words, key=lambda word: word.count('a'))
    ['b', 'a', 'abase', 'alfalfa']
    >>>

## 升序和降序

`list.sort()` 和 `sorted()` 都接受一个布尔类型的 `reverse` 参数。这个参数用来标记是否使用降序排序。比如获取按 age 降序排序的 student 数据：

    :::python
    >>> sorted(student_tuples, key=itemgetter(2), reverse=True)
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
    
    >>> sorted(student_objects, key=attrgetter('age'), reverse=True)
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

## 平衡（Stability）排序和复杂排序

从 Python 2.2 开始，排序将保证能够 [stable][6]。
这意味着当多个记录拥有相同的 key 时，它们的原始顺序将被保留。

    :::python
    >>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
    >>> sorted(data, key=itemgetter(0))
    [('blue', 1), ('blue', 2), ('red', 1), ('red', 2)]

这里有两条记录都包含 'blue' 并且原列表中 ('blue', 1) 排在 ('blue', 2) 之前，排序后这个顺序依旧被保留。

这个非常有用的特性可以用来实现包含多重排序（一会升序，一会降序）的复杂排序。比如，目标是实现 student 数据先以 grade 降序排序再以 age 升序排序：

    :::python
    >>> class Student:
            def __init__(self, name, grade, age):
                    self.name = name
                    self.grade = grade
                    self.age = age
            def __repr__(self):
                    return repr((self.name, self.grade, self.age))

    >>> student_objects = [
            Student('john', 'A', 15),
            Student('jane', 'B', 12),
            Student('dave', 'B', 10),
    ]

    >>> s = sorted(student_objects, key=attrgetter('age'))     # sort on secondary key
    >>> s
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

    >>> sorted(s, key=attrgetter('grade'), reverse=True)       # now sort on primary key, descending
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

Python 使用的 [Timsort][7] 排序算法能够高效的实现多重排序。

## 以前的实现方式(Decorate-Sort-Undecorate)

Python 2.4 之前的惯用方法之一是使用 Decorate-Sort-Undecorate，比如将 student 数据按 grade 排序：

    :::python
    >>> decorated = [(student.grade, i, student) for i, student in enumerate(student_objects)]
    >>> decorated.sort()
    >>> [student for grade, i, student in decorated]               # undecorate
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

这种方法的另一个名字是 [Schwartzian transform][8]，有兴趣的可以去了解一下。

## 以前的实现方式(使用 cmp 参数)

Python 2.4 之前惯用的另一种方法是使用 cmp 参数：

    :::python
    >>> def numeric_compare(x, y):
            return x - y
    >>> sorted([5, 2, 4, 1, 3], cmp=numeric_compare)
    [1, 2, 3, 4, 5]

倒序：

    :::python
    >>> def reverse_numeric(x, y):
            return y - x
    >>> sorted([5, 2, 4, 1, 3], cmp=reverse_numeric)
    [5, 4, 3, 2, 1]

Python 3 不再支持 cmp 参数，那么如果转换之前的程序呢？可以使用下面的代码：

    :::python
    def cmp_to_key(mycmp):
        'Convert a cmp= function into a key= function'
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
        return K

用法：

    :::python
    >>> sorted([5, 2, 4, 1, 3], key=cmp_to_key(reverse_numeric))
    [5, 4, 3, 2, 1]

在 Python 2.7 中，`cmp_to_key()` 工具已经被内置到 [functools][9] 模块中。


## 其他

* 对于本地化排序，可以使用 [locale.strxfrm()][11] 作为 key 函数或使用 [locale.strcoll()][12] 作为比较函数。

* `reverse` 参数依然能够保存排序的稳定性（比如，拥有相同记录的 keys 依旧保留了原来的顺序），有趣的是，就算是不使用该参数也可以通过使用两次 `reversed` 函数来实现这种效果：

        :::python
        >>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
        >>> assert sorted(data, reverse=True) == list(reversed(sorted(reversed(data))))

* 如果想给类排序的话，只需添加相关的比较方法：

        :::python
        >>> Student.__eq__ = lambda self, other: self.age == other.age
        >>> Student.__ne__ = lambda self, other: self.age != other.age
        >>> Student.__lt__ = lambda self, other: self.age < other.age
        >>> Student.__le__ = lambda self, other: self.age <= other.age
        >>> Student.__gt__ = lambda self, other: self.age > other.age
        >>> Student.__ge__ = lambda self, other: self.age >= other.age
        >>> sorted(student_objects)
        [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

    一般情况下，只需定义上面6个比较操作就可以了。[functools.total_ordering][10] 类装饰器可以很方便就实现这个需求。

* key 函数也可以不访问要排序对象的相关数据，访问外部资源也是可以的。比如，学生成绩存储在一个字典中，这个字典可以用来对学生名字进行排序：

        :::python
        >>> students = ['dave', 'john', 'jane']
        >>> newgrades = {'john': 'F', 'jane':'A', 'dave': 'C'}
        >>> sorted(students, key=newgrades.__getitem__)
        ['jane', 'dave', 'john']


<!--## 参考-->

<!--* [TimSort 中的核心过程 - YD Blog - ITeye技术网站](http://yangdong.iteye.com/blog/1170214)-->

[1]: http://wiki.python.org/moin/HowTo/Sorting/
[2]: http://docs.python.org/library/operator.html#module-operator
[3]: http://docs.python.org/2/library/operator.html#operator.itemgetter
[4]: http://docs.python.org/2/library/operator.html#operator.attrgetter
[5]: http://docs.python.org/2/library/operator.html#operator.methodcaller
[6]: http://en.wikipedia.org/wiki/Sorting_algorithm#Stability
[7]: http://en.wikipedia.org/wiki/Timsort
[8]: http://en.wikipedia.org/wiki/Schwartzian_transform
[9]: http://docs.python.org/2/library/functools.html#functools.cmp_to_key
[10]: http://docs.python.org/2/library/functools.html#functools.total_ordering
[11]: http://docs.python.org/2/library/locale.html#locale.strxfrm
[12]: http://docs.python.org/2/library/locale.html#locale.strcoll
