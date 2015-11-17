title: 使用 weinre 远程调试微信页面
tags: wechat, 微信, weinre, 移动端开发
slug: how-to-debug-wechat-web-page-with-weinre
date: 2015-11-17 20:00


![](/static/images/weinre/weinre-demo.jpg)

图片来源： <https://people.apache.org/~pmuellr/weinre-docs/latest/>

## weinre 介绍

> weinre is WEb INspector REmote. Pronounced like the word "winery". Or maybe like the word "weiner". Who knows, really.

> weinre is a debugger for web pages, like FireBug (for FireFox) and Web Inspector (for WebKit-based browsers), except it's designed to work remotely, and in particular, to allow you debug web pages on a mobile device such as a phone.

> —— 摘自 [官网](https://people.apache.org/~pmuellr/weinre-docs/latest/Home.html)


## 安装

    sudo npm -g install weinre

## 启动服务端

    weinre --boundHost 0.0.0.0 --httpPort 8081

打开本地浏览器，访问 <http://localhost:8081> 可以看到一个 web 界面：

![](/static/images/weinre/Snip20151117_7.png)           
![](/static/images/weinre/Snip20151117_8.png)


## 在待调试的页面中注入 weinre 代码

在页面中引入一个脚本就可以了，本例中是:

    <script src="http://本机ip:8081/target/target-script-min.js#anonymous"></script>


## 远程调试

打开 <http://localhost:8081/client/#anonymous> 在这个页面进行调试:


我们随便找一个公众号比如“语音云开放平台”，然后向这个公众号内的登录页面注入 `weinre` 代码，
然后，我们就可以看到打开的页面了：

![](/static/images/weinre/Screenshot_2015-11-17-14-17-26_com.tencent.mm.png)            
![](/static/images/weinre/Snip20151117_9.png)           
![](/static/images/weinre/Snip20151117_10.png)



## 修改 html

在调试页面内修改 html 内容会直接反映到移动端：

![](/static/images/weinre/Snip20151117_13.png)          
![](/static/images/weinre/Screenshot_2015-11-17-14-23-23_com.tencent.mm.png)

## 修改 css

比如修改 `background-color`:

![](/static/images/weinre/Snip20151117_14.png)         
![](/static/images/weinre/Screenshot_2015-11-17-14-25-12_com.tencent.mm.png)

## 执行 javascript

原先隐藏的菜单：

![](/static/images/weinre/Screenshot_2015-11-17-14-18-16_com.tencent.mm.png)

可以在调试页面控制台里执行 javascript 把菜单显示出来：

![](/static/images/weinre/Snip20151117_11.png)         
![](/static/images/weinre/Screenshot_2015-11-17-14-20-31_com.tencent.mm.png)

alert:

![](/static/images/weinre/Snip20151117_15.png)         
![](/static/images/weinre/Screenshot_2015-11-17-14-26-05_com.tencent.mm.png)



更多内容请查阅 [官方文档](https://people.apache.org/~pmuellr/weinre-docs/latest/) ;)


## 参考资料

* [weinre 官网](https://people.apache.org/~pmuellr/weinre-docs/latest/)