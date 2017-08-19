让我们一起来构建一个模板引擎（四）
====================================
:date: 2016-06-01
:slug: let-us-build-a-template-engine-part4
:tags: lsbate, 让我们一起来构建一个模板引擎

在 `上篇文章`_ 中我们的模板引擎实现了对 ``include`` 和 ``extends`` 的支持，
到此为止我们已经实现了模板引擎所需的大部分功能。
在本文中我们将解决一些用于生成 html 的模板引擎需要面对的一些安全问题。

转义
-----------

首先要解决的就是转义问题。到目前为止我们的模板引擎并没有对变量和表达式结果进行转义处理，
如果用于生成 html 源码的话就会出现下面这样的问题 ( `template3c.py`_ ):

.. code-block:: python

    >>> from template3c import Template
    >>> t = Template('<h1>{{ title }}</h1>')
    >>> t.render({'title': 'hello<br />world'})
    '<h1>hello<br />world</h1>'

很明显 title 中包含的标签需要被转义，不然就会出现非预期的结果。
这里我们只对 ``&`` ``"`` ``'`` ``>`` ``<`` 这几个字符做转义处理，其他的字符可根据需要进行处理。

.. code-block:: python

    html_escape_table = {
        '&': '&amp;',
        '"': '&quot;',
        '\'': '&apos;',
        '>': '&gt;',
        '<': '&lt;',
    }


    def html_escape(text):
        return ''.join(html_escape_table.get(c, c) for c in text)

转义效果:

.. code-block:: python

    >>> html_escape('hello<br />world')
    'hello&lt;br /&gt;world'

既然有转义自然也要有禁止转义的功能，毕竟不能一刀切否则就丧失灵活性了。

.. code-block:: python

    class NoEscape:

        def __init__(self, raw_text):
            self.raw_text = raw_text


    def escape(text):
        if isinstance(text, NoEscape):
            return str(text.raw_text)
        else:
            text = str(text)
            return html_escape(text)


    def noescape(text):
        return NoEscape(text)

最终我们的模板引擎针对转义所做的修改如下(可以下载 `template4a.py`_ ):

.. code-block:: python

    class Template:
        def __init__(self, ..., auto_escape=True):
            ...
            self.auto_escape = auto_escape
            self.default_context.setdefault('escape', escape)
            self.default_context.setdefault('noescape', noescape)
            ...

        def _handle_variable(self, token):
            if self.auto_escape:
                self.buffered.append('escape({})'.format(variable))
            else:
                self.buffered.append('str({})'.format(variable))

        def _parse_another_template_file(self, filename):
            ...
            template = self.__class__(
                    ...,
                    auto_escape=self.auto_escape
            )
            ...


    class NoEscape:
        def __init__(self, raw_text):
            self.raw_text = raw_text

    html_escape_table = {
        '&': '&amp;',
        '"': '&quot;',
        '\'': '&apos;',
        '>': '&gt;',
        '<': '&lt;',
    }


    def html_escape(text):
        return ''.join(html_escape_table.get(c, c) for c in text)


    def escape(text):
        if isinstance(text, NoEscape):
            return str(text.raw_text)
        else:
            text = str(text)
            return html_escape(text)


    def noescape(text):
        return NoEscape(text)


效果:

.. code-block:: python

    >>> from template4a import Template
    >>> t = Template('<h1>{{ title }}</h1>')
    >>> t.render({'title': 'hello<br />world'})
    '<h1>hello&lt;br /&gt;world</h1>'

    >>> t = Template('<h1>{{ noescape(title) }}</h1>')
    >>> t.render({'title': 'hello<br />world'})
    '<h1>hello<br />world</h1>'
    >>>


exec 的安全问题
--------------------

由于我们的模板引擎是使用 ``exec`` 函数来执行生成的代码的，所以就需要注意一下
``exec`` 函数的安全问题，预防可能的服务端模板注入攻击（详见 `使用 exec 函数时需要注意的一些安全问题`_ ）。

首先要限制的是在模板中使用内置函数和执行时上下文变量( `template4b.py`_ ):

.. code-block:: python

    class Template:
        ...

        def render(self, context=None):
            """渲染模版"""
            namespace = {}
            namespace.update(self.default_context)
            namespace.setdefault('__builtins__', {})   # <---
            if context:
                namespace.update(context)
            exec(str(self.code_builder), namespace)
            result = namespace[self.func_name]()
            return result

效果:

.. code-block:: python

    >>> from template4b import Template
    >>> t = Template('{{ open("/etc/passwd").read() }}')
    >>> t.render()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/mg/develop/lsbate/part4/template4b.py", line 245, in render
        result = namespace[self.func_name]()
      File "<string>", line 3, in __func_name
    NameError: name 'open' is not defined

然后就是要限制通过其他方式调用内置函数的行为:

.. code-block:: python

    >>> from template4b import Template
    >>> t = Template('{{ escape.__globals__["__builtins__"]["open"]("/etc/passwd").read()[0] }}')
    >>> t.render()
    '#'
    >>>
    >>> t = Template("{{ [x for x in [].__class__.__base__.__subclasses__() if x.__name__ == '_wrap_close'][0].__init__.__globals__['path'].os.system('date') }}")
    >>> t.render()
    Mon May 30 22:10:46 CST 2016
    '0'

一种解决办法就是不允许在模板中访问以下划线 `_` 开头的属性。
为什么要包括单下划线呢，因为按照约定单下划线开头的属性是私有属性，
不应该在外部访问这些属性。

这里我们使用 ``tokenize`` 模块来帮助我们解析生成的代码，然后再找出其中的特殊属性。

.. code-block:: python

    import io
    import tokenize


    class Template:
        def __init__(self, ..., safe_attribute=True):
            ...
            self.safe_attribute = safe_attribute

        def render(self, ...):
            ...
            code = str(self.code_builder)
            if self.safe_attribute:
                check_unsafe_attributes(code)
            exec(code, namespace)
            func = namespace[self.func_name]

    def check_unsafe_attributes(s):
        g = tokenize.tokenize(io.BytesIO(s.encode('utf-8')).readline)
        pre_op = ''
        for toktype, tokval, _, _, _ in g:
            if toktype == tokenize.NAME and pre_op == '.' and \
                    tokval.startswith('_'):
                attr = tokval
                msg = "access to attribute '{0}' is unsafe.".format(attr)
                raise AttributeError(msg)
            elif toktype == tokenize.OP:
                pre_op = tokval

效果:

.. code-block:: python

    >>> from template4c import Template
    >>> t = Template("{{ [x for x in [].__class__.__base__.__subclasses__() if x.__name__ == '_wrap_close'][0].__init__.__globals__['path'].os.system('date') }}")
    >>> t.render()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/xxx/lsbate/part4/template4c.py", line 250, in render
        check_unsafe_attributes(func)
      File "/xxx/lsbate/part4/template4c.py", line 296, in check_unsafe_attributes
        raise AttributeError(msg)
    AttributeError: access to attribute '__class__' is unsafe.
    >>>
    >>> t = Template('<h1>{{ title }}</h1>')
    >>> t.render({'title': 'hello<br />world'})
    '<h1>hello&lt;br /&gt;world</h1>'


这个系列的文章到目前为止就已经全部完成了。

如果大家感兴趣的话可以尝试使用另外的方式来解析模板内容,
即: 使用词法分析/语法分析的方式来解析模板内容（欢迎分享实现过程）。


P.S. 整个系列的所有文章地址：

* `让我们一起来构建一个模板引擎（一） <http://mozillazg.com/2016/03/let-us-build-a-template-engine-part1.html>`__
* `让我们一起来构建一个模板引擎（二） <http://mozillazg.com/2016/03/let-us-build-a-template-engine-part2.html>`__
* `让我们一起来构建一个模板引擎（三） <http://mozillazg.com/2016/03/let-us-build-a-template-engine-part3.html>`__
* `让我们一起来构建一个模板引擎（四） <http://mozillazg.com/2016/06/let-us-build-a-template-engine-part4.html>`__

P.S. 文章中涉及的代码已经放到 GitHub 上了: `<https://github.com/mozillazg/lsbate>`__

2016.06.18 更新：

* 使用 ``dis`` 没法分析嵌套函数的代码，所以 ``check_unsafe_attributes`` 部分还需要再完善，
  详见 `使用 exec 函数时需要注意的一些安全问题`_ 下面的评论。

2016.07.10 更新:

* 已经改为使用 ``tokenize`` 分析生成的代码（可以分析嵌套函数）。


.. _template3c.py: https://github.com/mozillazg/lsbate/raw/master/part3/template3c.py
.. _template4a.py: https://github.com/mozillazg/lsbate/raw/master/part4/template4a.py
.. _template4b.py: https://github.com/mozillazg/lsbate/raw/master/part4/template4b.py
.. _template4c.py: https://github.com/mozillazg/lsbate/raw/master/part4/template4c.py
.. _template4d.py: https://github.com/mozillazg/lsbate/raw/master/part4/template4d.py
.. _上篇文章: http://mozillazg.com/2016/03/let-us-build-a-template-engine-part3.html
.. _使用 exec 函数时需要注意的一些安全问题: http://mozillazg.com/2016/05/python-some-security-problems-about-use-exec-function.rst.html
