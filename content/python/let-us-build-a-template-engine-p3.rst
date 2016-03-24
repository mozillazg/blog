让我们一起来构建一个模版引擎（三）
====================================
:date: 2016-03-24
:slug: let-us-build-a-template-engine-part3
:tags: lsbate, 让我们一起来构建一个模版引擎

在 `上篇文章`_ 中我们的模版引擎实现了对 ``if`` 和 ``for`` 对支持，同时在文章的最后我给大家留了一个
问题：如何实现支持 ``include`` 和 ``extends`` 的标签功能。

在本篇文章中我们将一起来动手实现这两个功能。

include
-----------

``include`` 标签对语法是这样的：假设有一个 item.html 模版文件，它的内容如下:

.. code-block:: htmldjango

    <li>{{ item }}</li>

还有一个我们要渲染的模版 list.html 内容如下:

.. code-block:: htmldjango

    <ul>
      {% for item in items %}
        {% include "item.html" %}
      {% endfor %}
    </ul>

渲染 list.html 后的结果类似:

.. code-block:: htmldjango

    <ul>
      <li>item1</li>
      <li>item2</li>
      <li>item3</li>
    </ul>

从上面可以看出来 ``include`` 标签的作用类似使用 ``include`` 所在位置的名字空间
渲染另一个模版然后再使用渲染后的结果。所以我们可以将 ``include`` 的模版文件
当作普通的模版文件来处理，用解析那个模版生成后的代码替换 ``include`` 所在的位置，
再将结果追加到 ``result_var`` 。 生成的代码类似:

.. code-block:: python

    def func_name():
        result = []

        # 解析 include 的模版
        def func_name_include():
            result_include = []
            return ''.join(result_include)
        # 调用生成的 func_name_include 函数获取渲染结果
        result.append(func_name_include())

        return ''.join(result)

生成类似上面的代码就是 ``include`` 的关键点，下面看一下实现 ``include`` 功能
都做了哪些改动 (可以从 Github 上下载 `template3a.py`_):

.. code-block:: python

    class Template:

        def __init__(self, ..., template_dir='', encoding='utf-8'):
            # ...
            self.template_dir = template_dir
            self.encoding = encoding
            # ...

        def _handle_tag(self, token):
            """处理标签"""
            # ...
            tag_name = tag.split()[0]
            if tag_name == 'include':
                self._handle_include(tag)
            else:
                self._handle_statement(tag)

        def _handle_include(self, tag):
            filename = tag.split()[1].strip('"\'')
            included_template = self._parse_another_template_file(filename)
            # 把解析 include 模版后得到的代码加入当前代码中
            # def __func_name():
            #    __result = []
            #    ...
            #    def __func_name_hash():
            #        __result_hash = []
            #        return ''.join(__result_hash)
            self.code_builder.add(included_template.code_builder)
            # 把上面生成的代码中函数的执行结果添加到原有的结果中
            # __result.append(__func_name_hash())
            self.code_builder.add_line(
                '{0}.append({1}())'.format(
                    self.result_var, included_template.func_name
                )
            )

        def _parse_another_template_file(self, filename):
            template_path = os.path.realpath(
                os.path.join(self.template_dir, filename)
            )
            name_suffix = str(hash(template_path)).replace('-', '_')
            func_name = '{}_{}'.format(self.func_name, name_suffix)
            result_var = '{}_{}'.format(self.result_var, name_suffix)
            with open(template_path, encoding=self.encoding) as fp:
                template = self.__class__(
                    fp.read(), indent=self.code_builder.indent,
                    default_context=self.default_context,
                    func_name=func_name, result_var=result_var,
                    template_dir=self.template_dir
                )
            return template

首先是 ``__init__`` 增加了两个参数 ``template_dir`` 和 ``encoding``:

* ``template_dir``: 指定模版文件夹路径，因为 ``include`` 的模版是相对路径所以需要这个
  选项来获取模版的绝对路径
* ``encoding``: 指定模版文件的编码，默认是 ``utf-8``

然后就是 ``_parse_another_template_file`` 了，这个方法是用来解析 ``include`` 中
指定的模版文件的，其中的 ``func_name`` 和 ``result_var`` 之所以加了个 hash 值
作为后缀是不想跟其他函数变量重名。

``_handle_include`` 实现的是解析 include 的模版，
然后将生成的代码和代码中函数的执行结果添加到当前代码中。

下面来看一下实现的效果。还是用上面的模版文件:

item.html:

.. code-block:: htmldjango

    <li>{{ item }}</li>

list.html:

.. code-block:: htmldjango

    <ul>
      {% for item in items %}
        {% include "item.html" %}
      {% endfor %}
    </ul>


先来看一下生成的代码:

.. code-block:: python

    >>> from template3a import Template
    >>> text = open('list.html').read()
    >>> t = Template(text)
    >>> t.code_builder
    def __func_name():
        __result = []
        __result.extend(['<ul>\n  '])
        for item in items:
            __result.extend(['\n    '])
            def __func_name_7654650009897399020():
                __result_7654650009897399020 = []
                __result_7654650009897399020.extend(['<li>',str(item),'</li>\n'])
                return "".join(__result_7654650009897399020)
            __result.append(__func_name_7654650009897399020())
            __result.extend(['\n  '])
        __result.extend(['\n</ul>\n'])
        return "".join(__result)

然后是渲染效果:

.. code-block:: python

    >>> print(t.render({'items': ['item1', 'item2', 'item3']}))
    <ul>

        <li>item1</li>


        <li>item2</li>


        <li>item3</li>


    </ul>

``include`` 已经实现了，下面让我们一起来实现 ``extends`` 功能。

extends
-------------

``extends`` 标签实现的是模版继承的功能，并且只能在第一行出现，语法如下:

假设有一个 parent.html 文件它的内容是:

.. code-block:: htmldjango

    <div id="header">{% block header %} parent_header {% endblock header %}</div>
    <div id="footer">{% block footer %} parent_footer {% endblock footer %}</div>

还有一个 child.html 文件:

.. code-block:: htmldjango

    {% extends "parent.html" %}
    {% block header %} child_header {{ block.super }} {% endblock header %}

child.html 渲染后的结果:

.. code-block:: html

    <div id="header"> child_header parent_header </div>
    <div id="footer"> parent_footer </div>

可以看到 ``extends`` 的效果类似用子模版里的 ``block`` 替换父模版中定义的同名 ``block``,
同时又可以使用 ``{{ block.super }}`` 引用父模版中定义的内容，有点类似 ``class`` 的继承效果。

注意我刚才说的是: 类似用子模版里的 ``block`` 替换父模版中定义的同名 ``block`` 。

这个就是 ``extends`` 的关键点，我们可以先找出子模版里定义的 ``block`` ，
然后用子模版里的 ``block`` 替换父模版里的同名 ``block`` ,
最后只处理替换后的父模版就可以了。

暂时先不管 ``block.super`` ，支持 ``extends`` 的代码改动如下(可以从 Github 下载 `template3b.py`_ ):

.. code-block:: python

    class Template:
        def __init__(self, ...):
            # extends
            self.re_extends = re.compile(r'\{% extends (?P<name>.*?) %\}')
            # blocks
            self.re_blocks = re.compile(
                r'\{% block (?P<name>\w+) %\}'
                r'(?P<code>.*?)'
                r'\{% endblock \1 %\}', re.DOTALL)

        def _parse_text(self):
            # extends
            self._handle_extends()

            tokens = self.re_tokens.split(self.raw_text)
            # ...

        def _handle_extends(self):
            match_extends = self.re_extends.match(self.raw_text)
            if match_extends is None:
                return

            parent_template_name = match_extends.group('name').strip('"\' ')
            parent_template_path = os.path.join(
                self.template_dir, parent_template_name
            )
            # 获取当前模版里的所有 blocks
            child_blocks = self._get_all_blocks(self.raw_text)
            # 用这些 blocks 替换掉父模版里的同名 blocks
            with open(parent_template_path, encoding=self.encoding) as fp:
                parent_text = fp.read()
            new_parent_text = self._replace_parent_blocks(
                parent_text, child_blocks
            )
            # 改为解析替换后的父模版内容
            self.raw_text = new_parent_text

        def _replace_parent_blocks(self, parent_text, child_blocks):
            """用子模版的 blocks 替换掉父模版里的同名 blocks"""
            def replace(match):
                name = match.group('name')
                parent_code = match.group('code')
                child_code = child_blocks.get(name)
                return child_code or parent_code
            return self.re_blocks.sub(replace, parent_text)

        def _get_all_blocks(self, text):
            """获取模版内定义的 blocks"""
            return {
                name: code
                for name, code in self.re_blocks.findall(text)
            }

从上面的代码可以看出来我们遵循的是使用子模版 ``block`` 替换父模版同名 ``block``
然后改为解析替换后的父模版的思路. 即，虽然我们要渲染的是:

.. code-block:: htmldjango

    {% extends "parent.html" %}
    {% block header %} child_header {% endblock header %}

实际上我们最终渲染的是替换后的父模版:

.. code-block:: htmldjango

    <div id="header"> child_header </div>
    <div id="footer"> parent_footer </div>

依旧是来看一下实际效果:

parent1.html:

.. code-block:: htmldjango

    <div id="header">{% block header %} parent_header {% endblock header %}</div>
    <div id="footer">{% block footer %} parent_footer {% endblock footer %}</div>

child1.html:

.. code-block:: htmldjango

    {% extends "parent1.html" %}
    {% block header %} {{ header }} {% endblock header %}

看看最后要渲染的模版字符串:

.. code-block:: python

    >>> from template3b import Template
    >>> text = open('child1.html').read()
    >>> t = Template(text)
    >>> print(t.raw_text)
    <div id="header"> {{ header }} </div>
    <div id="footer"> parent_footer </div>

可以看到确实是替换后的内容，再来看一下生成的代码和渲染后的效果:

.. code-block:: python

    >>> t.code_builder
    def __func_name():
        __result = []
        __result.extend(['<div id="header"> ',str(header),' </div>\n<div id="footer"> parent_footer </div>\n'])
        return "".join(__result)

    >>> print(t.render({'header': 'child_header'}))
    <div id="header"> child_header </div>
    <div id="footer"> parent_footer </div>

``extends`` 的基本功能就这样实现了。下面再实现一下 ``{{ block.super }}`` 功能。

block.super
------------

``{{ block.super }}`` 类似 Python ``class`` 里的 ``super`` 用来实现对父 ``block``
的引用，让子模版可以重用父 ``block`` 中定义的内容。
只要改一下 ``_replace_parent_blocks`` 中的 ``replace`` 函数让它支持 ``{{ block.super }}``
就可以了(可以从 Github 下载 `template3c.py`_):

.. code-block:: python

    class Template:
        def __init__(self, ....):
            # blocks
            self.re_blocks = ...
            # block.super
            self.re_block_super = re.compile(r'\{\{ block\.super \}\}')

        def _replace_parent_blocks(self, parent_text, child_blocks):
            def replace(match):
                ...
                parent_code = match.group('code')
                child_code = child_blocks.get(name, '')
                child_code = self.re_block_super.sub(parent_code, child_code)
                new_code = child_code or parent_code
                return new_code

效果:

parent2.html:

.. code-block:: htmldjango

    <div id="header">{% block header %} parent_header {% endblock header %}</div>

child2.html:

.. code-block:: htmldjango

    {% extends "parent2.html" %}
    {% block header %} child_header {{ block.super }} {% endblock header %}


.. code-block:: python

    >>> from template3c import Template
    >>> text = open('child2.html').read()
    >>> t = Template(text)
    >>> t.raw_text
    '<div id="header"> child_header  parent_header  </div>\n'

    >>> t.render()
    '<div id="header"> child_header  parent_header  </div>\n'


到目前为主我们已经实现了现代 python 模版引擎应有到大部分功能了， 之后就是完善了。

不知道大家有没有注意到，我之前都是用生成 html 来试验模版引擎的功能的，
这是因为模版引擎确实是在 web 开发中用的比较多，既然是生成 html 源码那就需要考虑
针对 html 做一点优化，比如去掉多余的空格，转义之类的，还有就是一些 Web 安全方面的考虑。

至于怎么实现这些优化项，我将在 `第四篇文章`_ 中向你详细的讲解。敬请期待。


.. _template3a.py: https://github.com/mozillazg/lsbate/raw/master/part3/template3a.py
.. _template3b.py: https://github.com/mozillazg/lsbate/raw/master/part3/template3b.py
.. _template3c.py: https://github.com/mozillazg/lsbate/raw/master/part3/template3c.py
.. _template3d.py: https://github.com/mozillazg/lsbate/raw/master/part3/template3d.py
.. _第四篇文章: #
.. _上篇文章: https://mozillazg.com/2016/03/let-us-build-a-template-engine-part2.html
