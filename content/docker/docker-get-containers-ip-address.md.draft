title: 如何获取 docker 容器(container)的 ip 地址
slug: docker-get-containers-ip-address
date: 2016-01-12

主要命令是 `docker inspect`:

    $ sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' 1f7d8f36523c
    172.17.0.6

可以考虑在 ~/.bashrc 中写一个 bash 函数：

    function docker_ip() {
        sudo docker inspect --format '{{ .NetworkSettings.IPAddress }}' $1
    }

`source ~/.bashrc` 然后：

    $ docker_ip 1f7d8f36523c
    172.17.0.6