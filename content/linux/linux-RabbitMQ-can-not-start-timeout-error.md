Title: [linux]无法启动 rabbitmq-server，出现 timeout 错误
Date: 2013-10-20
Tags: linux
Slug: linux-RabbitMQ-server-can-not-start-with-host-timeout-error

上次安装 rabbitmq 时，有台服务器上 `service rabbitmq-server start` 总是起不来。
错误日志里出现如下错误：

    ERROR: epmd error for host "yourhostname": timeout (xxxxx)

解决办法就是, 修改 /etc/hosts 将本机的 hostname 加进去：

    127.0.0.1    yourhostname


## 参考

* [RabbitMQ - Amazon EC2](http://www.rabbitmq.com/ec2.html#issues-hostname)
* [Troubleshooting RabbitMQ installation on OSX via homebrew](https://gist.github.com/jch/2522701)
* [rabbitmq-server starting.... TIMEOUT - Airtime Support Discussions on Sourcefabric Forum](http://forum.sourcefabric.org/discussion/comment/13783)
