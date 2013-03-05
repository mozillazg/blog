Title: [django]复制/克隆一条查询结果
Date: 2013-02-24
Tags: python, django
Slug: django-copy-or-clone-a-query-result-and-insert-it-into-database

复制/克隆一条查询结果，并将它插入到数据库中：

将 pk 值设为 None 即可：

    :::python
    blog = Blog(name='My blog', tagline='Blogging is easy')
    blog.save() # post.pk == 1

    blog.pk = None
    blog.save() # post.pk == 2

如果该 model 继承于另一个 model 的话，必须将 `pk` 和 `id` 的值都设为 None:

    :::python
    class ThemeBlog(Blog):
        theme = models.CharField(max_length=200)

    django_blog = ThemeBlog(name='Django', tagline='Django is easy', theme='python')
    django_blog.save() # django_blog.pk == 3


    django_blog.pk = None
    django_blog.id = None
    django_blog.save() # django_blog.pk == 4

需要注意都是：这种方法不会复制相关对象。如果想复制相关（类似多对对的）对象的话，需要先将相关对象取出来然后在保存到新的对象中。例如，`Entry` 与 `Author` 是多对多关系：

    :::python
    entry = Entry.objects.all()[0] # some previous entry
    old_authors = entry.authors.all()
    entry.pk = None
    entry.save()
    entry.authors = old_authors # saves new many2many relations

## 参考

* [python - How do I clone a Django model instance object and save it to the database? - Stack Overflow](http://stackoverflow.com/questions/4733609/how-do-i-clone-a-django-model-instance-object-and-save-it-to-the-database)
* [Making queries | Django documentation | Django ](https://docs.djangoproject.com/en/dev/topics/db/queries/#copying-model-instances)
