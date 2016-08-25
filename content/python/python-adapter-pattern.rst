Python 设计模式: 适配器模式(adapter pattern)
===================================================
:date: 2016-08-22
:slug: python-adapter-pattern
:tags: design pattern, 设计模式

在不修改原对象代码的基础上，把对象的不兼容接口封装成调用者需要的兼容接口即为适配器模式。比如新代码要对接老代码，但是又不想修改老代码，可以使用适配器模式将老代码封装为新代码需要的接口。


比如:

.. code-block:: python

    class QiniuClient:
        def __init__(self, ...):
            self._client = Qiniu(...)

        def get_content(self, path):
            content = self._client.get(path, ...)
            return content


    class OSSClient:
        def __init__(self, ...):
            self._client = OSS(...)

        def get_content(self, path):
            content = self._client.get_data(path, ...)
            return content

    def download(client, remote_path, local_path):
        with open(local_path, 'wb') as fp:
            content = client.get_content(remote_path)
            fp.write(content)

    client = OSSClient(...)
    download(client, '/hello/world.json', 'hello.json')


参考资料
-----------
* `《Mastering Python Design Patterns》 <https://book.douban.com/subject/26336439/>`_
