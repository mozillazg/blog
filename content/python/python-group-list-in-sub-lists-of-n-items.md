Title: [python]将列表分组成包含多个子列表的列表
Date: 2013-02-19
Tags: python
Slug: python-group-list-in-sub-lists-of-n-items

想取得的效果是： [1, 2, 3, 4, 5, 6, 7] --> [[1, 2, 3], [4, 5, 6], [7]]

下面三种方法取自博文 <http://sandrotosi.blogspot.com/2011/04/python-group-list-in-sub-lists-of-n.html> 及评论。

## 第一种方法

    def group_iter(iterator, n=2):
        """ Given an iterator, it returns sub-lists made of n items
        (except the last that can have len < n)
        inspired by http://countergram.com/python-group-iterator-list-function"""
        accumulator = []
        for item in iterator:
            accumulator.append(item)
            if len(accumulator) == n: # tested as fast as separate counter
                yield accumulator
                accumulator = [] # tested faster than accumulator[:] = []
                # and tested as fast as re-using one list object
        if len(accumulator) != 0:
            yield accumulator

效果：

    >>> group_iter([1, 2, 3, 4, 5, 6], 3)
    <generator object group_iter at 0x02A43418>
    >>> list(group_iter([1, 2, 3, 4, 5, 6], 3))
    [[1, 2, 3], [4, 5, 6]]
    >>> list(group_iter([1, 2, 3, 4, 5, 6], 4))
    [[1, 2, 3, 4], [5, 6]]

## 第二种方法：

    >>> original_list = [1, 2, 3, 4, 5, 6]
    >>> list_size = 5
    >>> [original_list[i:i+list_size] for i in xrange(0, len(original_list), list_size)]
    [[1, 2, 3, 4, 5], [6]]
    >>>

## 第三种方法：

    def splitarray(array, gsize):
        arraylen = len(array)
        for i in range(arraylen / gsize):
            yield array[i * gsize:(i * gsize) + gsize]
        if arraylen % gsize != 0:
            yield array[-(arraylen % gsize):]

效果：

    >>> original_list = [1, 2, 3, 4, 5, 6]
    >>> list_size = 5
    >>> [original_list[i:i+list_size] for i in xrange(0, len(original_list), list_size)]
    [[1, 2, 3, 4, 5], [6]]
    >>>


## 参考

* [Group a list into sequential n-tuples « Python recipes « ActiveState Code](http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/)
* [Sandro Tosi: Python: group a list in sub-lists of n items](http://sandrotosi.blogspot.com/2011/04/python-group-list-in-sub-lists-of-n.html)
* [Gary Robinson's Rants: Splitting a Python list into sublists](http://www.garyrobinson.net/2008/04/splitting-a-pyt.html)
