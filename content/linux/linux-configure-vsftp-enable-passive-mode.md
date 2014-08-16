Title: [linux]配置 vsftp 启用被动模式（passive mode）解决客户端"no route to host"错误
Date: 2014-05-20
Tags: linux, vsftp
Slug: linux-configure-vsftp-enable-passive-mode

系统: CentOS


* 修改 vsftpd.conf，启用被动模式，指定端口:

        pasv_min_port=12000
        pasv_max_port=12199
        pasv_enable=YES


* 配置防火墙 iptables，允许端口访问:

        iptables -I INPUT -p tcp --dport 12000:12199 -j ACCEPT
        service iptables save


## 参考资料

* [centos - How to configure vsftpd to work with passive mode - Server Fault ](http://serverfault.com/questions/421161/how-to-configure-vsftpd-to-work-with-passive-mode)
* [How to check the Passive and Active FTP - Unix & Linux Stack Exchange ](http://unix.stackexchange.com/questions/58291/how-to-check-the-passive-and-active-ftp)
