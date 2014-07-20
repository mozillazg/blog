Title: 修复启动 sqldeveloper 时出现“Unable to create an instance of the Java Virtual Machine Located at path”错误
Date: 2014-07-17
Tags: sqldeveloper
Slug: fix-Unable-to-create-an-instance-of-the-Java-Virtual-Machine-Located-at-path-error-for-oracle-sqldeveloper

刚才打开 sqldeveloper 时提示如下错误：

    Unable to create an instance of the Java Virtual Machine
    Located at path:
    x:\xxxx\jre\bin\client\jvm.dll

最后的解决办法是：编辑 `sqldeveloper.exe` 所在目录下的 `ide\bin\ide.conf` 文件，
将 38 行左右的 `AddVMOption  -Xmx800M` 改为 `AddVMOption -Xmx512M`

    # AddVMOption  -Xmx800M
    AddVMOption -Xmx512M


## 参考资料

* [Solution to ‘Unable to Create an Instance of the Java Virtual Machine’ for JDeveloper | In Piscean's Heart ](http://pisceansheart.wordpress.com/2009/08/06/solution-to-unable-to-create-an-instance-of-the-java-virtual-machine-for-jdeveloper/)