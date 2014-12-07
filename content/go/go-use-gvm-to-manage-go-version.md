

## 安装

安装依赖：

    $ sudo apt-get install curl git mercurial make binutils bison gcc build-essential

安装 gvm:


    $ bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)

如果上面的脚本提示 `git clone` 错误的话，可以通过下面的方式解决：

    $ wget https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer
    $ vim gvm-installer   # 修改 gvm-installer 文件
    $ # 将 SRC_REPO=${SRC_REPO:-https://github.com/moovweb/gvm.git} 
    $ # 改为 SRC_REPO=${SRC_REPO:-git://github.com/moovweb/gvm.git} 
    $ bash gvm-installer
    Cloning from git://github.com/moovweb/gvm.git to /home/xx/.gvm
    Created profile for existing install of Go at "/usr/lib/go"
    Installed GVM v1.0.22
    
    Please restart your terminal session or to get started right away run
     `source /home/xx/.gvm/scripts/gvm`

激活 gvm 脚本:

    $ source /home/xx/.gvm/scripts/gvm
    $ gvm version
    Go Version Manager v1.0.22 installed at /home/xx/.gvm


## 使用

安装不同版本的 go，比如安装 1.3 版本:

    $ gvm install go1.3

如果提示如下错误，是因为当前网络无法访问 go 源码仓储地址:

    $ gvm install go1.3
    Downloading Go source...
    ERROR: Couldn't download Go source. Check the logs /home/xx/.gvm/logs/go-download.log
    $ tail ~/.gvm/logs/go-download.log
    中止: 失败: Network is unreachable

可以使用我在 bitbucket 上创建的镜像库(通过 -s/--source 指定 go 源码 hg 仓库的地址）：

    $ gvm install go1.3 --source=https://mozillazg@bitbucket.org/mozillazg/go
    Downloading Go source...
    Installing go1.3...
     * Compiling...

查看系统中安装的 go 版本：

    $ gvm list
    
    gvm gos (installed)
    
       go1.3
       system

切换当前使用的 go 版本：
 
    $ go version
    go version go1.2.1 linux/amd64
    $
    $ gvm use go1.3
    Now using version go1.3
    $ go version
    go version go1.3 linux/amd64


## 参考资料

* [https://github.com/moovweb/gvm](https://github.com/moovweb/gvm)
* [https://bitbucket.org/mozillazg/go](https://bitbucket.org/mozillazg/go)