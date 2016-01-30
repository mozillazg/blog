titel: 解决 git push 时出现 error: pack-objects died of signal 13 的问题
slug: fix-git-push-raise-error-pack-objects-died-of-signal-13
date: 2016-01-29

今天执行 `git push` 的时候报了如下的错误：

    $ git push
    Warning: Permanently added 'ssh.github.com,192.30.252.149' (RSA) to the list of known hosts.
    对象计数中: 27, 完成.
    Delta compression using up to 4 threads.
    压缩对象中: 100% (26/26), 完成.
    Write failed: Broken pipe 3.20 MiB | 93.00 KiB/s
    写入对象中:  81% (22/27)fatal: , 3.83 MiB | 52.00 KiB/sThe remote end hung up unexpectedly
    error: pack-objects died of signal 13
    error: 无法推送一些引用到 'git@github.com:mozillazg/mozillazg.com.git'

最后的解决办法是加大 `http.postBuffer` 的值:

    $ git config http.postBuffer 52428800

`http.postBuffer` 的值的单位是字节， 52428800 = 1024 * 1024 * 50 即 50 M。


## 参考资料

* [git - Can&#39;t push to GitHub error: pack-objects died of signal 13 - Stack Overflow](http://stackoverflow.com/a/25846617/1804866)
* [site / master / issues / #7567 - git push remote end hung up &mdash; Bitbucket](https://bitbucket.org/site/master/issues/7567/git-push-remote-end-hung-up)