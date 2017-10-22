解决 HAProxy 节点网络异常（sendmsg: Invalid argument, Connection timed out ）的办法
=============================================================================================

:slug: linux-a-way-to-fix-haproxy-network-connection-timeout-ping-sendmsg-Invalid-argument-socket-errno-110-connection-timed-out
:date: 2017-10-21
:tags: ping, sysctl, HAProxy, ARP

问题
--------

之前连接一个 HAProxy 前端服务时总是时不时出现 ``[Errno 110] Connection timed out`` ，并且本地 ping 服务器丢包率特别高。
到服务器上看了以后，发现 ``ping 127.0.0.1`` 的丢包率也特别高，而且 ping
命令还出现 ``ping: sendmsg: Invalid argument`` 错误::

    64 bytes from 127.0.0.1: icmp_seq=150 ttl=64 time=0.050 ms
    64 bytes from 127.0.0.1: icmp_seq=151 ttl=64 time=0.062 ms
    ping: sendmsg: Invalid argument
    ping: sendmsg: Invalid argument
    ping: sendmsg: Invalid argument
    ping: sendmsg: Invalid argument
    ping: sendmsg: Invalid argument
    ping: sendmsg: Invalid argument
    64 bytes from 127.0.0.1: icmp_seq=158 ttl=64 time=0.962 ms
    64 bytes from 127.0.0.1: icmp_seq=159 ttl=64 time=0.033 ms

查看 ``dmesg -H`` 有很多类似 ``net_ratelimit: 478 callbacks suppressed`` 的记录::

    ```
    [  +6.555833] net_ratelimit: 478 callbacks suppressed
    [Oct19 11:08] net_ratelimit: 57 callbacks suppressed
    ```

需要提一下的就是，这个 HAProxy 服务在一个非常大的内网(large subnets)里，
内网里很多机器都会去连接这个服务。


解决方法
---------------

修改了一下 sysctl, 加大了 ARP cache::

    $ sudo sysctl -w net.ipv4.neigh.default.gc_thresh1=1024
    $ sudo sysctl -w net.ipv4.neigh.default.gc_thresh2=2048
    $ sudo sysctl -w net.ipv4.neigh.default.gc_thresh3=4096
    $ sudo sysctl -p
    $ sudo sysctl -a |grep net.ipv4.neigh.default.gc_thresh


为什么要修改为上面的值？
~~~~~~~~~~~~~~~~~~~~~~~~


先来看看这几个配置项的含义(摘自 https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt)::


    neigh/default/gc_thresh1 - INTEGER
        Minimum number of entries to keep.  Garbage collector will not
        purge entries if there are fewer than this number.
        Default: 128

    neigh/default/gc_thresh2 - INTEGER
        Threshold when garbage collector becomes more aggressive about
        purging entries. Entries older than 5 seconds will be cleared
        when over this number.
        Default: 512

    neigh/default/gc_thresh3 - INTEGER
        Maximum number of neighbor entries allowed.  Increase this
        when using large numbers of interfaces and when communicating
        with large numbers of directly-connected peers.
        Default: 1024

ARP 相关的 `简单解释就是 <https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Welcome%20to%20High%20Performance%20Computing%20(HPC)%20Central/page/Linux%20System%20Tuning%20Recommendations>`_ (详见 `arp(7) <http://man7.org/linux/man-pages/man7/arp.7.html>`_):

* ``net.ipv4.neigh.default.gc_thresh1``: min IPV4 entries to keep in ARP cache -  garbage collection never runs if this many or less entries are in cache
* ``net.ipv4.neigh.default.gc_thresh2``: IPV4 entries allowed in ARP cache before garbage collection will be scheduled in 5 seconds
* ``net.ipv4.neigh.default.gc_thresh3``: maximum IPV4 entries allowed in ARP cache; garbage collection runs when this many entries reached

然后我们通过 ``arp -an|wc -l`` 查看当前记录的 ARP 记录的数量::

    $ arp -an|wc -l
    1108

或者通过 ``ip -4 neigh show nud all | wc -l`` 查看当前 IPv4 的 ARP 记录的数量::

    $ ip -4 neigh show nud all | wc -l
    1112


可以看到上面的值比 ``net.ipv4.neigh.default.gc_thresh3`` 的默认值 ``1024`` 要大，
<del>*此时就会进行 gc 操作，如果 gc 操作持续时间太久就会导致新的 ARP 记录无法被创建，进而导致 ARP 通信无法正常完成，TCP 之类的操作更加就无法完成了(有空的时候再仔细求证这个理解...)* ，</del> 所以我们要修改为更大的值。

如果上面的值特别大，可以考虑配置再大一点的值，比如::

    net.ipv4.neigh.default.gc_thresh1 = 8192
    net.ipv4.neigh.default.gc_thresh2 = 32768
    net.ipv4.neigh.default.gc_thresh3 = 65536


注：上面修改的都是 IPv4 相关的配置，如果有用到 IPv6 网络的话可以把对应的配置项也修改一下。
注：如果机器性能特别好或者比较介意 gc，可以考虑把值调到非常非常大，然后禁用 gc:
``net.ipv4.neigh.default.gc_interval``, ``net.ipv4.neigh.default.gc_stale_time``


参考资料
-----------

* `Bug 1316981 – Arp table kernel tuning necessary for large neutron environments <https://bugzilla.redhat.com/show_bug.cgi?id=1316981>`_
* `Bug 1498213 – Increase ARP cache size on loadbalancers <https://bugzilla.redhat.com/show_bug.cgi?id=1498213>`_
* `Chapter 4. Setting up a Router - Red Hat Customer Portal <https://access.redhat.com/documentation/en-us/openshift_container_platform/3.4/html/installation_and_configuration/setting-up-a-router#deploy-router-arp-cach-tuning-for-large-scale-clusters>`_
* `ARP cache: What is it and how can it help you? - Petri <https://www.petri.com/csc_arp_cache>`_
* `kernel.org/doc/Documentation/networking/ip-sysctl.txt <https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt>`_
* `Welcome to High Performance Computing (HPC) Central : Linux System Tuning Recommendations <https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Welcome%20to%20High%20Performance%20Computing%20(HPC)%20Central/page/Linux%20System%20Tuning%20Recommendations>`_
* `router - What happens when the ARP cache overflows? - Network Engineering Stack Exchange <https://networkengineering.stackexchange.com/questions/2327/what-happens-when-the-arp-cache-overflows>`_
* `PacketFence: Solving neighbour table overflow errors (large subnets) <https://packetfence.org/support/faq/article/solving-neighbour-table-overflow-errors-large-subnets.html?no_cache=1>`_
* `Kernel: Neighbour table overflow | Mark's Blog <https://www.e-rave.nl/kernel-neighbour-table-overflow>`_
* `arp(7) - Linux manual page <http://man7.org/linux/man-pages/man7/arp.7.html>`_
* `ARP and ARP Cache - 35629 - The Cisco Learning Network <https://learningnetwork.cisco.com/thread/35629>`_
* `The TCP/IP Guide - ARP Caching <http://www.tcpipguide.com/free/t_ARPCaching.htm>`_
* `Address Resolution Protocol - Wikipedia <https://en.wikipedia.org/wiki/Address_Resolution_Protocol>`_
