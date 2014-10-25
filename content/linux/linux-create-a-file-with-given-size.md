Title: [linux]创建指定大小的文件
Date: 2013-08-03
Tags: linux
Slug: linux-create-a-file-with-given-size

比如创建 10M 大小的文件：

    :::shell
    # 创建大小为 10M 的文件：abc.exe
    dd if=/dev/zero of=abc.exe bs=1M count=10

    # 只生成属性为 10M 大小的文件，但不占用实际硬盘空间
    dd if=/dev/zero of=abc.exe bs=1M seek=10 count=0


## 参考

* [Linux生成指定大小文件的方法](http://rubyer.me/blog/196/)
