Title: [django]修复 bad character range 异常
Date: 2013-02-26
Tags: python, django
Slug: django-bad-character-range


出现 bad character range 异常， 是因为程序某个地方的正则表达式写错了，
不是一个有效的正则表达式。


比如正则 `[_-\d]` 就是一个无效的正则，会报 `bad character range` 异常。
将正则修改为 `[-_\d]` 使之成为一个有效的正则，就可以修复该异常。


## 参考

* [django - "bad character range" exception? - Stack Overflow](http://stackoverflow.com/questions/1526137/bad-character-range-exception)
