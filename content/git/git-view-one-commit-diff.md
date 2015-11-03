title: git 查看某个 commit 的改动
slug: git-view-one-commit-diff
date: 2015-11-03


命令如下：

    git show COMMIT

或

    git diff COMMIT^!


比如：

    git show d34ff657f5
    git diff d34ff657f5^!


## 参考资料

* <http://stackoverflow.com/questions/7663451/view-a-specific-git-commit>
* <http://stackoverflow.com/questions/17563726/git-diff-for-one-commit>