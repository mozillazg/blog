Python 设计模式: 桥接模式(bridge pattern)
==================================================
:date: 2016-09-17
:slug: python-bridge-pattern
:tags: design pattern, 设计模式

桥接模式用于将"抽象"(abstraction, 比如接口或算法)与实现方式相分离。

如果不用桥接模式，那么通常的做法是，创建若干个基类用于表示各个抽象方式，
然后从每个基类中继承出两个或多个子类，用于表示对这种抽象方式的不同实现方法。
用了桥接模式之后，我们需要创建两套独立的"类体系"（class hierarchy）: "抽象体系"
定义了我们所要执行的操作（比如接口或高层算法），而“实现体系”则包含具体实现方式，
抽象体系要调用实现体系以完成其操作。抽象体系中的类会把实现体系中的某个类实例
聚合进来，而这个实例将充当抽象接口与具体实现之间的桥梁(bridge)。


.. code-block:: python


    class OSSClient:
        def __init__(self, ...):
            self._client = OSS(...)

        def url_to_path(self, url):
            path = ...
            return path

        def get_content(self, path):
            content = self._client.get_data(path, ...)
            return content

        def put_content(self, path, content):
            self._client.put_data(path, content)


    class Downloader:
        def __init__(self, client):
            self._client = client

        def download(url, local_path):
            with open(local_path, 'wb') as fp:
                remote_path = self._client.url_to_path(url)
                data = self._client.get_content(remote_path)
                fp.write(data)

上面的 ``OSSClient`` 即为实现体系类， ``Downloader`` 是抽象体系类：

抽象体系中的类(``Downloader``)会把实现体系中的某个类(``OSSClient``)实例
聚合进来，而这个实例将充当抽象接口与具体实现之间的桥梁(bridge)。


参考资料
-----------
* `《Python in Practice》 <https://book.douban.com/subject/24390228/>`_
