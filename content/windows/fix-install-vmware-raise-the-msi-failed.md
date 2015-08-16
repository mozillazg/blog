Title: 解决安装 VMware workstation 时提示“The MSI '' failed”
Date: 2015-08-15
Slug: fix-install-vmware-raise-the-msi-failed
Tags: VMware

昨天碰到了安装 VMware workstation 时提示“The MSI '' failed” 的问题，最终的解决办法如下：

1. 首先需要准备一个安装文件，比如：VMware-workstation-full-xxx.exe
2. 解压 exe 文件，在 CMD 命令行中输入（假设 exe 文件放在 f:\Downloads 目录下）：

    f:\Downloads>VMware-workstation-full-10.0.2-1744117.1398244508.exe /extract vm\

3. 进入解压后的目录，使用 vmwareworkstation_xx.msi 进行安装（32 位的系统使用 vmwareworkstation_x86.msi ，64 位的系统使用 vmwareworkstation_x64.msi）

    f:\Downloads>cd vm
    f:\Downloads\vm>vmwareworkstation_x64.msi EULAS_AGREED=1
    f:\Downloads\vm>

4. 安装完成，现在看看桌面上是不是已经有了一个 VMware Workstation 的快捷键了。:)