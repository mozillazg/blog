Title: [git]修复 fatal: You are on a branch yet to be born 错误
Date: 2013-08-04
Tags: git, git-submodule
Slug: git-fatal-You-are-on-a-branch-yet-to-be-born
status: draft

使用 git 添加 submodule 时，有时会错误如下错误：

$ git submodule add -f git://github.com/derekwyatt/vim-scala.git .vim/bundle/vim-scala
fatal: You are on a branch yet to be born
Unable to checkout submodule '.vim/bundle/vim-scala'
