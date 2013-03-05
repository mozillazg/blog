Title: 更改 phpMyAdmin 默认访问端口(apache2)
Date: 2013-02-27
Tags: phpmyadmin, mysql, ubuntu
Slug: change-phpmyadmin-default-visit-port

将访问 phpMyAdmin 的端口从默认的 80 改为 8081 。

本文的 phpmyadmin 目录：`/var/www/phpmyadmin/`

编辑 apache 配置文件：

    :::bash
    # vi /etc/apache2/sites-available/phpmyadmin

    <VirtualHost *:8081>
        ServerName 127.0.0.1
        DocumentRoot /var/www/phpmyadmin
    </VirtualHost>


配置 apache 监听 8081 端口：

    :::bash
    # vi /etc/apache2/ports.conf

    # 添加
    NameVirtualHost *:8081
    Listen 8081

重启 apache 服务：`service apache2 restart`，
现在可以通过 http://ip:8081/phpmyadmin/ 访问 phpMyAdmin 了。

## 参考

* [PHPMyAdmin Port Change - Ubuntu Forums](http://ubuntuforums.org/showthread.php?t=1329607)
