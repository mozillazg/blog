title: 怎么给 django class view 增加权限判断
slug: django-check-user-permission-for-class-generic-view
date: 2015-11-03


本文将讲述如何给 django 项目内的 class view 增加权限控制。


至少有两种方法：

1. 定义一个基类，重写 as_view 方法，在 as_view 方法中判断用户权限。然后其他 class view 继承这个基类
    
    from django.contrib.auth.decorators import login_required

    class LoginRequiredMixin(object):
        @classmethod
        def as_view(cls, **initkwargs):
            view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
            return login_required(view)
    
    
2. 定义一个基类，重写 dispatch 方法，给这个加个权限判断的装饰器。然后其他 class view 继承这个基类
    
    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator
    from django.views.generic import TemplateView

    class ProtectedView(TemplateView):
        template_name = 'secret.html'

        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
            return super(ProtectedView, self).dispatch(*args, **kwargs)


如果所需的权限不只是 login_required 该怎么判断权限呢？还是上面的方法，我就举一个第一种方法的例子。

    class User(models.Model):
        ...
        
        def is_god(self):
            ....
    
    
    class GodOnlyView(TemplateView):
        ...

假设有上面的 user 和 class view，其中 `OnlyGodView` 只允许 `user.is_god() 为 `True` 用户才能查看。

首先，我们定义一个 `GodRequiredMixin`:

    from django.contrib.auth.decorators import user_passes_test
    from django.core.urlresolvers import reverse_lazy

    LOGIN_URL = reverse_lazy('login')


    def god_check(user):
        return user.is_authenticated() and user.is_god()


    class GodRequiredMixin(object):

        @classmethod
        def as_view(cls, **initkwargs):
            view = super(GodRequiredMixin, cls).as_view(**initkwargs)
            actual_decorator = user_passes_test(
                god_check, login_url=LOGIN_URL
            )
            return actual_decorator(view)
    
然后定义 class view 的时候继承自这个 Mixin:

    
    class GodOnlyView(GodRequiredMixin, TemplateView):
        ...

现在我们的 `GodOnlyView` 只有当用户是 `is_god()` 的时候才能查看了。


## 参考资料

* [Applying permissions to generic views | Using the Django authentication system | Django documentation | Django](https://docs.djangoproject.com/en/1.8/topics/auth/default/#applying-permissions-to-generic-views)
* [login_required | Using the Django authentication system | Django documentation | Django](https://docs.djangoproject.com/en/1.8/topics/auth/default/#django.contrib.auth.decorators.login_required)
* [Mixins that wrap as_view() | Introduction to class-based views | Django documentation | Django](https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/#mixins-that-wrap-as-view)
* [Decorating the class | Introduction to class-based views | Django documentation | Django](https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/#decorating-the-class)