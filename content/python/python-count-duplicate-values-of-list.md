Title: [python]统计列表中重复项的出现次数
Date: 2013-08-17
Tags: python, list
Slug: python-count-duplicate-values-of-list

列表项由数字、字符串组成，统计重复项：

    :::python
    >>> from collections import defaultdict
    >>> d = defaultdict(int)
    >>> for x in [1, 2, 3, 1, 2, 3, 1]:
    ...     d[x] += 1
    ...
    >>> dict(d)
    {1: 3, 2: 2, 3: 2}
    >>>
    >>> c = defaultdict(int)
    >>> for y in ['a', 'b', 'a', 'c', 'c']:
    ...     c[y] += 1
    ...
    >>> dict(c)
    {'a': 2, 'c': 2, 'b': 1}


列表项由字典组成，统计某一键值的重复数：

    :::python
    >>> e = defaultdict(int)
    >>> for x in [{'a': 1, 'b': 1}, {'a': 2, 'b':1}, {'a': 1, 'c': 3}]:
    ...     e[x['a']] += 1
    ...
    >>> dict(e)   # 'a': 1 出现2次，'a': 2 出现1次
    {1: 2, 2: 1}


## 参考

* [dictionary - counting duplicate words in python the fastest way - Stack Overflow](http://stackoverflow.com/questions/14374568/counting-duplicate-words-in-python-the-fastest-way)
