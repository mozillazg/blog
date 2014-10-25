Title: [django]在模板中对变量作减法操作
Date: 2013-02-25
Tags: django, python
Slug: django-variable-subtraction-in-django-templates


我们知道可以使用内置过滤器 `add` 对变量做加法操作：

    :::django
    {{ 3|add:"1" }}   # 4

其实，`add` 也可以做减法操作：

    :::django
    {{ 3|add:"-1" }}  # 2


## 参考

* [Variable subtraction in django templates - Stack Overflow](http://stackoverflow.com/questions/9948095/variable-subtraction-in-django-templates)
