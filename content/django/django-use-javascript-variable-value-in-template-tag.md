Title: [django]在模板标签中使用 javascript 变量的值作为参数
Date: 2013-05-20
Tags: django, python, javascript
Slug: django-use-javascript-variable-value-in-template-tag

示例：

    :::html+django
    var url = "{% url 'foo' 0 %}".replace('0', value);

当然，针对这个例子更好的办法是：
将 url 定义为 /foo?xxx=y 这种形式，这样就不需要使用 javascript 变量的值了。

