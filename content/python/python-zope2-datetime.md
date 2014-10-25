Title: [python]在 zope2 中获取当前时间及格式化输出
Date: 2013-03-18
Tags: python, zope2
Slug: python-zope2-datetime


可以使用 Zope2 内置的 `DateTime()` 获取当前时间。

## Script(Python)

新建 Script(Python) 文件：

    return DateTime()
结果：

    2013/03/18 12:38:22.825950 GMT-4
格式输出：

return DateTime().strftime('%Y-%m-%d %H:%M:%S')
结果：

    2013/03/18 12:38

## DTML

新建 DTML 文件：

    <dtml-var expr="DateTime()" fmt="%Y/%m/%d %H:%M">

结果：

    2013/03/18 12:40

## 参考
* [ZopeBook Appendix B: API Reference](http://www.faqs.org/docs/ZopeBook/AppendixB.html)
