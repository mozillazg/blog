Title: [linux]修复 gcc 编译时的出现的 "CPU you selected does not support x86-64 instruction set" 错误
Date: 2014-05-20
Tags: linux
Slug: linux-fix-gcc-error-CPU-you-selected-does-not-support-x86-64-instruction-set

前两天在服务器上安装 `gevent` 时出现了 `gevent/gevent.core.c:1: error: CPU you selected does not support x86-64 instruction set` 错误：

    $ pip install gevent
    Downloading/unpacking gevent
      Running setup.py egg_info for package gevent
        ....
        
        building 'gevent.core' extension
        gcc -pthread -DNDEBUG -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic -D_GNU_SOURCE -fPIC -fwrapv -O2 -mcpu=i686 -march=i686 -fPIC -DLIBEV_EMBED=1 -DEV_COMMON= -DEV_CLEANUP_ENABLE=0 -DEV_EMBED_ENABLE=0 -DEV_PERIODIC_ENABLE=0 -Ibuild/temp.linux-x86_64-2.6/libev -Ilibev -I/usr/include/python2.6 -c gevent/gevent.core.c -o build/temp.linux-x86_64-2.6/gevent/gevent.core.o
        
        gevent/gevent.core.c:1: error: CPU you selected does not support x86-64 instruction set
        
        error: command 'gcc' failed with exit status 1
        
        ....
 
最后使用的解决方法是设置一下环境变量 `CFLAGS`:

    $ CFLAGS='-march=x86-64'
    $ pip install gevent


## 参考资料

* [Pip install - CPU you selected does not support x86-64 instruction set](http://unix.stackexchange.com/questions/82089/pip-install-cpu-you-selected-does-not-support-x86-64-instruction-set)