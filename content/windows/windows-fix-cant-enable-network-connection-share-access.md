Title: [windows] 修复无法启用网络连接共享，提示 “0x80004005” 错误
Date: 2014-08-14
Tags: windows
Slug: windows-fix-cant-enable-network-connection-share-access-0x80004005-error


今天在配置笔记本网络连接共享时，提示如下错误信息：

    ---------------------------
    Network Connections
    ---------------------------
    Cannot enable shared access.

    Error 0x80004005: Unspecified error

后来通过 **启用 Windows 防火墙服务** 的方式解决了。


## 参考资料

* [Error "Cannot enable shared access.0x80004005" when sharing - Microsoft Community ](http://answers.microsoft.com/en-us/windows/forum/windows_7-networking/error-cannot-enable-shared-access0x80004005-when/43da0b01-ab0d-49de-8fba-7b8edad5cde0)