Title: 《An Introduction to Programming in Go》学习笔记——安装 Go
Date: 2014-11-03
Slug: go-an-introduction-to-programming-in-go-notes-installation

本文介绍在 Ubuntu 下用包管理器的安装过程：

1. 安装 go: `sudo apt-get install golang`
2. 配置环境变量：
     1. ``mkdir ~/go  ~/go/src ~/go/pkg ~/go/bin          # go 工作目录``
     2. 在 ~/.bashrc 中加入 `export GOPATH=/home/your-user-name/go` （注意要把 your-user-name 替换为你本机的用户名，这里 **不能使用 `~` 代替 `/home/your-user-name`**）
3. 验证：直接在终端下输入 `go` 命令就可以了。


其他安装方式以及在其他操作系统下的安装，请参考：[https://github.com/astaxie/build-web-application-with-golang/blob/master/ebook/01.0.md](https://github.com/astaxie/build-web-application-with-golang/blob/master/ebook/01.0.md)