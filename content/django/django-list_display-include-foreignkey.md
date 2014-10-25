Title: [django]list_display 中包含外键内的字段
Date: 2013-04-18
Tags: django, python, list_display, admin
Slug: django-admin-list_display-include-foreignkey

本文将实现 list_display 中包含外键内的字段，同样适用于自定义要显示的列。

比如包含 User 中的 email 地址。

![image](/static/images/2013-4-18-01.png)

admin.py:

    :::python
    class HelloAdmin(admin.ModelAdmin):
        list_display = ('user', 'user_email', 'role')
        # ...

        # 显示用户邮箱地址
        def user_email(self, obj):
            return u'%s' % obj.user.email
        user_email.short_description = u'邮箱'

    admin.site.register(Hello, HelloAdmin)

## 参考

* [Django - Include data from foreignkey in admin list_display function - Stack Overflow](http://stackoverflow.com/questions/4013585/django-include-data-from-foreignkey-in-admin-list-display-function)
