Title: [go]使用 goxc 方便的进行交叉编译
Date: 2015-02-28
Slug: go-use-goxc-to-cross-compile


## 安装

`go get github.com/laher/goxc`

## 使用

所有命令皆在 main 包所在目录下执行

**基本使用**

`goxc -d=build -pv=0.1.0`

上面命令的意思是：将编译好的文件保存到 `./build` 目录下，指定文件名包含的版本号为 `0.1.0`       
最后生成的文件如下：


     (master) ccuser$ tree build/
    build/
    └── 0.1.0
        ├── ccuser_0.1.0_amd64.deb
        ├── ccuser_0.1.0_armhf.deb
        ├── ccuser_0.1.0_darwin_386.zip
        ├── ccuser_0.1.0_darwin_amd64.zip
        ├── ccuser_0.1.0_dragonfly_386.zip
        ├── ccuser_0.1.0_dragonfly_amd64.zip
        ├── ccuser_0.1.0_freebsd_386.zip
        ├── ccuser_0.1.0_freebsd_amd64.zip
        ├── ccuser_0.1.0_freebsd_arm.zip
        ├── ccuser_0.1.0_i386.deb
        ├── ccuser_0.1.0_linux_386.tar.gz
        ├── ccuser_0.1.0_linux_amd64.tar.gz
        ├── ccuser_0.1.0_linux_arm.tar.gz
        ├── ccuser_0.1.0_nacl_386.zip
        ├── ccuser_0.1.0_nacl_amd64p32.zip
        ├── ccuser_0.1.0_nacl_arm.zip
        ├── ccuser_0.1.0_netbsd_386.zip
        ├── ccuser_0.1.0_netbsd_amd64.zip
        ├── ccuser_0.1.0_netbsd_arm.zip
        ├── ccuser_0.1.0_openbsd_386.zip
        ├── ccuser_0.1.0_openbsd_amd64.zip
        ├── ccuser_0.1.0_plan9_386.zip
        ├── ccuser_0.1.0_solaris_amd64.zip
        ├── ccuser_0.1.0_windows_386.zip
        ├── ccuser_0.1.0_windows_amd64.zip
        ├── downloads.md
        ├── LICENSE
        └── README.md

**指定操作系统平台**
默认全平台。


`goxc -d=build -pv=0.1.0 bc='linux,windows,darwin'`

指定只生成适用于 `linxu, windows, 苹果系统` 的文件

**指定 CPU 架构**
默认所有 CPU 架构


`goxc -d=build -pv=0.1.0 -arch='386 amd64'`


## 参考资料

* [https://github.com/laher/goxc](https://github.com/laher/goxc)