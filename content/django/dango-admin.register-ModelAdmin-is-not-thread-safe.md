Title: django @admin.register 线程安全陷阱
Date: 2015-07-27
Tags: Thread-Locals
Slug: dango-admin.register-ModelAdmin-is-not-thread-safe

一直以为注册的 ModelAdmin 是线程安全的，直到最近看到[有人提到](http://stackoverflow.com/questions/727928/django-admin-how-to-access-the-request-object-in-admin-py-for-list-display-met#comment27035661_729879) ModelAdmin 不是线程安全的。


然后看了一下 Django admin.register 的源码，才发现确实不是线程安全的。 [核心代码](https://github.com/django/django/blob/927b30a6ab33ea33e5e3b1e7408ac1d5d267ff6a/django/contrib/admin/sites.py#L110) 如下：

    # Instantiate the admin class to save in the registry
    self._registry[model] = admin_class(model, self)

当配置如下代码后：

    @admin.register(Foo)
    class FooAdmin(admin.ModelAdmin):
        pass
实际上注册的是一个 FooAdmin 示例，也就是说 FooAdmin 这个类在启动的时候就初始化，所有的请求访问的都是同一个实例。
所以类似下面的代码就会有非线程安全的问题，因为 FooAdmin 实例(self)会共享给所有子线程/所有请求：

    @admin.register(Foo)
    class FooAdmin(admin.ModelAdmin):
    
    def foobar(self):
        print(self.param)
    
    def changelist_view(self, request, extra_context=None):
        self.param = request.GET['param']
        return super(FooAdmin,self).changelist_view(request, extra_context=extra_context)

对于使用多线程的服务，可以使用 Thread-Locals 解决这个问题:

    from threading import local
    g = local()
    
    @admin.register(Foo)
    class FooAdmin(admin.ModelAdmin):
    
    def foobar(self):
        print(g.param)
    
     def changelist_view(self, request, extra_context=None):
        g.param = request.GET['param']
        return super(FooAdmin,self).changelist_view(request, extra_context=extra_context)

对于使用协程（比如，使用 gevent）的服务，可以用 werkzeug.local.Local:

    from werkzeug.local import Local
    g = Local()
    
    # ...



## 参考资料

* http://stackoverflow.com/questions/727928/django-admin-how-to-access-the-request-object-in-admin-py-for-list-display-met#comment27035661_729879
* https://github.com/django/django/blob/927b30a6ab33ea33e5e3b1e7408ac1d5d267ff6a/django/contrib/admin/sites.py#L110
* http://stackoverflow.com/questions/1408171/thread-local-storage-in-python
* http://werkzeug.pocoo.org/docs/0.10/local/#werkzeug.local.LocalProxy