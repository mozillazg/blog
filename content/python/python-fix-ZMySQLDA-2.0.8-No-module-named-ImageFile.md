Title: [python]修复 ZMySQLDA-2.0.8 出现的“ImportError: No module named ImageFile”
Date: 2013-03-08
Tags: python, zope, mysql
Slug: python-fix-zmysqlda-2.0.8-no-module-named-imagefile

修改 ZMySQLDA 文件夹内的 DA.py、DABase.py 文件，将

    :::python
    from ImageFile import ImageFile

改为

    :::python
    from App.ImageFile import ImageFile

即可。

    :::console
    [zope@localhost ZMySQLDA]$ cat DA.py | grep App.Image -n
    96:from App.ImageFile import ImageFile

    [zope@localhost ZMySQLDA]$ cat DABase.py | grep App.Image -n
    92:from App.ImageFile import ImageFile

## 参考

* [zope の version up で Products "COREBlog" "EPos" でエラー](http://rescue.unchor.com/4)
* [Installing ZMySQLDA in Zope using buildout on Ubuntu and perhaps Debian in general](http://mxm-mad-science.blogspot.com/2008/01/installing-zmysqlda-in-zope-using.html)
