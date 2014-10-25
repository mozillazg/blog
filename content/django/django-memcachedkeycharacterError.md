Title: [django]修复 MemcachedKeyCharacterError
Date: 2013-07-09
Tags: django, memcached
Slug: django-memcachedkeycharactererror


## 错误详情

> MemcachedKeyCharacterError at /
> 
> Control characters not allowed
>

出现这个错误是因为 key 值不合法：长度大于 250、包含空格或控制符


## 解决

去掉非法字符或将 key 进行编码(base64/md5/sha1/...)


## 参考

* [php - Can memcached keys contain spaces? - Stack Overflow](http://stackoverflow.com/a/11322746)
