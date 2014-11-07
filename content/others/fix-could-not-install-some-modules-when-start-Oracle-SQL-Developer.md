Title: 修复无法启动 Oracle SQL Developer，提示：could not install some modules
Date: 2014-11-02
Slug: fix-could-not-install-some-modules-when-start-Oracle-SQL-Developer

今天启动 Oracle SQL Developer时，提示如下错误：

    Warning - could not install some modules:

导致不能成功启动 Oracle SQL Developer。

最后的解决办法是（ **注意，这个办法会导致丢失所有之前定义的数据库连接配置** ）：

 **删除 c:\Users\yourusername\AppData\Roaming\SQL Developer\ 目录下的 system4.0.0.12.84 文件夹** 。
 
 
 
## 参考资料

* [Sql Developer 4.0 EA Winsdows 7 Could not insta... | Oracle Community](https://community.oracle.com/thread/2560920?start=0&tstart=0)
