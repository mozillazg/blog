Title: [python]解决 64 位 windows 下使用 pip 安装带 c 扩展的模块时，出现 "ValueError: [u'path']" 错误
Date: 2013-06-06
Tags: python, ValueError
Slug: python-Windows-x64-compile-c-valueerror-path

今天在 64 位 Windows 下使用 pip 安装 rcssmin 时，出现了如下错误：

>     :::bash
>     ...
>        File "C:\Python27\lib\distutils\msvc9compiler.py", line 299, in query_vcvarsall
>      
>           raise ValueError(str(list(result.keys())))
>      
>      ValueError: [u'path']

这是因为在编译 c 扩展程序时，出现了错误。

解决办法是，安装 Visual Studio 2008 Professional x64，并且在安装时选中 x64 compiler tools:

![install vs2008](/static/images/install_vs_x64_compiler_tools.png)

## 参考

* [command line - Value error trying to install Python for Windows extensions - Stack Overflow](http://stackoverflow.com/questions/4676728/value-error-trying-to-install-python-for-windows-extensions)
