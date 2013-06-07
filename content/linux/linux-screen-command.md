Title: [linux]screen 常用命令
Date: 2013-05-16
Tags: linux, screen
Slug: linux-screen-command

通过 screen 命令可以让终端命令在我们断开远程服务器后依旧运行而不会中断。

## 安装 screen 命令

redhat/centos:

    ::bash
    yum install screen
ubuntu:

    ::bash
    sudo apt-get install screen

## 常用的 screen 命令

新建一个名为 django 的 screen shell：

    ::bash
    screen -S django

新建一个名为 django 的后台 screen shell：

    ::bash
    screen -dS django

查看所有的 screen shell:

    ::bash
    $ screen -ls
    There are screens on:
        1429.django	(Detached)
        23264.abc	(Detached)
    2 Sockets in /var/run/screen/S-abc.

打开后台状态为 Detached 且名称为 django 的 screen shell:

    ::bash
    $ screen -r django

将当前 screen shell 转到后台（Detached），按快捷键: `Ctrl + a + d`

打开后台状态为 Attached 且名称为 django 的 screen shell:

    ::bash
    $ screen -r django
    There is a screen on:
        1429.django	(Attached)
    There is no screen to be resumed matching django.
    $ screen -x django
