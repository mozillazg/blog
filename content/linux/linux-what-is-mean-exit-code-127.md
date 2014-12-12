Title: [linux]退出码 127 含义
Date: 2014-12-11
Slug:linux-what-is-mean-exit-code-127

在 bash 下退出码 `127` 的含义是 **命令不存在** :

    $ foo
    未找到 'foo' 命令，您要输入的是否是：
     命令 'fog' 来自于包 'ruby-fog' (universe)
     命令 'fox' 来自于包 'objcryst-fox' (universe)
     命令 'xoo' 来自于包 'xoo' (universe)
     命令 'fgo' 来自于包 'fgo' (universe)
     命令 'fio' 来自于包 'fio' (universe)
     命令 'fop' 来自于包 'fop' (main)
     命令 'goo' 来自于包 'goo' (universe)
     命令 'zoo' 来自于包 'zoo' (universe)
    foo：未找到命令
    $ echo $?
    127