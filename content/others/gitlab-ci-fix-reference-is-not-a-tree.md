title: 解决 gitlab 配置不正确导致 ci 中 git clone 时出现 “You appear to have cloned an empty repository” 的问题
slug: gitlab-ci-fix-reference-is-not-a-tree-you-appear-to-have-cloned-an-empty
date: 2015-11-02
tags: gitlab, gitlab-git-http-server

最近在使用 gitlab 的 ci 服务时出现了如下问题：

    gitlab-ci-multi-runner ...
    ...

    Cloning repository... 
    Cloning into '/builds/...'... 
    warning: You appear to have cloned an empty repository. 
    Checking out 2c80f515 as develop... 
    fatal: reference is not a tree: 1b53f5157b357f4c006ceccf0e36035bad340185

经过多翻搜索验证后发现是 gitlab-git-http-server 的配置问题：
这个 gitlab 服务没有使用内置的 nginx 来反向代理 gitlab 服务而是使用的 yum 安装的 nginx。
由于配置有问题导致 ci 任务一直失败。

解决办法如下：

1. 修改 `/etc/gitlab/gitlab.rb`, 找到如下配置并修改为：
    
        nginx['enabled'] = false
        gitlab_git_http_server['listen_network'] = "tcp"
        # 这个端口修改为你实际需要的端口
        gitlab_git_http_server['listen_addr'] = "localhost:8081"
    
2. 应用更改 `sudo gitlab-ctl reconfigure`
3. 下载官方 nginx 配置（选择相应版本分支下的文件）:
    
        wget https://gitlab.com/gitlab-org/gitlab-ce/raw/v8.1.2/lib/support/nginx/gitlab -O /etc/nginx/conf.d/gitlab.conf
        # 如果你的 ci 服务器使用的是独立的域名或者使用了 ssl 的话，可以去
        # https://gitlab.com/gitlab-org/gitlab-ce/tree/master/lib/support/nginx
        # 下载相应的配置文件
    
4. 修改 nginx 配置文件中的 `upstream`， `server_name`, `root`，提示：
   如果不存在 `/home/git/gitlab/public` 目录的话，那么 `root` 就是
   `/opt/gitlab/embedded/service/gitlab-rails/public`
5. reload nginx: `nginx -t && nginx -s reload`


## 参考资料

* <https://gitlab.com/gitlab-org/gitlab-ce/issues/2727>
* <https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/nginx.md#gitlab>
* <https://gitlab.com/gitlab-org/gitlab-ce/tree/master/lib/support/nginx>
