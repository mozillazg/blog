[linux]bash 下 ; && || 的区别
#############################

:date: 2013-09-28
:tags: linux, bash, shell
:slug: linux-bash-run-mutil-cmd

linux 中 bash 下执行多个命令时，; && || 操作符的区别：

+--------------+-------------------------------------+
| cmd1 ; cmd2  | cmd1 和 cmd2 **都会** 被执行        |
+--------------+-------------------------------------+
| cmd1 && cmd2 | 如果 cmd1 执行 **成功** 则执行 cmd2 |
+--------------+-------------------------------------+
| cmd1 || cmd2 | 如果 cmd1 执行 **失败** 则执行 cmd2 |
+--------------+-------------------------------------+


参考
----

* `linux - what is the difference between "command && command" and "command ; command" - Super User <http://superuser.com/questions/619016/what-is-the-difference-between-command-command-and-command-command>`__
