Title: [django]更改 request.GET 字典的键值时出现 "AttributeError: This QueryDict instance is immutable" 错误
Date: 2013-08-31
Author: mozillazg
Tags: django, querydict, python
Slug: django-attributeerror-this-querydict-instance-is-immutable

当修改 request.GET/request.POST 时，会出现: "AttributeError: This QueryDict instance is immutable":

    :::python
    def foobar(request):
        #...
        request.GET['foo'] = bar  # AttributeError: This QueryDict instance is immutable
        #...

因为默认的 QueryDict 是**不可修改**的。解决办法就是复制一份副本，对副本进行修改：

    :::python
    def foobar(request):
        #...
        request.GET = request.GET.copy()  # 添加这一句
        request.GET['foo'] = bar
        #...


## 参考

* [Changing request.POST values (QueryDict instance is immutable) | Django foo](http://www.djangofoo.com/67/changing-request-post-values-querydict-immutable)
* [django - cannot urlencode() after storing QueryDict in session - Stack Overflow](http://stackoverflow.com/questions/7067020/cannot-urlencode-after-storing-querydict-in-session/7068497#7068497)
