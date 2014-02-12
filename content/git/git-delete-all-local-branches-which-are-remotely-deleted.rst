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


参考资料
----------

* `How do you remove an invalid remote branch reference from Git? - Stack Overflow <http://stackoverflow.com/questions/1072171/how-do-you-remove-an-invalid-remote-branch-reference-from-git>`__
