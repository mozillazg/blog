[git]如何删除在远程已被删除的本地分支（清理本地分支）
=======================================================

:date: 2014-02-12
:tags: git
:slug: git-delete-all-local-branches-which-are-remotely-deleted

通过 ``git fetch -p`` 命令可以实现清理本地分支的功能::

    $ git fetch -p
     x [deleted]         (none)     -> origin/feature-xxx
     x [deleted]         (none)     -> origin/feature-xxxx
     x [deleted]         (none)     -> origin/feature-xxxxx
     x [deleted]         (none)     -> origin/hotfix-xx

    # 然后再执行
    $ git branch -r | awk '{print $1}' | egrep -v -f /dev/fd/0 <(git branch -vv | grep origin) | awk '{print $1}' | xargs git branch -d



参考资料
----------

* `How do you remove an invalid remote branch reference from Git? - Stack Overflow <http://stackoverflow.com/questions/1072171/how-do-you-remove-an-invalid-remote-branch-reference-from-git>`__
* `Git: How to prune local tracking branches that do not exist on remote anymore - Stack Overflow <http://stackoverflow.com/questions/13064613/git-how-to-prune-local-tracking-branches-that-do-not-exist-on-remote-anymore>`__