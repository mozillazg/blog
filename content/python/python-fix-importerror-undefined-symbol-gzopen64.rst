一种解决 ImportError: ./xyz.so: undefined symbol: gzopen64 的办法
=============================================================================

:slug: python-fix-importerror-undefined-symbol-gzopen64
:date: 2016-04-17

出现 ImportError: ./xxx.so: undefined symbol: gzopen64 错误的一种原因是因为系统内安装
的 zlib so 文件的版本不是最新的 1.2.8 版本

.. code-block:: python

    >>> import xyz
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: ./xyz.so: undefined symbol: gzopen64

一种解决办法就是告诉 python 使用最新的 zlib 1.2.8 的 so 文件

1. 从 http://www.zlib.net/ 下载最新版的 zlib 源码包(1.2.8, tar.gz)

.. code-block:: shell

    wget http://zlib.net/zlib-1.2.8.tar.gz
    tar zxvf zlib-1.2.8.tar.gz
    cd zlib-1.2.8
    ./configure
    make && make install

2. 告诉程序使用最新的 zlib so 文件

.. code-block:: shell

    export LD_PRELOAD=/usr/local/lib/libz.so.1
    python
    ....
    >>> import xyz
    >>>  

参考资料
------------

* `ImportError: ../libunity_shared.so: undefined symbol: gzopen64 - Dato Forum <http://forum.dato.com/discussion/1125/importerror-libunity-shared-so-undefined-symbol-gzopen64>`__