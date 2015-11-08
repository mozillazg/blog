Title: 解决通过 ifttt 把 Feed 中的图片转发到 twritter 时，总是出现 "image not found" 的问题
Date: 2015-05-01
Modified: 2015-08-27
Slug: fix-ifttt-feed-image-not-found


之前使用 ifttt 把 Feed 中的图片转发到 twritter 时，总是出现 "image not found"。然后就不再使用 ifttt 转发图片了。

![image not found](/static/images/ifttt-image-not-found.png)

趁着今天给 [comic.mozillazg.com](http://comic.mozillazg.com) 增加 Atom Feed 的功能的时候，研究了一下 ifttt 获取图片的规则。通过搜索后得知，ifttt 只会从文章内容的开头位置获取图片地址，如果获取不到的话，就 "image not found":


    <!-- bad: "image not found"  -->
    <content type="html">
        <p>译自：http://explosm.net/comics/3908/<br /> AT 2015-05-01 </p>
        <img src="http://tmp-images.qiniudn.com/comics/3908.you-should.zh-cn.png" alt="Cyanide & Happiness #3908：你应该" />
    </content>
    
    <!-- good -->
    <content type="html">
        <img src="http://tmp-images.qiniudn.com/comics/3908.you-should.zh-cn.png" alt="Cyanide & Happiness #3908：你应该" />
        <p>译自：http://explosm.net/comics/3908/<br /> AT 2015-05-01 </p>
    </content>


## 参考

* [https://twitter.com/ifttt/status/372166382172925952](https://twitter.com/ifttt/status/372166382172925952)
* [How To Include Your WordPress Post’s Featured Image in a RSS Feed Excerpt]( Excerpthttps://winwar.co.uk/2015/02/include-wordpress-posts-featured-image-rss-feed-excerpt/)
