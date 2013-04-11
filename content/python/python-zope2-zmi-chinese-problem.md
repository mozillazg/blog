Title: [python]解决 zope2 后台编辑器中文编码问题
Date: 2013-03-15
Tags: python, zope2
Slug: python-zope2-zmi-chinese-problem

默认情况下 zope2 的后台编辑器不能正常显示中文：

    <title>&#24050;&#25552;&#20132;&#21464;&#26356;</title>

在 manage 后台稍作修改后就可以正常保存中文了：

    <title>已提交变更</title>

修改步骤：

> 在zope的根目录的propertyies页下面，增加如下特性：management_page_set: utf-8。

![alt][img1]

## 参考

* [如何改变Zope默认的编码？][3]
* [ZMI 中文 乱码问题解决][4]


[img1]: /static/images/2013-3-zope2-chinese-01.png
[3]: http://comments.gmane.org/gmane.comp.web.zope.chinese/541
[4]: http://315ok.org/blogs/zmizhongwenluanmawentijiejue
