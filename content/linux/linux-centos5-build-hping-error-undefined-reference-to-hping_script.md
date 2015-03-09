title: [linx]解决编译 hping 时出现 "undefined reference to `hping_script'" 错误
date: 2015-03-08
slug: linux-centos5-build-hping-error-undefined-reference-to-hping_script

错误信息如下：

    $ sudo make
    ...
    pd.o -L/usr/local/lib -lpcap  -ltcl8.4.threads -lm -lpthread
    main.o: In function `main':
    /xxx/main.c:186: undefined reference to `hping_script'
    collect2: ld returned 1 exit status
    make: *** [hping3] Error 1

解决: 执行 `make clean`

    $ sudo make clean
    rm -rf hping3 *.o libars.a
    $ sudo make
    ...
    This binary is TCL scripting capable
    use `make strip' to strip hping3 binary
    use `make install' to install hping3


## 参考资料

* [http://wiki.hping.org/20](http://wiki.hping.org/20)