Title: [git]按日期列出所有分支信息
Date: 2013-08-17
Tags: git
Slug: git-show-branches-by-date

    :::console
    for k in `git branch|perl -pe s/^..//`;do echo -e "\e[31m"$k"\e[0m" `git log -1 --pretty=format:'- %s %Cgreen(%ci %cr) %C(bold blue)<%an>%Creset' "$k"|head -n 2`\\t;done | sort


![git-show-branches-by-date](/static/images/2013-8-17_19-04-55.png "title")

## 参考

* [Show git branches by date - useful for showing active branches | commandlinefu.com](http://www.commandlinefu.com/commands/view/2345/show-git-branches-by-date-useful-for-showing-active-branches)
