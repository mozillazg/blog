title: git clone 时使用了 --depth 后，如何再重新拉取全部的历史
slug: git-revert-depth-1
date: 2016-01-10

有时我们为了加快 clone 的速度会使用 `--depth` 参数，比如：

    git clone https://xxx/xxx.git --depth 1


如果我们之后要把之前的历史重新再 `pull` 下来呢？
比如要把本地的仓库 `push` 到一个新的空仓库（
会出现 `error: failed to push some refs` 错误
）。

可以使用 `--unshallow` 参数：

    git pull --unshallow
