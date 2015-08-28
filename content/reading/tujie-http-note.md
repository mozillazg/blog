Title:《图解 HTTP》阅读笔记
Date: 2015-08-28
Tags: HTTP, 图解 HTTP
Slug: tujie-http-note

[![图解 HTTP](/static/images/reading/tujie-http-note/s27283822.jpg)](http://book.douban.com/subject/25863515/)

本文记录了我阅读 《图解 HTTP》这本书时觉得重要的或之前不知道的内容。


## 了解 Web 及网络基础

**TCP/IP 四层模型**

* 应用层：HTTP, FTP, DNS 协议之类的处于这一层
* 传输层：提供两台计算机之间的数据传输，TCP, UDP 协议处于这一层
* 网络层：处理在网络上流动的数据包，IP 协议处于这一层
* 链路层（数据链路层）：处理网络的硬件部分：网卡，光纤等物理可见的部分。

![图解 HTTP](/static/images/reading/tujie-http-note/1.jpg)


![图解 HTTP](/static/images/reading/tujie-http-note/2.jpg)

**IP 协议**

使用 ARP 协议凭借 MAC 地址进行通信

ip -> mac1 -> mac2 -> mac3 -> mac

ARP 协议（Address Resolution Protocol）是一种用以解析地址的协议，
根据通信方的 IP 地址就可以反查出对应的 MAC 地址。

![图解 HTTP](/static/images/reading/tujie-http-note/3.jpg)


**TCP 三次握手**

我要给你发数据了 SYN (发送端） -> 回应一个收到 SYN + ACK（接收端） -> 回应一个 OK ACK （发送端）

![图解 HTTP](/static/images/reading/tujie-http-note/4.jpg)

**各协议与 HTTP 协议的关系**

![图解 HTTP](/static/images/reading/tujie-http-note/5.jpg)


**URI 和 URL**

* URI：统一资源标识符（Uniform Resource Identifier），比如：
    * http://abc.com/a.txt
    * redis://127.0.0.1/0
    * mailto:foo@bar.com
    * tel:+86123455
* URL：统一资源定位符（Uniform Resource Locator）即我们熟悉的网址，比如：
    * http://abc.com/a.txt
    * https://foo.bar.com/foobar.txt

URI 用字符串标识某一互联网资源，而 URL 表示资源的地点（互联网上所处的位置）。
**可见 URL 是 URI 的子集** 。

<!--
## 简单的 HTTP 协议

## HTTP 报文内的 HTTP 信息

## 返回结果中的 HTTP 状态码
-->

## 与 HTTP 协作的 Web 服务器

HTTP 通信时，处客户端和服务器外，还有一些用于通信数据转发的应用程序，例如：代理，网关和隧道。

* 代理：代理是一种有转发功能的应用程序，它扮演了位于服务器和客户端“中间人”的角色，接收由客户端发送的
  请求并转发给服务器，同时也接收服务器返回的响应并转发给客户端。
    * 缓存代理：代理转发响应时，缓存代理会预先将资源的副本（缓存）保存在代理服务器上。
    * 透明代理：转发请求或响应时，不对报文做任何加工的代理类型被称为透明代理。反之，对
      报文内容进行加工的代理被成为非透明代理。
* 网关：网关是转发其他服务器通信数据的服务器，接收从客户端发送来的请求时，它就像自己拥有资源
  的源服务器一样对请求进行处理。有时客户端可能都不会察觉，自己的通信目标是一个网关。
  网关的工作机制和代理十分相似。而网关能使通信线路上的服务器提供非 HTTP 协议服务。
* 隧道：隧道是在相隔甚远的客户端和服务器两者之间进行中转，并保持双方通信连接的应用程序。


## HTTP 首部

* `Cache-Control`
    * `no-cache`: 使用 no-cache 指令的目的是为了防止从缓存总返回过期的资源。
      事实上， no-cache 代表不缓存过期的资源，缓存会向源服务器进行有效期确认，然后再处理资源。
    * `no-store`: 该指令规定缓存不能在本地存储请求或响应的任一部分。
* `Pragma` 是 HTTP/1.1 之前版本的历史遗留字段。
    * `Pargma: no-cache`: 只能用在客户端发送的请求中。客户端会要求所有的中间服务器不返回缓存的资源。
      但要整体掌握全部中间服务器使用 HTTP 协议版本确实不现实的。因此，发送的请求会同时含有
      `Cache-Control: no-cache`和 `Pragma: no-cache`
* X-Frame-Options: 作用于 HTTP 响应，用于控制网站内容在其他 Web 网站的 Frame 标签内的显示问题。
  其主要目的是为了防止点击劫持（clickjacking）攻击。
    * `DENY`: 拒绝
    * `SAMEORIGINE`: 仅同源域名下的页面可以加载
* X-XSS-Protection: 用于控制浏览器 XSS 防护机制的开关
    * `0`: 将 XSS 过滤设置为无效状态
    * `1`: 将 XSS 过滤设置为有效状态
* DNT: 拒绝个人信息被收集
    * `0`: 同意被追踪
    * `1`: 拒绝被追踪

**协议中对 X- 前缀的废除**

在 HTTP 等多种协议中，通过给非标准参数加上前缀 X-, 来区分标准参数，并使
那些非标准的参数作为扩展变成可能。但是这种简单粗暴的做法有百害而无一益，
因此在 "RFC 6648 - Deprecating the "X-" Prefix and Similar
Constructs in Application Protocols" 中提议停止该做法。

然而，对已经在使用中的 X- 前缀来说，不应该要求其变更。


## 确保 HTTP 安全的 HTTPS
 
HTTP 协议的实现本是非常简单，不论是谁发送过来的请求都会返回响应，
因此不确认通信方，会存在以下各种隐患。

* 无法确定请求发送至目标的 Web 服务器是否是按真实意图返回响应的那台服务器。
  有可能是已伪装的 Web 服务器。
* 无法确定响应返回到的客户端是否是按真实意图接收响应的那个客户端。有可能是已伪装的客户端。
* 无法确定正在通信的对方是否具有访问权限。因为某些 Web 服务器上保存着重要的信息，
  只想发给特定用户通信的权限。
* 无法判定请求是来自何方、出自谁手。
* 即时是无意义的请求也会照单全收。无法阻止海量请求下的 DoS 攻击（Denial of Service, 拒绝服务器攻击）。

HTTP + 加密 + 认证 + 完整性包含 = HTTPS

HTTPS 并非是应用层的一种新协议。只是 HTTP 通信接口部分用 SSL(Secure Socket Layer) 和
TLS(Transport Layer Security)协议代替而已。

通常， HTTP 直接和 TCP 通信。当使用 SSL 时，则演变成先和
SSL 通信，再由 SSL 和 TCP 通信了。简言之，所谓 HTTPS，其实就是身披 SSL 协议这层外壳的 HTTP。
所以 HTTPS 又叫 HTTP over SSL, HTTP over TLS

**对称密钥加密**: 加密和解密同用一个密钥的方式称为共享密钥加密(Common key crypto system)，
也被叫做对称密钥加密。

**非对称加密**：公开密钥加密方式很好地解决了共享密钥加密的困难。公开密钥加密使用一对非对称密钥。一把叫做私有密钥
(private key)，另一把叫做公开密钥（public key）。顾名思义，私有密钥
不能让其他任何人知道，而公开密钥则可以随意发布，任何人都可以获得。

**HTTPS 通信步骤**

![图解 HTTP](/static/images/reading/tujie-http-note/6.jpg)

![图解 HTTP](/static/images/reading/tujie-http-note/7.jpg)

![图解 HTTP](/static/images/reading/tujie-http-note/8.jpg)


**为什么不一直使用 HTTPS** 既然 HTTPS 那么安全可靠，那为何所有的 Web 网站不一直使用 HTTPS？

* 其中一个原因是，因为与纯文本通信相比，加密通信会消耗更多的 CPU 及内存资源。如果每次通信都加密，会消耗
  相当多的资源，平摊到一台计算机上时，能够处理的请求数量必定也会随之减少。
* 除此之外，想要节约购买证书的开销也是原因之一。

## 基于 HTTP 的功能追加协议

HTTP 的瓶颈

* 一条连接只可发送一个请求
* 请求只能从客户端开始。客户端不可以接收除响应以外的指令
* 请求/响应首部(header)未经压缩就发送。首部信息越多延迟越大。
* 发送冗长的首部(header)。每次互相发送相同的首部造成的浪费较多。
* 可任意选择数据压缩格式。非强制压缩发送。

**SPDY**

SPDY 以会话层的形式加入，控制对数据的流动，但还是采用 HTTP 建立通信连接。
使用 SPDY 后，HTTP 协议额外获得以下功能：

* 多路复用流：通过单一的 TCP 请求，可以无限制处理多个 HTTP 请求。所有请求的处理
  都在一条 TCP 连接上完成，因此 TCP 的处理效率得到提高。
* 赋予请求优先级
* 压缩 HTTP 首部(header)
* 推送功能：支持服务器主动向客户端推送数据。
* 服务器提示功能：服务器可以主动提示客户端请求所需的资源。

![图解 HTTP](/static/images/reading/tujie-http-note/9.jpg)



**使用浏览器进行全双工的 WebSocket**

一旦 Web 服务器与客户端之间建立起 WebSocket 协议的通信连接，之后所有
的通信都依靠这个专用协议进行。 WebSocket 协议的主要特点：

* 推送功能
* 减少通信量：只要建立起 WebSocket 连接，就希望一直保持连接状态。

![图解 HTTP](/static/images/reading/tujie-http-note/10.jpg)


**期盼已久的 HTTP/2.0**

以下摘自： https://http2.github.io/faq/

> What are the key differences to HTTP/1.x?

> At a high level, HTTP/2:

> * is binary, instead of textual
> * is fully multiplexed, instead of ordered and blocking
> * can therefore use one connection for parallelism
> * uses header compression to reduce overhead
> * allows servers to “push” responses proactively into client caches

## Web 的攻击技术

因输出值转义不完全引发的安全漏洞：

* **跨站脚本攻击（Cross-Site Scripting, XSS）** 主要是指在用户浏览器内运行了非法的 HTML 标签或 JavaScript 
  脚本。比如富文本编辑器，如果不过滤用户输入的数据直接显示用户输入的 HTML 内容的话，就会有可能运行恶意的 
  JavaScript 脚本，导致页面结构错乱，Cookies 信息被窃取等问题。
* **SQL 注入攻击（SQL Injection）** 是指针对 Web 应用使用的数据库，通过运行非法
  的 SQL 而产生的攻击。
* **OS 命令注入攻击（OS Command Injection）** 是指通过 Web 应用，执行非法的操作系统命令达到攻击的目的。
  只要在能调用 Shell 函数的地方就有存在被攻击的风险。
* **HTTP 首部注入攻击（HTTP Header Injection）** 是指攻击者通过在响应首部字段内插入换行，添加任意响应首部
  或主体的一种攻击。属于被动工具模式。
* **HTTP 响应截断攻击** 是用在 HTTP 首部注入的一种攻击。攻击顺序相同，但是要将两个 %0D%0A%0D%0A 并排插入字符串后
  发送。利用两个连续的换行就可作出 HTTP 首部与主体分隔所需的空行了，这样
  就能显示伪造的主体，达到攻击的目的。这样的攻击叫做 HTTP 响应截断攻击。
* **邮件首部注入攻击（Mail Header Injection）** 是指 Web 应用中的邮件发送功能，攻击者通过向邮件首部
  To 或 Subject 内任意添加非法内容发起的攻击。利用存在安全漏洞的 Web 网站，可对任意邮件地址发送广告邮件或
  病毒邮件。
* **目录遍历攻击（Directory Traversal）** 是指对本无意公开的文件目录，通过非法截断其目录路径后，达成访问
  目的的一种攻击。比如，通过 ../ 等相对路径定位到 /etc/passwd 等绝对路径上。
* **远程文件包含漏洞（Remote File Inclusion）** 是指当部分脚本内容需要从其他文件读入是，攻击者利用指定外部服务器
  的 URL 充当依赖文件，让脚本读取之后，就可运行任意脚本的一种攻击。

因设置或设计上的缺陷引发的安全漏洞：
  
* **强制浏览（Forced Browsing）安全漏洞** 是指，从安置在 Web 服务器的公开目录下的文件中，浏览那些原本非自愿公开
  的文件。比如，没有对那些需要保护的静态资源增加权限控制。
* **不正确的错误消息处理（Error Handling Vulerability）的安全漏洞** 是指，Web 应用的错误信息内包含对攻击者有用
  的信息。
* **开放重定向（Open Redirect）** 是一种对指定的任意 URL 作重定向跳转的功能。而于此功能相关联的安全漏洞是指，
  假如指定的重定向 URL 到某个具有恶意的 Web 网站，那么用户就会被诱导至那个 Web 网站。

因会话管理疏忽引发的安全漏洞：

* **会话劫持（Session Hijiack）** 是指攻击者通过某种手段拿到了用户的会话 ID，并非法使用此会话 ID 伪装成
  用户，达到攻击的目的。
* 对以窃取目标会话 ID 为主动攻击手段的会话劫持而言， **会话固定攻击（Session Fixation）** 会强制用户使用攻击者指定
  的会话 ID，属于被动攻击。
* **跨站请求伪造（Cross-Site Request Forgeries, CSRF）攻击** 是指攻击者通过设置好陷阱，
  强制对已完成认证的用户进行非预期的个人信息或设定等某些状态更新，属于被动攻击。

其他安全漏洞：

* **密码破解**
* **点击劫持（Clickjacking）** 是指利用透明的按钮或链接做成陷阱，覆盖在 Web 页面之上。然后诱使用户在不知情的情况下，
  单击那个链接访问内容的一种攻击手段。这种行为又称为界面伪装（UI Redressing）。
* **DoS 攻击（Denial of Service attack）** 是一种让运行中的服务呈停止状态的攻击。
  有时也叫做服务停止攻击或拒绝服务攻击。多台计算机发起的 Dos 攻击称为
  **DDoS 攻击（Distributed Denial of Service attach）** 。
* **后门程序（Backdoor）** 是指开发设置的隐藏入口，可不按正常步骤使用受限功能。利用后门程序就能够使用原本受限的功能。