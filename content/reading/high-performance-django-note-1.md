title: 《High Performance Django》阅读笔记
slug: high-performance-django-note-1
tags: High Performance Django, Django

[](![]())


一句话点评：老司机的经验之谈，物有所值。


## 第一章：The Big Picture

作者开篇就提到大家总说 Django 性能不行，但是实际上
有很多高性能的站点是使用 Django 开发的。

> Django’s scaling success stories are almost too numerous to list at this point. It backs Disqus,
> Instagram, and Pinterest. Want some more proof? Instagram was able to sustain over 30
> million users on Django with only 3 engineers (2 of which had no back-end development
> experience). Disqus serves over 8 billion page views per month. Those are some huge
> numbers. These teams have proven Django most certainly does scale. Our experience here
> at Lincoln Loop backs it up. We’ve built big Django sites capable of spending the day on
> the Reddit homepage without breaking a sweat.

在作者的公司，他们开发高性能 Django 站点的准则就是 **simplicity** :

* Using as few moving parts as possible to make it all work. “Moving parts” may be
servers, services or third-party software.
* Choosing proven and dependable moving parts instead of the new hotness.
* Using a proven and dependable architecture instead of blazing your own trail.
* Deflecting traffic away from complex parts and toward fast, scalable, and simple parts（

> Simple systems are easier to scale, easier to understand, and easier to develop. 

构建高性能 Web 应用通常需要关注一下几点：

* 数据库。关系型数据库通常是整个技术栈中最慢最复杂的部分，一个办法是改用 NoSQL 数据库，不过
  大多数情况下都可以通过缓存解决。
* 模板。我们可以用一个更快的模板引擎替换 Django 自带的模板引擎，不过即便是这样模板仍旧是
  整个技术栈中第二慢的部分。我们仍然可以通过缓存解决这个问题。
* Python。Python 在通常情况下已经足够快了。我们可以使用 Web 加速器（比如：Varnish）缓存服务器响应，
  在请求进入到 Python 那一层之前就返回相应。

这章作者一直在强调缓存，"CACHE ALL THE THINGS"。无论你怎么优化你的技术栈，没有比缓存更快的优化方案。
说到缓存可能大家可能会顾虑缓存过期的问题，作者说了现在先别关心这个问题，之后会给出解决方案。

作者提到一般的网站都保护这几层：负载均衡器，Web 加速器，APP 服务器，缓存，数据库


* 负载均衡器
  * 