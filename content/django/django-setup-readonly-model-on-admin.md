title: 如何在 django admin site 中设置某个 model 只读
slug: django-setup-readonly-model-on-admin
date: 2015-09-16


本文主要讲解如何在 django 1.8.4 项目的 admin-site 中配置一个只读的 model。

1. 禁用添加操作，主要是重写 `has_delete_permission` 方法：

        def has_add_permission(self, request):
            return False

2. 禁用修改操作，这里有两种方法

    * 第一种是重写 `has_change_permission` 方法
        
            def has_change_permission(self, request, obj=None):
                if obj is None:     # 显示列表页
                    return True
                else:               # 禁用详情页
                    return False
   
      效果是无法查看详情页，间接实现了禁用修改操作
      
    * 第二种是定义 `readonly_fields` 属性
    
            readonly_fields = [field.name for field in ModelName._meta.fields]

      效果是详情页的所有表单项只读，间接实现了禁用修改操作
      
3. 禁用删除操作，主要是重写 `has_delete_permission` 方法以及禁用 actions:

        actions = None
        def has_delete_permission(self, request, obj=None):
            return False


完整代码举例 (admin.py)：

    @admin.register(Foo)
    class FooAdmin(admin.ModelAdmin):
        actions = None

        def has_add_permission(self, request):
            return False

        def has_change_permission(self, request, obj=None):
            if obj is None:
                return True
            else:
                return False

        def has_delete_permission(self, request, obj=None):
            return False
    
    
    @admin.register(Bar)
    class BarAdmin(admin.ModelAdmin):
        readonly_fields = [field.name for field in Bar._meta.fields]
        actions = None

        def has_add_permission(self, request):
            return False

        def has_delete_permission(self, request, obj=None):
            return False


demo 项目: [admin\_readonly\_model](https://github.com/mozillazg/django-simple-projects/tree/master/projects/admin_readonly_model)


## 参考资料

* [The Django admin site | Django documentation | Django](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/#django.contrib.admin.ModelAdmin.has_add_permission)
        