Title: [linux]常用的 CentOS 5/6/7 yum 源
Date: 2014-11-23
Slug: linux-recommended-centos-5-6-7-yum-source

下面是一些常用的 CentOS yum 源。

## rpmforge

    # centos 5 i386
    rpm -Uvh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el5.rf.i386.rpm
    # centos 5 x86_64
    rpm -Uvh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el5.rf.x86_64.rpm
    
    # centos 6 i686
    rpm -Uvh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.i686.
    # centos 6 x86_64
    rpm -Uvh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm
    
    # centos 7
    rpm -Uvh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm

## epel

    # centos 5 i386
    rpm -Uvh http://download.fedoraproject.org/pub/epel/5/i386/epel-release-5-2.noarch.rpm
    # centos 5 x86_64
    rpm -Uvh http://download.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-2.noarch.rpm
    
    # centos 6 i386
    rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-2.noarch.rpm
    # centos 6 x86_64
    rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-2.noarch.rpm
    
    # centos 7
    rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-2.noarch.rpm

## remi

    # centos 5
    rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-5.rpm
    # centos 6
    rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
    # centos 7
    rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
`vim /etc/yum.repos.d/remi.repo` 更改 `enable=1`