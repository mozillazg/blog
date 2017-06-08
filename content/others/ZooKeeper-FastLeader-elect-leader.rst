ZooKeeper FastLeader 选举
===========================

:slug: zookeeper-fastleader-elect-leader
:date: 2017-03-11
:tags: zookeeper, leader选举


ZooKeeper 在集群模式下默认会使用 FastLeader 算法来选举 leader。下面将说说 ZooKeeper 集群使用 FastLeader 算法选举的具体过程。写的过程中参考了多篇文章，详见文末的参考资料。

首先需要明确几个概念:

* 节点状态：每个集群中的节点都有一个状态 LOOKING/FOLLOWING/LEADING/OBSERVING。每个节点启动的时候都是 LOOKING 状态，如果这个节点参与选举但最后不是leader，则状态是 FOLLOWING，如果不参与选举则是 OBSERVING，leader 的状态是 LEADING。
* epoch: 表示选举轮数。
* zxid: 事务 zxid 包含了本地数据的最后更新时间相关的信息。
* serverid: 当前 server 的 ID, 通过配置文件指定(比如: ``echo '1' > myid``)。

先用文字描述一下大概的选举思想：

* 在没有遇到比我牛的人之前，第一票推荐我自己
* 当接收到其他人的选举信息时，如果他们推荐的人没我牛，那我还是推荐我自己
* 我有一个票箱，保存了当前这一轮选举中自己的推荐人以及接收到的推荐人信息，一人一票，重复或过期的票概不接受
* 当我发现了比我牛的人的时候，改为推荐这个牛人
* 如果我发现我的选举轮数落后了，清空票箱，改为推荐接收到的最新选举中大家推荐的最牛的那个人（如果没有人比我牛，那还是推荐我自己）
* 不断的重复上面的过程，不断的告诉别人“我的投票是第几轮”、“我推举的人是谁”。直到我的票箱中“我推举的最牛的人”收到了不少于 **N / 2 + 1** 的推举投票，此时这个人就是我认定的最终 leader。
* 当我确定了谁是最终 leader 并且这个 leader 一切正常，我就更新我的状态为 FOLLOWING/LEADING（我自己是最终  leader 则是 LEADING 否则就是 FOLLOWING），之后的选举中都直接反馈我确定的这个最终 leader。

那么，以什么标准来确定一个节点可以成为一个 leader 呢？
依次比较 epoch, zxid, serverid ：

* 接收到的消息中，有 epoch 比我大的，则选 epoch 大的消息中确定的 server
* 如果 epoch 相等，则选 zxid 最大的 server
* 如果 zxid 也相等，则选 serverid 最大的 server (有的节点生来就是当 leader 的 😂）

.. code-block:: java

    switch (n.state) {  
    //LOOKING消息，则  
    case LOOKING:  
    ......  
        //检查下收到的这张选票是否可以胜出，依次比较选举轮数epoch，事务zxid，服务器编号server id  
        } else if (totalOrderPredicate(n.leader, n.zxid, n.peerEpoch,  
                proposedLeader, proposedZxid, proposedEpoch)) {  
            //胜出了，就把自己的投票修改为对方的，然后广播消息  
            updateProposal(n.leader, n.zxid, n.peerEpoch);  
            sendNotifications();  
        }
    }

    protected boolean totalOrderPredicate(long newId, long newZxid, long newEpoch, long curId, long curZxid, long curEpoch) {
        return (
            (newEpoch > curEpoch) || 
            ((newEpoch == curEpoch) &&
            ((newZxid > curZxid) || ((newZxid == curZxid) &&
            (newId > curId))))
        );
        }


从网上找了一个流程图，可以看看：

|flow.png|


举个例子，理想情况下，先后启动三个节点的选举过程如下：

* 第一轮：每个节点广播选自己（此时只有 node1)
* 第二轮：node2 启动了，发起一轮投票。node1 收到了 node2 选它自己的投票，发现 node2 比自己牛，广播选 node2。此时 node1 发现 node2 获得了2票 >= N / 2 + 1，认定 node2 为 leader 进入 following 状态。
  node2 收到了 node1 选自己的广播，此时 node2 发现自己 获得了2票 >= N / 2 + 1，进入 leading 状态。
* 第三轮：node3 启动了，发起一轮投票。node1 和 node2 都选 node2 , node3 通过比对发现 node2 的票数 >= N /2 + 1，认定 node2 是 leader 进入 following 状态。


上面就是 FastLeader 算法选举的简单介绍了，更详细的信息可以查阅官方文档和代码。


参考
-----

* `图解zookeeper FastLeader选举算法 - loop in codes <http://codemacro.com/2014/10/19/zk-fastleaderelection/>`_
* `zookeeper3.3.3源码分析(二)FastLeader选举算法 - xhh198781的专栏 - 博客频道 - CSDN.NET <http://blog.csdn.net/xhh198781/article/details/6619203>`_
* `深入浅出Zookeeper之五 Leader选举 - 吊丝码农 - ITeye技术网站 <http://iwinit.iteye.com/blog/1773531>`_
* `Zookeeper-Zookeeper leader选举 - 横刀天笑 - 博客园 <http://www.cnblogs.com/yuyijq/p/4116365.html>`_
* `hadoop系列：zookeeper（2）——zookeeper核心原理（选举） - JAVA入门中 - 博客频道 - CSDN.NET <http://blog.csdn.net/yinwenjie/article/details/47613309>`_
* `zookeeper/FastLeaderElection.java at branch-3.4 · apache/zookeeper <https://github.com/apache/zookeeper/blob/branch-3.4/src/java/main/org/apache/zookeeper/server/quorum/FastLeaderElection.java>`_
* `ZooKeeper Administrator's Guide <http://zookeeper.apache.org/doc/r3.4.10/zookeeperAdmin.html#sc_configuration>`_

.. |flow.png| image:: /static/images/zookeeper/elect-leader.png
