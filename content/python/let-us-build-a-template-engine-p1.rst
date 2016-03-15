让我们一起来构建一个模版引擎（一）
====================================
:date: 2016-03-15
:slug: let-us-build-a-template-engine-part1
:tags: lsbate, 让我们一起来构建一个模版引擎

假设我们要生成下面这样的 html 字符串:

.. code-block:: html

    <div>
        <p>welcome, Tom</p>
        <ul>
            <li>age: 20</li>
            <li>weight: 100</li>
            <li>height: 170</li>
        </ul>
    </div>

要求姓名以及 ``<ul></ul>`` 中的内容是根据变量动态生成的，也就是这样的:

.. code-block:: htmldjango


    <div>
        <p>welcome, {name}</p>
        <ul>
            {info}
        </ul>
    </div>

没接触过模版的同学可能会想到使用字符串格式化的方式来实现:

.. code-block:: python

    HTML = '''
    <div>
        <p>welcome, {name}</p>
        <ul>
            {info}
        </ul>
    </div>
    '''


    def gen_html(person):
        name = person['name']
        info_list = [
            '<li>{0}: {1}</li>'.format(item, value)
            for item, value in person['info'].items()
        ]
        info = '\n'.join(info_list)
        return HTML.format(name=name, info=info)

这种方案有一个很明显的问题那就是，需要拼接两个 html 片段。
使用过模版技术的同学应该很容易就想到，在 Web 开发中生成 HTML 的更常用的办法是使用模版:

.. code-block:: python

    HTML = '''
    <div>
        <p>welcome, {{ person['name'] }}</p>
        <ul>
            {% for item, value in person['info'].items() %}
            <li>{{ item }}: {{ value }}</li>
            {% endfor %}
        </ul>
    </div>
    '''


    def gen_html(person):
        return Template(HTML).render(person=person)

本系列文章要讲的就是如何从零开始实现一个这样的模版引擎( ``Template`` )。


使用技术
----------

我们将使用将模版编译为 python 代码的方式来解析和渲染模版。
比如上面的模版将被编译为如下 python 代码:

.. code-block:: python

    def render_function():
        result = []

        result.extend([
            '<div>\n',
            '<p>welcome, '
            str(person['name']),
            '</p>\n',
            '<ul>\n'
        ])
        for item, value in person['info'].items():
            result.extend([
                '<li>',
                str(item),
                ': ',
                value,
                '</li>\n'
            ])
        result.extend([
            '</ul>\n'
            '</div>\n'
        ])
        return ''.join(result)

然后通过 ``exec`` 执行生成的代码，之后再执行 ``render_function()`` 就可以得到我们需要的 html 字符串了:

.. code-block:: python


    namespace = {'person': person}
    exec(code, namespace)
    render_functio = namespace['render_function']
    html = render_function()

模版引擎的核心技术就是这些了，下面让我们一步一步的实现它吧。


CodeBuilder
--------------

我们都知道 python 代码是高度依赖缩进的，所以我们需要一个对象用来保存我们生成代码时的当前缩进情况，
同时也保存已经生成的代码行（可以直接在 github 上下载 `template1a.py`_ ）:

.. code-block:: python

    # -*- coding: utf-8 -*-
    # tested on Python 3.5.1


    class CodeBuilder:
        INDENT_STEP = 4     # 每次缩进的空格数

        def __init__(self, indent=0):
            self.indent = indent    # 当前缩进
            self.lines = []         # 保存一行一行生成的代码

        def forward(self):
            """缩进前进一步"""
            self.indent += self.INDENT_STEP

        def backward(self):
            """缩进后退一步"""
            self.indent -= self.INDENT_STEP

        def add(self, code):
            self.lines.append(code)

        def add_line(self, code):
            self.lines.append(' ' * self.indent + code)

        def __str__(self):
            """拼接所有代码行后的源码"""
            return '\n'.join(map(str, self.lines))

        def __repr__(self):
            """方便调试"""
            return str(self)

``forward`` 和 ``backward`` 方法可以用来控制缩进前进或后退一步，比如在生成 ``if`` 语句的时候::

    if age > 13:      # 生成完这一行以后，需要切换缩进了 ``forward()``
        ...
        ...           # 退出 if 语句主体的时候，同样需要切换一次缩进 ``backward()``
    ...


Template
-----------

这个模版引擎的核心部分就是一个 ``Template`` 类，用法:

.. code-block:: python

    # 实例化一个 Template 对象
    template = Template('''
    <h1>hello, {{ name }}</h1>
    {% for skill in skills %}
        <p>you are good at {{ skill }}.</p>
    {% endfor %}
    ''')

    # 然后，使用一些数据来渲染这个模版
    html = template.render(
        {'name': 'Eric', 'skills': ['python', 'english', 'music', 'comic']}
    )

一切魔法都在 ``Template`` 类里。下面我们写一个基本的 ``Template`` 类（可以直接在 github 上下载 `template1b.py`_ ）:

.. code-block:: python

    class Template:

        def __init__(self, raw_text, indent=0, default_context=None,
                     func_name='__func_name', result_var='__result'):
            self.raw_text = raw_text
            self.default_context = default_context or {}
            self.func_name = func_name
            self.result_var = result_var
            self.code_builder = code_builder = CodeBuilder(indent=indent)
            self.buffered = []

            # 生成 def __func_name():
            code_builder.add_line('def {}():'.format(self.func_name))
            code_builder.forward()
            # 生成 __result = []
            code_builder.add_line('{} = []'.format(self.result_var))
            self._parse_text()

            self.flush_buffer()
            # 生成 return "".join(__result)
            code_builder.add_line('return "".join({})'.format(self.result_var))
            code_builder.backward()

        def _parse_text(self):
            pass

        def flush_buffer(self):
            # 生成类似代码: __result.extend(['<h1>', name, '</h1>'])
            line = '{0}.extend([{1}])'.format(
                self.result_var, ','.join(self.buffered)
            )
            self.code_builder.add_line(line)
            self.buffered = []

        def render(self, context=None):
            namespace = {}
            namespace.update(self.default_context)
            if context:
                namespace.update(context)
            exec(str(self.code_builder), namespace)
            result = namespace[self.func_name]()
            return result

以上就是 ``Template`` 类的核心方法了。我们之后要做的就是实现和完善 ``_parse_text`` 方法。
当模版字符串为空时生成的代码如下:

.. code-block:: python

    >>> import template1b
    >>> template = template1b.Template('')
    >>> template.code_builder
    def __func_name():
        __result = []
        __result.extend([])
        return "".join(__result)

可以看到跟上面[使用技术]那节所说生成的代码是类似的。下面我们就一起来实现这个 ``_parse_text`` 方法。


变量
---------

首先要实现是对变量的支持，模版语法是 ``{{ variable }}`` 。
既然要支持变量，首先要做的就是把变量从模版中找出来，这里我们可以使用正则表达式来实现:

.. code-block:: python

    re_variable = re.compile(r'\{\{ .*? \}\}')

    >>> re_variable = re.compile(r'\{\{ .*? \}\}')
    >>> re_variable.findall('<h1>{{ title }}</h1>')
    ['{{ title }}']
    >>>

知道了如何匹配变量语法，下面我们要把变量跟其他的模版字符串分割开来，这里还是用的 ``re``:

.. code-block:: python

    >> re_variable = re.compile(r'(\{\{ .*? \}\})')
    >>> re_variable.split('<h1>{{ title }}</h1>')
    ['<h1>', '{{ title }}', '</h1>']

这里的正则之所以加了个分组是因为我们同时还需要用到模版里的变量。
分割开来以后我们就可以对每一项进行解析了。支持 ``{{ variable }}`` 语法的 ``Template`` 类增加了如下代码
（可以直接在 github 上下载 `template1c.py`_ ）:

.. code-block:: python

    class Template:

        def __init__(self, raw_text, indent=0, default_context=None,
                     func_name='__func_name', result_var='__result'):
            # ...
            self.buffered = []

            self.re_variable = re.compile(r'\{\{ .*? \}\}')
            self.re_tokens = re.compile(r'(\{\{ .*? \}\})')

            # 生成 def __func_name():
            code_builder.add_line('def {}():'.format(self.func_name))
            # ...

        def _parse_text(self):
            tokens = self.re_tokens.split(self.raw_text)

            for token in tokens:
                if self.re_variable.match(token):
                    variable = token.strip('{} ')
                    self.buffered.append('str({})'.format(variable))
                else:
                    self.buffered.append('{}'.format(repr(token)))

``_parse_text`` 中之所以要用 ``repr`` ，是因为此时需要把 ``token`` 当成一个普通的字符串来处理，
同时需要考虑 ``token`` 中包含 ``"`` 和 ``'`` 的情况。
下面是几种有问题的写法:

* ``'str({})'.format(token)``: 这种是把 ``token`` 当成变量来用了，生成的代码为 ``str(token)``
* ``'"{}"'.format(token)``: 这种虽然是把 ``token`` 当成了字符串，但是会有转义的问题，当 ``token`` 中包含 ``"`` 时生成的代码为 ``""hello""``

下面先来看一下新的 ``template1c.py`` 生成了什么样的代码:

.. code-block:: python

    >>> from template1c import Template
    >>> template = Template('<h1>{{ title }}</h1>')
    >>> template.code_builder
    def __func_name():
        __result = []
        __result.extend(['<h1>',str(title),'</h1>'])
        return "".join(__result)

没问题，跟预期的是一样的。再来看一下 ``render`` 的效果:

.. code-block:: python

    >>> template.render({'title': 'Python'})
    '<h1>Python</h1>'

不知道你有没有发现，其实 ``{{ variable }}`` 不只支持变量，还支持表达式和运算符:

.. code-block:: python

    >>> Template('{{ 1 + 2 }}').render()
    '3'
    >>> Template('{{ items[0] }}').render({'items': [1, 2, 3]})
    '1'
    >>> Template('{{ func() }}').render({'func': list})
    '[]'


这个既可以说是个 BUG 也可以说是个特性😂， 看模版引擎是否打算支持这些功能了，
我们在这里是打算支持这些功能 ;)。

既然支持了 ``{{ }}`` 那么支持注释也就非常好实现了。


注释
-------

打算支持的注释模版语法是 ``{# comments #}`` ，有了上面实现 ``{{ variable }}``
的经验，实现注释是类似的代码
（可以直接在 github 上下载 `template1d.py`_ ）:

.. code-block:: python

    class Template:

        def __init__(self, raw_text, indent=0, default_context=None,
                     func_name='__func_name', result_var='__result'):
            # ...
            self.buffered = []

            self.re_variable = re.compile(r'\{\{ .*? \}\}')
            self.re_comment = re.compile(r'\{# .*? #\}')
            self.re_tokens = re.compile(r'''(
                (?:\{\{ .*? \}\})
                |(?:\{\# .*? \#\})
            )''', re.X)

            # 生成 def __func_name():
            # ...

        def _parse_text(self):
            tokens = self.re_tokens.split(self.raw_text)

            for token in tokens:
                if self.re_variable.match(token):
                    # ...
                # 注释 {# ... #}
                elif self.re_comment.match(token):
                    continue
                else:
                    # ...

效果:

.. code-block:: python

    >>> from template1d import Template
    >>> template = Template('<h1>{{ title }} {# comment #}</h1>')
    >>> template.code_builder
    def __func_name():
        __result = []
        __result.extend(['<h1>',str(title),' ','</h1>'])
        return "".join(__result)

    >>> template.render({'title': 'Python'})
    '<h1>Python </h1>'

至此，我们的模版引擎已经支持了变量和注释功能。
那么如何实现支持 ``if`` 语句和 ``for`` 循环的标签语法呢:

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


我将在 `第二篇文章`_ 中向你详细的讲解。敬请期待。


.. _template1a.py: https://github.com/mozillazg/lsbate/raw/master/part1/template1a.py
.. _template1b.py: https://github.com/mozillazg/lsbate/raw/master/part1/template1b.py
.. _template1c.py: https://github.com/mozillazg/lsbate/raw/master/part1/template1c.py
.. _template1d.py: https://github.com/mozillazg/lsbate/raw/master/part1/template1d.py
.. _第二篇文章: #
