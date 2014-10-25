Title: [django]合并多个查询结果集(queryset)并按字段排序
Date: 2013-03-28
Tags: django, python, queryset, sort, merge
Slug: django-merge-queryset-then-sort

## 需求

合并博文的喜爱及转发信息，并按时间排序。

相关 models :

    :::python
    class Post(models.Model):
        #...

        created_at = models.DateTimeField(auto_now_add=True)
        reblog_from = models.ForeignKey('self', null=True, blank=True)

        #...


    class Like(models.Model):
        #...

        post = models.ForeignKey(Post)
        created_at = models.DateTimeField(auto_now_add=True)

        #...

## 解决方案

    :::python
    from itertools import chain
    from operator import attrgetter

    #...

    post = Post.objects.get(pk=post_id)  # 获取博文
    likes = likes = post.like_set.all()  # 获取喜爱信息
    # likes = Like.objects.filter(post=post)
    reblogs = Post.objects.filter(reblog_from=post)  # 获取转发信息

    # 合并喜爱及转发信息，并按时间逆序排序
    notes = sorted(chain(likes, reblogs), key=attrgetter('created_at'),
                   reverse=True)

    #...

**使用 itertools.chain 函数合并可迭代对象**：

    :::python
    >>> list(chain([1, 2, 3], 'abc'))
    >>> [1, 2, 3, 'a', 'b', 'c']


**使用 sorted 函数排序（按对象属性排序）**。
关于排序请参考博文：
[\[python\]排序（Sorting Mini-HOW TO）](http://mozillazg.com/2013/03/python-sorting-how-to.html)

## 参考

* [itertools — Functions creating iterators for efficient looping — Python v2.7.3 documentation](http://docs.python.org/2/library/itertools.html#itertools.chain)
* [\[python\]排序（Sorting Mini-HOW TO）](http://mozillazg.com/2013/03/python-sorting-how-to.html)
