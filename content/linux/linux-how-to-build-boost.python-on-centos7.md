title: 如何在 centos 7 上编译 boost
slug: linux-how-to-build-boost.python-on-centos7.md
tags: boost, python, c++
date: 2016-04-17

本文主要记录一下如何在 centos 7 上编译 boost 库，同时也适用于 ubuntu（安装系统包的命令需要改为 `apt-get`）

1. 安装编译工具 `clang` ，也可以使用 `gcc` 代替，只需要将下面命令中的 `clang` 替换为 `gcc` 即可

        yum install clang

2. 下载 boost: 

    1. 下载 boost_1_60_0.tar.gz( <http://sourceforge.net/projects/boost/files/boost/1.60.0/> )
    2. 解压: 
        
            mv boost_1_60_0.tar.gz /opt/
            cd /opt/
            tar zxvf boost_1_60_0.tar.gz

3. 编译 boost（同时编译所有的 boost lib， **内存和 CPU 如果不够的话可能会编译失败甚至导致系统死机** ）

        cd boost_1_60_0/
        # 可以通过 ./bootstrap.sh --help 查看更多选项
        ./bootstrap.sh  --with-toolset=clang --with-libraries=all
        ./b2

4. 编译安装 boost.build

        cd toos/build/
        ./bootstrap.sh  --with-toolset=clang
        ./b2

5. 设置 ld

        echo "/opt/boost_1_60_0/stage/lib" >> /etc/ld.so.conf
        ldconfig

6. 需要记下的几个路径，代码编译的时候可能会用到

        * boost 目录: `/opt/boost_1_60_0/`
        * lib 目录:  `/opt/boost_1_60_0/stage/lib`
   

## 参考资料:

* [Boost Getting Started on Unix Variants - 1.60.0](http://www.boost.org/doc/libs/1_60_0/more/getting_started/unix-variants.html)

