Title: [django]编写作用于视图（view）的装饰器（Decorator）
Date: 2013-02-23
Tags: python, django, decorator, 装饰器
Slug: django-custom-decorators-optional-keyword-arguments-for-views

本文假设读者已经知道如何编写基本的装饰器代码，否则请自行 google：“python 装饰器”and/or “python decorator”。

## 不带参数的装饰器

<!--分两种情况：-->

<!--* 视图函数只有一个 request 参数-->


    :::python
    def object_does_not_exist(func):
        def returned_wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                raise Http404()
        return returned_wrapper

用法：

    :::python
    @object_does_not_exist
    def detail(request):
        pass

## 带参数的装饰器

* 第一种写法：

        :::python
        def object_does_not_exist(redirect=None):
            def decorator(func):
                def returned_wrapper(request, *args, **kwargs):
                    try:
                        return func(request, *args, **kwargs)
                    except ObjectDoesNotExist:
                        if redirect:
                            return HttpResponseRedirect(redirect)
                        else:
                            raise Http404()
                return returned_wrapper
            return decorator
  用法：

        :::python
        @object_does_not_exist(redirect='/')
        def detail(request):
            pass


        # 记得加个闭合括号，否则会出现类似 takes exactly 1 argument (0 given) 的错误
        @object_does_not_exist()
        def foo(request):
            pass


* 第二种写法：

        :::python
        def object_does_not_exist(func=None, redirect=None):
            def decorator(func):
                def returned_wrapper(request, *args, **kwargs):
                    try:
                        return func(request, *args, **kwargs)
                    except ObjectDoesNotExist:
                        if redirect:
                            return HttpResponseRedirect(redirect)
                        else:
                            raise Http404()
                return returned_wrapper

            if not func:
                def foo(func):
                    return decorator(func)
                return foo

            else:
                return decorator(func)
  用法：

        :::python
        @object_does_not_exist(redirect='/')
        def detail(request):
            pass


        @object_does_not_exist
        def foo(request):
            pass


第二种方法可以解决 `got an unexpected keyword argument` 错误。

## 参考

* [Type and Flow: Python Decorator with Optional Keyword Arguments](http://typeandflow.blogspot.com/2011/06/python-decorator-with-optional-keyword.html)
* <https://github.com/django/django/blob/master/django/contrib/auth/decorators.py>
* <https://github.com/django/django/blob/master/django/utils/http.py>
* [Signature Preserving Function Decorators | Numerical Recipes](http://numericalrecipes.wordpress.com/2009/05/25/signature-preserving-function-decorators/)
* [Python decorator notes - Helpful](http://helpful.knobs-dials.com/index.php/Python_decorator_notes#To_the_decorated_function)
