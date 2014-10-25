Title: [git]显示单个文件变更日志
Date: 2013-08-17
Tags: git
Slug: git-show-file-changelog

`git log -p filename`:

    :::console
    $ git log -p fabfile.py
    commit fd792030bc0ac1db0f1f97ec701a2fd8bcb26a07
    Author: username <email>
    Date:   Sun Jun 23 15:36:58 2013 +0800

        commit title

    diff --git a/fabfile.py b/fabfile.py
    index 4ed36fa..1408118 100644
    --- a/fabfile.py
    +++ b/fabfile.py
    @@ -9,28 +9,29 @@ from fabric.api import settings

     @task
     def make_html():
    -    """生成 html 文件"""
    -    local('pelican content -o output -s pelicanconf.py')
    +    """generate the web site"""
    +    with settings(warn_only=True):
    +        local('pelican content -o output -s pelicanconf.py -D')


`git log filename`:

    :::console
    $ git log fabfile.py
    commit fd792030bc0ac1db0f1f97ec701a2fd8bcb26a07
    Author: username <email>
    Date:   Sun Jun 23 15:36:58 2013 +0800

        commit title


    $ git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit fabfile.py
    * fd79203 - commit title (8 weeks ago) <username>
    * 7642a05 - commit title (10 weeks ago) <username>
    * d04ba24 - commit title (10 weeks ago) <username>


## 参考

* [git log - View the change history of a file using Git versioning - Stack Overflow](http://stackoverflow.com/questions/278192/view-the-change-history-of-a-file-using-git-versioning)
