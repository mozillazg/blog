title: 修复 gitlab 中 fork 失败，提示 "visibility level private visibility has been restricted"
date: 2015-10-20
slug: gitlab-fix-fork-error-because-visibility-level-private-visibility-has-been-restricted-by-your-gitlab-administrator
tags: gitlab


版本：Gitlab 8.0.4, 错误截图：

![gitlab-fork-error-1.png](/static/images/2015/gitlab-fork-error-1.png)


出现这个错误是因为管理员没有配置 private 仓库允许 被 fork。解决办法如下（管理员身份操作）：

1. 进入【admin area】                   
![](/static/images/2015/gitlab-fork-error-2.png)

2. 【settings】               
![](/static/images/2015/gitlab-fork-error-3.png)

3. 修改【Restricted visibility levels】，**取消** Private 的选中状态            
![](/static/images/2015/gitlab-fork-error-4.png)