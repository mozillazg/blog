Title: [linux]解决 screen 中不能使用退格键的问题
Date: 2013-05-21
Tags: linux, screen, backspace
Slug: linux-screen-can-not-use-backspace-key
status: draft

screen 中不能使用退格键，ctrl+h 也不行，会把整行删除，而不是退格键该有的功能。

编辑 /etc/screenrc 或 ~/.screenrc 添加一句：

    bind ^h


## 参考

*[Bug #29787-Backspace key in GNU Screen not detected correctly](https://bugs.launchpad.net/ubuntu/+source/vte/+bug/29787)
