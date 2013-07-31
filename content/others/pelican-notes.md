Title: pelican 使用笔记
Date: 2013-03-04
Tags: pelican, markdown, pygments, python-markdown
Slug: pelican-notes

记录一些使用 Pelican 写博客的经验。

##Markdown

### 多级列表

官方的 Markdown 语法：

    :::text
    * list
      * sublist
      * sublist
    * list

pelican 使用的是 python-markdown 来解析 markdown 文件，
而 python-markdown 的关于多级列表的语法跟官方的有点不一样：

    :::text
    * list
        * sublist
        * sublist
    * list

子列表与父列表之间的对齐方式是：至少空出4个空格或1一个 Tab 键。
官方的语法兼容 python-markdown 的语法，所以不要担心兼容性。

### 语法高亮

python-markdown 使用 pygments 来实现语法高亮的功能，并且支持指定编程语言。

比如，指定代码用的是 Python 编程语言：

    :::text
    :::python
    print 'hello, world'

效果：

    :::python
    print 'hello, world'

我用的比较多的语言标记：

* :::text
* :::python
* :::django
* :::html+django
* :::bash
* :::console
* :::nginx
* :::apacheconf

更多的语言标记，可以通过查看网站 [Pygments — Python syntax highlighter][1] 的源代码操作相关的语言标记（查看 id 为 flt_lang 的 select 的 option 值）。


**注意**：该语法不兼容官方 markdown 语法。


[1]: http://pygments.org/demo/


## 参考

* [Pelican — Pelican documentation](http://docs.getpelican.com/)
* [CodeHilite Extension — Python Markdown](http://pythonhosted.org/Markdown/extensions/code_hilite.html)
