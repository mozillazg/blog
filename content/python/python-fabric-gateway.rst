[python]配置 fabric 穿越跳板机
==============================

:date: 2013-12-27
:tags: python, fabric, fab, gateway, 跳板机
:slug: python-fabric-gateway

说实话，跳板机给研发的日常工作添加了些许麻烦。
幸好 fabric 提供了穿越跳板机的功能，使跳板机不再影响我们的工作。

.. code-block:: console

    $ fab --version
    Fabric 1.8.1
    Paramiko 1.12.0

.. code-block:: python

    # 跳板机
    env.gateway = 'lisi@192.168.100.123'

    # 目标服务器
    env.hosts = ['foo@111.111.111.111']

    env.passwords = {
        'lisi@192.168.100.123:22': 'pssword3',  # 跳板机密码
        'foo@111.111.111.111:22': 'pssword4',   # 目标服务器密码
    }

    @task
    @hosts(env.hosts)
    def foobar():
        pass

穿越跳板机的原理是： `SSH 隧道技术 <http://en.wikipedia.org/wiki/Tunneling_protocol>`__ 。


参考资料
--------

* `The environment dictionary, env — Fabric 1.8.1 documentation <http://docs.fabfile.org/en/latest/usage/env.html#gateway>`__
* `Pre-filling env.passwords no longer works in 1.7 · Issue #976 · fabric/fabric · GitHub <https://github.com/fabric/fabric/issues/976>`__
* `Tunneling protocol - Wikipedia, the free encyclopedia <http://en.wikipedia.org/wiki/Tunneling_protocol>`__
