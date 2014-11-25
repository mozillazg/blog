Title: [python]如何复制一个 class
Date: 2014-11-20
Tags: 
Slug: python-copy-a-class

通过下面两种方法可以复制一个 `class`:

* `class B(A): pass`
* `B = type("B", (A,), {})`


参考资料
========

* [How to copy a python class? - Stack Overflow](http://stackoverflow.com/questions/9541025/how-to-copy-a-python-class)