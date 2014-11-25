Title: [linux]修复执行 make 命令时，提示：warning: Clock skew detected，导致无法执行 make 命令的问题
Date: 2014-11-20
Tags: 
Slug: linux-fix-make-warning-Clock-skew-detected

有时，执行 `make` 命令时会出现如下提示：

    make: warning: Clock skew detected. Your build may be incomplete.

导致无法执行 `make` 命令。

出现这个提示的原因是因为 Makefile 的修改时间大于系统的当前时间。
比如把本机的 Makefile 文件上传到服务器上时，而服务器上的时间比本机时间要慢，就会出现这种情况。

有两种解决办法：

* 同步本地时间和服务器时间。
* 在服务器上通过 touch 命令修改 Makefile 文件的修改时间。


参考资料
========

* [Compling C++ on remote Linux machine - "clock skew detected" warning - Stack Overflow](http://stackoverflow.com/questions/3824500/compling-c-on-remote-linux-machine-clock-skew-detected-warning)