[python]如何在生产环境下更新 tornado 项目代码
=====================================================

:date: 2015-03-27
:slug: how-to-restart-or-update-tornado-code-on-fly-in-production


本文将讲述一种在线上环境下更新 tornado 项目代码的方法。

一般 tornado HTTP 服务都类似下面这样的：

* 用 nginx 做反向代理、负载均衡和静态文件服务器
* 同时起多个 tornado 进程服务多个端口

假设配置文件如下::

    upstream tornado_server {
        server 127.0.0.1:5001;
    } 

线上重启 tornado 服务的思路如下：

1. 更新代码
2. 使用不同的端口启动新的 tornado 服务: `start tornado_5002`
3. 更改 nginx 配置，将新端口加入到配置中，降低旧服务端口的权重::

    upstream tornado_server {
        server 127.0.0.1:5001;   # old
        server 127.0.0.1:5002 weight=9;   # add new
    }

4. 应用新的 nginx 配置（注意看是否有错误提示）: `nginx -t && nginx -s reload`
5. 一段时间后，更新 nginx 配置，删除/注释掉旧服务的端口配置::

    upstream tornado_server {
        # server 127.0.0.1:5001;      # remove old
        server 127.0.0.1:5002;             # new
    }

6. 应用新的 nginx 配置（注意看是否有错误提示）: `nginx -t && nginx -s reload`
7. 一段时间后，停止旧的 tornado 服务: `stop tornado_5001`


参考资料
---------

* `Running and deploying —— Tornado documentation <http://www.tornadoweb.org/en/stable/guide/running.html>`_
* `Module ngx_http_upstream_module <http://nginx.org/en/docs/http/ngx_http_upstream_module.html>`_
* `nginx command-line parameters <http://nginx.org/en/docs/switches.html>`_
* `Is there a way to deploy new code with Tornado/Python without restarting the server? - Stack Overflow`__

__ http://stackoverflow.com/questions/8086885/is-there-a-way-to-deploy-new-code-with-tornado-python-without-restarting-the-ser