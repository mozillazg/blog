[python]如何让命令行程序支持管道和重定向输入
==================================================
:slug: python-let-cli-support-pipe-read-data-from-stdin
:date: 2016-03-10

管道和重定向输入的数据都是通过标准输入传入程序的， ``sys.stdin`` 这个 file-like 对象即为标准输入。
同时也可以通过 ``sys.stdin.isatty()``
判断是否是管道和重定向输入（为 ``True`` 时表示是交互式环境，
为 ``False`` 时是我们要的场景）。

假设有个 ``hello.py``:

.. code-block:: python

    import sys


    def main():
        data = sys.argv[1:]
        if not sys.stdin.isatty():
            data.append(sys.stdin.read())
        return data


    if __name__ == '__main__':
        data = main()
        print(' '.join(data))


测试效果:

.. code-block:: shell

    $ echo "hello" > hello.txt
    $ python hello.py hello world       # 参数输入
    hello world
    $ cat hello.txt | python hello.py   # 管道输入
    hello

    $ python hello.py < hello.txt       # 重定向输入
    hello

    $


参考资料
------------

* `29.1. sys — System-specific parameters and functions — Python 3.5.1 documentation <https://docs.python.org/3/library/sys.html#sys.stdin>`__
