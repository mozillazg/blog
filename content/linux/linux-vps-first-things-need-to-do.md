Title: [linux]入手 VPS 后首先该做的事情
Date: 2013-01-10
Tags: linux, vps, ssh, iptables, ubuntu, centos
Slug: linux-vps-first-things-need-to-do


本文将介绍入手 VPS 后首先该做的一些事情。

本文推荐使用 Xshell 作为 Windows 下的 SSH 客户端。

## 更改 root 用户密码

使用 root 登录 ssh 后，

    :::console
    Xshell:\> ssh root@192.168.1.2

首先要做的事情就是更改 root 密码，密码记得要复杂点：

    :::console
    # passwd
    Enter new UNIX password: 
    Retype new UNIX password: 
    passwd: password updated successfully

修改完密码之后可以断开 ssh 重新使用 root 登录验证一下密码。

## 创建普通用户

为了安全，平时我们应该以普通用户的身份操作 VPS。所以需要创建一个普通用户。

    :::console
    # useradd -m hello
    # passwd hello
    Enter new UNIX password: 
    Retype new UNIX password: 
    passwd: password updated successfully

给用户添加 sudo 命令的使用权限：

    :::console
    # echo -e "\nhello ALL=(ALL) ALL\n" >> /etc/sudoers
    # tail -3 /etc/sudoers

    hello ALL=(ALL) ALL


如果不想每次使用 `sudo` 都输入 root 密码，上面的命令修改为：

    :::console
    # echo -e "\nhello ALL=(ALL) NOPASSWD:ALL\n" >> /etc/sudoers
    # tail -3 /etc/sudoers

    hello ALL=(ALL) NOPASSWD:ALL

## 使用 SSH 密匙认证登录 VPS

为了安全与方便，需要使用 SSH 密匙认证的方式来登录 VPS 。

首先切换到普通用户下，

    :::console
    # sudo su -l hello

如果出现 sudo: unable to resolve host xxx 错误:

1. 查看 hostname:

        :::console
        # head /etc/hostname
        ubuntu

2. 修改文件 /etc/hosts，增加一行内容 `127.0.0.1 hostname`:

        :::console
        # echo -e "\n127.0.0.1 ubuntu\n" >> /etc/hosts
        # tail -3 /etc/hosts

        127.0.0.1 ubuntu


生成密钥：

    :::console
    $ ssh-keygen

一路回车。

    :::console
    $ cd ~/.ssh 
    $ cat id_rsa.pub >> authorized_keys
    $ ls 
    authorized_keys  id_rsa  id_rsa.pub
    $ chmod 600 authorized_keys

id\_rsa 文件就是客户端用来登录的私钥了，下面我们要把他从服务器上下载下来。

点击 Xshell 导航栏的“new file transfer” 图标，进入一个终端界面后：

    :::console
    $ cd /home/hello/.ssh
    $ get id_rsa

此时 id\_rsa 文件已经在 Xshell 的安装目录下了。然后再配置 xshell 使用密钥登录即可。

## 禁用 root 登录及密码认证登录

为了安全起见，我们需要配置 SSH 从而达到禁用 root 登录及密码认证登录的目的。

在进行下面的配置前你需要再三确认可以通过上面生成的密钥以普通用户的身份登录 VPS，并且 root 密码正确无误的记下来了。

编辑 ssh 服务器端配置文件：

    :::console
    $ sudo vi /etc/ssh/sshd_config

将 26 行左右的 `PermitRootLogin yes` 改为 `PermitRootLogin no` ，       
50 行左右的 `#PasswordAuthentication yes` 改为 `PasswordAuthentication no`。

重启 ssh 服务：

    :::console
    $ sudo service sshd restart

## 配置防火墙

下面将使用 iptables 作为服务器的防火墙，如果服务器没有安装的话需要先安装 iptables。

    :::console
    $ sudo apt-get install iptables             # ubuntu
    $ yum install iptables                      # centos

对于 centos/redhat：

    :::console
    $ sudo vi /etc/sysconfig/iptables

    # Firewall configuration written by system-config-firewall
    # Manual customization of this file is not recommended.
    *filter
    :INPUT ACCEPT [0:0]
    :FORWARD ACCEPT [0:0]
    :OUTPUT ACCEPT [0:0]
    -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    -A INPUT -p icmp -j ACCEPT
    -A INPUT -i lo -j ACCEPT
    -A INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
    -A INPUT -j REJECT --reject-with icmp-host-prohibited
    -A FORWARD -j REJECT --reject-with icmp-host-prohibited
    -A INPUT -j DROP
    COMMIT

ubuntu：

    :::console
    $ sudo vi /etc/iptables.up.rules  # 添加上面的规则

    $ sudo vim /etc/network/interfaces 

在  'iface lo inet loopback' 后增加一行 pre-up iptables-restore < /etc/iptables.up.rules

应用防火墙规则：

    :::console
    $ sudo service iptables restart  # centos

    $ sudo iptables-restore < /etc/iptables.up.rules   # ubuntu

开机启动 iptables ：

    :::console
    $ sudo chkconfig iptables on  # redhat/centos
    
    $ sudo apt-get install sysv-rc-conf  # ubuntu
    $ sudo sysv-rc-conf iptables on    # ubuntu

## 参考

* [Linux : 大三学生的作品- 42qu.com](http://matrix.42qu.com/10728837)
* [Configuring IPtables on ubuntu server - LinodeWiki](http://www.linode.com/wiki/index.php/Configuring_IPtables_on_ubuntu_server)
* [Chapter 1. Preparing the System](http://docs.kolab.org/en-US/Kolab_Groupware/3.0/html/Community_Installation_Guide/chap-Community_Installation_Guide-Preparing_the_System.html#sect-Community_Installation_Guide-Preparing_the_System-System_Firewall)
