[django]解决 django 模板中无法正常输入 {{ 或 {%
========================================================================================

:date: 2015-03-07
:slug: django-how-to-both-use-javascript-template-and-django-template

默认情况下，模板中的 ``{{`` 和 ``{%`` 会被当作是 django 模板引擎标签和过滤器的关键字。
如果我们所用的 javascript 模板引擎的关键字也是 ``{{`` 或 ``{%`` 的话，会出现无法正常输入 ``{{`` 或 ``{%`` 的情况。


比如，下面的模板代码:

.. code-block:: html+django

    <script id="template" type="x-tmpl-mustache">
        {{#stooges}}
          <li>{{name}}</li>
        {{/stooges}}
        {% test %}
    </script>

会报如下错误::

    TemplateSyntaxError at /foo/bar/
    Could not parse the remainder: '#stooges' from '#stooges'

有下面四种解决办法：

* 临时关掉模板引擎 `[ref]`__ :

.. code-block:: html+django

     {% verbatim %}
     <script id="template" type="x-tmpl-mustache">
       {{#stooges}}
       <li>{{name}}</li>
       {{/stooges}}
       {% test %}
     </script>
     {% endverbatim %}

* 修改 javascript 模板引擎的关键字
* 使用 ``templatetag`` 标签 `[ref]`__ :

.. code-block:: html+django

     <script id="template" type="x-tmpl-mustache">
       {% templatetag openvariable %}#stooges{% templatetag closevariable %}
       <li>{% templatetag openvariable %}name{% templatetag closevariable %}</li>
       {% templatetag openvariable %}/stooges{% templatetag closevariable %}
       {% templatetag openblock %} test {% templatetag closeblock %}
     </script>

* 自定义几个标签，用于输入包含关键字的字符串:

.. code-block:: django

     @register.simple_tag()
     def brace(str):
         return "{%s}" % str


     @register.simple_tag()
     def double_brace(str):
         return "{{%s}}" % str

.. code-block:: html+django

     <script id="template" type="x-tmpl-mustache">
       {% double_brace "#stooges" %}
       <li>{% double_brace "name" %}</li>
       {% double_brace "/stooges" %}
       {% brace "% test %" %}
     </script>

__ https://docs.djangoproject.com/en/1.7/ref/templates/builtins/#verbatim
__ https://docs.djangoproject.com/en/1.7/ref/templates/builtins/#templatetag


参考资料
----------

* http://stackoverflow.com/questions/7985594/django-and-mustache-use-the-same-syntax-for-template
* https://docs.djangoproject.com/en/1.7/ref/templates/builtins/
* https://docs.djangoproject.com/en/1.7/howto/custom-template-tags/