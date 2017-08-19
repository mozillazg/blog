让我们一起来构建一个模板引擎（二）
====================================
:date: 2016-03-19
:slug: let-us-build-a-template-engine-part2
:tags: lsbate, 让我们一起来构建一个模板引擎

在 `上篇文章`_ 中我们的模板引擎实现了变量和注释功能，同时在文章的最后我给大家留了一个
问题：如何实现支持 ``if`` 和 ``for`` 的标签功能:

.. code-block:: htmldjango

    {% if user.is_admin %}
        admin, {{ user.name }}
    {% elif user.is_staff %}
        staff
    {% else %}
        others
    {% endif %}

    {% for name in names %}
        {{ name }}
    {% endfor %}

在本篇文章中我们将一起来实现这个功能。


if ... elif ... else ... endif
---------------------------------

首先我们来实现对 ``if`` 语句的支持。 ``if`` 语句的语法如下:

.. code-block:: htmldjango

    {% if True %}
    ...
    {% elif True %}
    ...
    {% else %}
    ...
    {% endif %}

我们首先要做的跟之前一样，那就是确定匹配标签语法的正则表达式。这里我们用的是下面
的正则来匹配标签语法:

.. code-block:: python

    re_tag = re.compile(r'\{% .*? %\}')

    >>> re_tag.findall('{% if True %}...{% elif True %}...{% else %}...{% endif %}')
    ['{% if True %}', '{% elif True %}', '{% else %}', '{% endif %}']

然后就是生成代码了， ``if`` 语句跟之前的变量不一样那就是：需要进行缩进切换，这一点需要注意一下。

下面我们来看一下为了支持 ``if`` 标签增加了哪些代码吧(完整代码可以从 Github 上下载 `template2a.py`_ ):

.. code-block:: python

    class Template:

        def __init__(self, ...):
            # ...
            # 注释
            self.re_comment = re.compile(r'\{# .*? #\}')
            # 标签
            self.re_tag = re.compile(r'\{% .*? %\}')
            # 用于按变量，注释，标签分割模板字符串
            self.re_tokens = re.compile(r'''(
                (?:\{\{ .*? \}\})
                |(?:\{\# .*? \#\})
                |(?:\{% .*? %\})
            )''', re.X)

            # 生成 def __func_name():
            # ...

        def _parse_text(self):
            # ...
            for token in tokens:
                # ...
                if self.re_variable.match(token):
                    # ...
                elif self.re_comment.match(token):
                    continue

                # {% tag %}
                elif self.re_tag.match(token):
                    # 将前面解析的字符串，变量写入到 code_builder 中
                    # 因为标签生成的代码需要新起一行
                    self.flush_buffer()

                    tag = token.strip('{%} ')
                    tag_name = tag.split()[0]
                    if tag_name in ('if', 'elif', 'else'):
                        # elif 和 else 之前需要向后缩进一步
                        if tag_name in ('elif', 'else'):
                            self.code_builder.backward()
                        self.code_builder.add_line('{}:'.format(tag))
                        # if 语句条件部分结束，向前缩进一步，为下一行做准备
                        self.code_builder.forward()
                    elif tag_name in ('endif',):
                        # if 语句结束，向后缩进一步
                        self.code_builder.backward()

                else:
                    # ...

上面代码的关键点是生成代码时的缩进控制:

* 在遇到 ``if`` 的时候, 需要在 ``if`` 这一行之后将缩进往前移一步
* 在遇到 ``elif`` 和 ``else`` 的时候, 需要将缩进先往后移一步，待 ``elif``/ ``else`` 那一行完成后还需要把缩进再移回来
* 在遇到 ``endif`` 的时候, 我们知道此时 ``if`` 语句已经结束了，需要把缩进往后移一步，
  离开 ``if`` 语句的主体部分

我们来看一下生成的代码:

.. code-block:: python

    >>> from template2a import Template
    >>> t = Template('''
       ... {% if score >= 80 %}
       ... A
       ... {% elif score >= 60 %}
       ... B
       ... {% else %}
       ... C
       ... {% endif %}
       ... ''')
    >>> t.code_builder
    def __func_name():
        __result = []
        __result.extend(['\n'])
        if score >= 80:
            __result.extend(['\nA\n'])
        elif score >= 60:
            __result.extend(['\nB\n'])
        else:
            __result.extend(['\nC\n'])
        __result.extend(['\n'])
        return "".join(__result)

代码中的 ``if`` 语句和缩进没有问题。下面再看一下 ``render`` 的结果:

.. code-block:: python

    >>> t.render({'score': 90})
     '\n\nA\n\n'
    >>> t.render({'score': 70})
     '\n\nB\n\n'
    >>> t.render({'score': 50})
     '\n\nC\n\n'

对 ``if`` 语句的支持就这样实现了。有了这次经验下面让我们一起来实现对 ``for`` 循环的支持吧。


for ... endfor
------------------

模板中的 ``for`` 循环的语法如下:

.. code-block:: htmldjango

    {% for name in names %}
        ...
    {% endfor %}

从语法上可以看出来跟 ``if`` 语句是很相似了，甚至比 ``if`` 语句还要简单。只需在原有 ``if`` 语句代码
的基础上稍作修改就可以(完整版可以从 Github 上下载 `template2b.py`_ ):

.. code-block:: python

    class Template:

        # ...

        def _parse_text(self):
            # ...
                elif self.re_tag.match(token):
                    # ...
                    if tag_name in ('if', 'elif', 'else', 'for'):
                        # ...
                    elif tag_name in ('endif', 'endfor'):
                        # ...

可以看到其实就是修改了两行代码。按照惯例我们先来看一下生成的代码:

.. code-block:: python

    >>> from template2b import Template
    >>> t = Template('''
       ... {% for number in numbers %}
       ... {{ number }}
       ... {% endfor %}
       ... ''')
    >>> t.code_builder
    def __func_name():
        __result = []
        __result.extend(['\n'])
        for number in numbers:
            __result.extend(['\n',str(number),'\n'])
        __result.extend(['\n'])
        return "".join(__result)

``render`` 效果:

.. code-block:: python

    >>> t.render({'numbers': range(3)})
    '\n\n0\n\n1\n\n2\n\n'

``for ... endfor`` 语法就这样实现了。是不是很简单😄？但是还没完😁

相信大家都知道在 python 中 ``for`` 循环其实还支持 ``break`` 和 ``else`` 。
下面我们就一起来让我们的模板引擎的 ``for`` 语法支持 ``break`` 和 ``else`` （可以从 Github 上下载: `template2c.py`_ ）

.. 至于如何让我们都模板都 ``for`` 标签也支持 ``break`` 和 ``else`` 这个任务就
.. 交给大家自己去实现了（也可以从 Github 上下载我的实现: `template2c.py`_ ）。

.. code-block:: python

        class Template:

            # ...

            def _parse_text(self):
                # ...
                    elif self.re_tag.match(token):
                        # ...
                        if tag_name in ('if', 'elif', 'else', 'for'):
                            # ...
                        elif tag_name in ('break',):
                            self.code_builder.add_line(tag)
                        elif tag_name in ('endif', 'endfor'):
                            # ...

可以看到，其实也是只增加了两行代码。效果：

.. code-block:: python

    from template2c import Template

    >>> t = Template('''
    ... {% for number in numbers %}
    ...    {% if number > 2 %}
    ...       {% break %}
    ...    {% else %}
    ...       {{ number }}
    ...    {% endif %}
    ... {% else %}
    ...    no break
    ... {% endfor %}
    ... ''')
    >>> t.code_builder
    def __func_name():
        __result = []
        __result.extend(['\n'])
        for number in numbers:
            __result.extend(['\n   '])
            if number > 2:
                __result.extend(['\n      '])
                break
                __result.extend(['\n   '])
            else:
                __result.extend(['\n      ',str(number),'\n   '])
            __result.extend(['\n'])
        else:
            __result.extend(['\n   no break\n'])
        __result.extend(['\n'])
        return "".join(__result)
    
    >>> t.render({'numbers': range(3)}).replace('\n', '')
    '         0            1            2      no break'
    >>> t.render({'numbers': range(4)}).replace('\n', '')
    '         0            1            2            '

就这样我们的模板引擎对 ``for`` 的支持算是比较完善了。
至于生成的代码里的换行和空格暂时先不管，留待之后优化代码的时候再处理。

重构
-------

我们的 ``Template._parse_text`` 方法代码随着功能的增加已经变成下面这样了:

.. code-block:: python

    def _parse_text(self):
        """解析模板"""
        tokens = self.re_tokens.split(self.raw_text)

        for token in tokens:
            if self.re_variable.match(token):
                variable = token.strip('{} ')
                self.buffered.append('str({})'.format(variable))
            elif self.re_comment.match(token):
                continue
            elif self.re_tag.match(token):
                self.flush_buffer()

                tag = token.strip('{%} ')
                tag_name = tag.split()[0]
                if tag_name in ('if', 'elif', 'else', 'for'):
                    if tag_name in ('elif', 'else'):
                        self.code_builder.backward()
                    self.code_builder.add_line('{}:'.format(tag))
                    self.code_builder.forward()
                elif tag_name in ('break',):
                    self.code_builder.add_line(tag)
                elif tag_name in ('endif', 'endfor'):
                    self.code_builder.backward()
            else:
                self.buffered.append('{}'.format(repr(token)))

有什么问题呢？问题就是 ``for`` 循环里的代码太长了，我们需要分割 ``for`` 循环里的
代码。比如把对变量，``if/for`` 的处理封装到单独的方法里。

下面展示了一种方法（可以从 Github 下载 `template2d.py`_ ):


.. code-block:: python


    def _parse_text(self):
        """解析模板"""
        tokens = self.re_tokens.split(self.raw_text)
        handlers = (
            (self.re_variable.match, self._handle_variable),   # {{ variable }}
            (self.re_tag.match, self._handle_tag),             # {% tag %}
            (self.re_comment.match, self._handle_comment),     # {# comment #}
        )
        default_handler = self._handle_string                  # 普通字符串

        for token in tokens:
            for match, handler in handlers:
                if match(token):
                    handler(token)
                    break
            else:
                default_handler(token)

    def _handle_variable(self, token):
        """处理变量"""
        variable = token.strip('{} ')
        self.buffered.append('str({})'.format(variable))

    def _handle_comment(self, token):
        """处理注释"""
        pass

    def _handle_string(self, token):
        """处理字符串"""
        self.buffered.append('{}'.format(repr(token)))

    def _handle_tag(self, token):
        """处理标签"""
        # 将前面解析的字符串，变量写入到 code_builder 中
        # 因为标签生成的代码需要新起一行
        self.flush_buffer()
        tag = token.strip('{%} ')
        tag_name = tag.split()[0]
        self._handle_statement(tag, tag_name)

    def _handle_statement(self, tag, tag_name):
        """处理 if/for"""
        if tag_name in ('if', 'elif', 'else', 'for'):
            # elif 和 else 之前需要向后缩进一步
            if tag_name in ('elif', 'else'):
                self.code_builder.backward()
            # if True:, elif True:, else:, for xx in yy:
            self.code_builder.add_line('{}:'.format(tag))
            # if/for 表达式部分结束，向前缩进一步，为下一行做准备
            self.code_builder.forward()
        elif tag_name in ('break',):
            self.code_builder.add_line(tag)
        elif tag_name in ('endif', 'endfor'):
            # if/for 结束，向后缩进一步
            self.code_builder.backward()

这样处理后是不是比之前那个都放在 ``_parse_text`` 方法里要好很多？

至此，我们的模板引擎已经支持了如下语法:

* 变量: ``{{ variable }}``
* 注释: ``{# comment #}``
* ``if`` 语句: ``{% if ... %} ... {% elif ... %} ... {% else %} ... {% endif %}``
* ``for`` 循环: ``{% for ... in ... %} ... {% break %} ... {% else %} ... {% endfor %}``

之后的文章还将实现其他实用的模板语法，比如 ``include``, ``extends`` 模板继承等。

``include`` 的语法(item.html 是个独立的模板文件, list.html 中 include item.html):

.. code-block:: htmldjango

    {# item.html #}
    <li>{{ item }}</li>

    {# list.html #}
    <ul>
        {% for name in names %}
            {% include "item.html" %}
        {% endfor %}
    </ul>

list.html 渲染后将生成类似下面这样的字符串:

.. code-block:: html

    <ul>
        <li>Tom</li>
        <li>Jim<li>
    </ul>

``extends`` 的语法(base.html 是基础模板, child.html 继承 base.html 然后重新定义 base.html
中定义过的 block):

.. code-block:: htmldjango

    {# base.html #}
    <div id="content">
    {% block content %}
        parent_content
    {% endblock content %}
    </div>
    <footer id="footer">
    {% block footer %}
        (c) 2016 example.com
    {% endblock footer %}
    </footer>

child.html:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        child_content
        {{ block.super }}
    {% endblock content %}

child.html 渲染后将生成类似下面这样的字符串:

.. code-block:: html

    <div id="content">
        child_content
        parent_content
    </div>
    <footer id="footer">
        (c) 2016 example.com
    </footer>


那么，该如何实现 ``include`` 和 ``extends`` 功能呢？
我将在 `第三篇文章`_ 中向你详细的讲解。敬请期待。


.. _template2a.py: https://github.com/mozillazg/lsbate/raw/master/part2/template2a.py
.. _template2b.py: https://github.com/mozillazg/lsbate/raw/master/part2/template2b.py
.. _template2c.py: https://github.com/mozillazg/lsbate/raw/master/part2/template2c.py
.. _template2d.py: https://github.com/mozillazg/lsbate/raw/master/part2/template2d.py
.. _第三篇文章: http://mozillazg.com/2016/03/let-us-build-a-template-engine-part3.html
.. _上篇文章: http://mozillazg.com/2016/03/let-us-build-a-template-engine-part1.html
