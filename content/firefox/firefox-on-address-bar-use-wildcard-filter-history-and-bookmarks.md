Title: [firefox]在地址栏使用通配符过滤书签及历史记录
Date: 2013-01-18
Tags: firefox
Slug: firefox-on-address-bar-use-wildcard-filter-history-and-bookmarks

通过在地址栏使用相应的通配符从而实现只搜索书签或历史记录的功能。

打开 [about:config](about:config) 搜索 `urlbar` ：

![about:config urlbar](/static/images/2013-1-19-firefox-about-config-urlbar.png)

从上图可以看出，默认情况下相关通配符的功能如下：

    :::text
    browser.urlbar.match.title            #      只匹配标题
    browser.urlbar.match.url              @      只匹配 URL
    browser.urlbar.restrict.bookmark      *      只搜索书签
    browser.urlbar.restrict.history       ^      只搜索历史记录
    browser.urlbar.restrict.openpage      %      只搜索所有打开的标签页
    browser.urlbar.restrict.tag           +      只搜索标签
    browser.urlbar.restrict.typed         ~      只搜索曾经在地址栏输入过的记录（URL + 标题）

例如，只搜索标题包含 firefox 的记录：

    :::text
    # firefox

可以组合使用，不同字符间要加空格。比如，只搜索所有书签中 URL 包含 firefox 的记录：

    :::text
    * @ firefox

最后就是，上面的字符都可以自定义，可以怎么方便怎么来。

## 参考

* [Location Bar search - MozillaZine Knowledge Base](http://kb.mozillazine.org/Browser.urlbar.match.url)
