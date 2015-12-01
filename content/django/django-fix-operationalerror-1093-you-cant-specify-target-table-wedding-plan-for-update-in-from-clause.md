title: [django] 解决 OperationalError: (1093, "You can't specify target table 'xxx' for update in FROM clause")
slug: django-fix-operationalerror-1093-you-cant-specify-target-table-wedding-plan-for-update-in-from-clause
date: 2015-11-30 19:00:00


错误信息如下：

    OperationalError: (1093, "You can't specify target table 'xxx' for update in FROM clause")


当使用类似如下代码时，会出现以上问题：


    user_ids = User.objects.filter(
        pk__gt=10
    ).values_list('pk', flat=True)


    User.objects.filter(id__in=user_ids).update(a=123)


解决办法：将第一个结果转换为列表

    user_ids = list(user_ids)

出现问题的原因是，上面报错的代码试图生成这样的 sql 语句：

    update user set a=1234 where id in (
        select id from user where id > 10
    )

这条语句是有问题的。
而修改后的代码生成的 sql 语句是这样的:

    update user set a=1234 where id in (
        1, 2, 3
    )