Title: [linux]修复 GPG key retrieval failed: [Errno 14] Could not open/read file:///etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag
Date: 2013-08-02
Tags: linux, rpmforge
Slug: linux-gpg-key-retrieval-failed-errno-14

两种方法：

* 编辑 `/etc/yum/etc/yum.repos.d/rpmforge.repo`，更改 `gpgcheck=0`

* `rpm --import http://apt.sw.be/RPM-GPG-KEY.dag.txt`


## 参考

* [GPG key retrieval failed](http://easylinuxalways.blogspot.jp/2013/04/gpg-key-retrieval-failed.html)
