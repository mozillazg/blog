Title: [django]__unicode__: Bad Unicode data 问题
Date: 2013-05-05
Tags: django, python
Slug: django-__unicode__-bad-unicode-data

问题：

    :::python
    >> models.Foo.objects.all()
    >> [<Foo: [Bad Unicode data]>]

解决办法：

更改 model 的 `__unicode__` 方法：

    :::python
    # Before
    def __unicode__(self):
        return '%s' % self.get_foo_display()  # it's bad

    # To
    def __unicode__(self):
        return u'%s' % self.get_foo_display()  # it's Ok

## 参考

* [Bad Unicode data · Issue #3 · coleifer/django-simple-ratings · GitHub](https://github.com/coleifer/django-simple-ratings/issues/3)
