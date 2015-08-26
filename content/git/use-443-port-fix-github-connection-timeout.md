Title: 改用 443 端口连接 Github 修复 git push 时出现 Connection timed out 的问题
Slug: use-443-port-fix-github-connection-timeout
Date: 2015-08-25
Tags: github

最近几天我这里出现了 `git push` 出现 timeout 的问题：

    $ git push
    ssh: connect to host github.com port 22: Connection timed out
    fatal: Could not read from remote repository.

    Please make sure you have the correct access rights
    and the repository exists.

不想改用 https 协议，因为 https 每次都要询问用户名，密码太烦了。最后找到了一个使用 443 端口连接 github 的方法：

修改 ~/.ssh/config 中 github.com 的配置，
`Hostname` 改为 `ssh.github.com`, `Port` 改为
`443`:

    Host github.com
      Hostname ssh.github.com
      Port 443

测试：

    $ ssh -T git@github.com
    Warning: Permanently added '[ssh.github.com]:443,[192.30.252.148]:443' (RSA) to the list of known hosts.
    Hi mozillazg! You've successfully authenticated, but GitHub does not provide shell access.

    $ git push
    Warning: Permanently added '[ssh.github.com]:443,[192.30.252.151]:443' (RSA) to the list of known hosts.


## 参考资料

* [Using SSH over the HTTPS port - User Documentation](https://help.github.com/articles/using-ssh-over-the-https-port/)