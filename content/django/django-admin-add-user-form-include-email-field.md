Title: [django]让后台新增用户的表单包含 email 字段
Date: 2013-04-19
Tags: python, django, admin, UserAdmin
Slug: django-admin-add-user-form-include-email-field

默认情况下，后台新增用户的表单不包含 email 字段。
每次新增用户后都需求再次修改新增的用户来添加 email 地址。

本文将实现在新增用户的同时将 email 地址也加上，一次完成用户添加，省去一个步骤。

默认情况下：

![before](/static/images/2013-4-19-01.png)

本文将实现：

![after](/static/images/2013-4-19-02.png)


    :::python
    from django.contrib.auth.models import User
    from django.contrib.auth.admin import UserAdmin


    class MyUserAdmin(UserAdmin):
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2')
            }),
        )

    admin.site.unregister(User)
    admin.site.register(User, MyUserAdmin)

## 参考

* [Extending new user form, in the admin Django - Stack Overflow](http://stackoverflow.com/questions/6858028/extending-new-user-form-in-the-admin-django)
