Python 探针实现原理
=======================

:slug: apm-python-agent-principle
:date: 2016-04-04
:tags: import, sys.meta_path, sitecustomize, usercustomize, 探针, APM

本文将简单讲述一下 Python 探针的实现原理。
同时为了验证这个原理，我们也会一起来实现一个简单的统计指定函数执行时间的探针程序。

探针的实现主要涉及以下几个知识点:

* sys.meta_path
* sitecustomize.py

sys.meta_path
---------------

``sys.meta_path`` 这个简单的来说就是可以实现 import hook 的功能，
当执行 import 相关的操作时，会触发 ``sys.meta_path`` 列表中定义的对象。
关于 ``sys.meta_path`` 更详细的资料请查阅 python 文档中 `sys.meta_path`_ 相关内容以及
`PEP 0302`_ 。

``sys.meta_path`` 中的对象需要实现一个 ``find_module`` 方法，
这个 ``find_module`` 方法返回 ``None`` 或一个实现了 ``load_module`` 方法的对象
(代码可以从 github 上下载 `part1`_) :

.. code-block:: python

    import sys


    class MetaPathFinder:

        def find_module(self, fullname, path=None):
            print('find_module {}'.format(fullname))
            return MetaPathLoader()


    class MetaPathLoader:

        def load_module(self, fullname):
            print('load_module {}'.format(fullname))
            sys.modules[fullname] = sys
            return sys

    sys.meta_path.insert(0, MetaPathFinder())

    if __name__ == '__main__':
        import http
        print(http)
        print(http.version_info)

``load_module`` 方法返回一个 module 对象，这个对象就是 import 的 module 对象了。
比如我上面那样就把 ``http`` 替换为 ``sys`` 这个 module 了。


.. code-block:: shell

    $ python meta_path1.py
    find_module http
    load_module http
    <module 'sys' (built-in)>
    sys.version_info(major=3, minor=5, micro=1, releaselevel='final', serial=0)


通过 ``sys.meta_path`` 我们就可以实现 import hook 的功能：
当 import 预定的 module 时，对这个 module 里的对象来个狸猫换太子，
从而实现获取函数或方法的执行时间等探测信息。

上面说到了狸猫换太子，那么怎么对一个对象进行狸猫换太子的操作呢？
对于函数对象，我们可以使用装饰器的方式来替换函数对象(代码可以从 github 上下载 `part2`_) :


.. code-block:: python
     
    import functools
    import time


    def func_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('start func')
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print('spent {}s'.format(end - start))
            return result
        return wrapper


    def sleep(n):
        time.sleep(n)
        return n

    if __name__ == '__main__':
        func = func_wrapper(sleep)
        print(func(3))

执行结果::

    $ python func_wrapper.py
    start func
    spent 3.004966974258423s
    3

下面我们来实现一个计算指定模块的指定函数的执行时间的功能(代码可以从 github 上下载 `part3`_) 。

假设我们的模块文件是 hello.py:

.. code-block:: python

    import time


    def sleep(n):
        time.sleep(n)
        return n

我们的 import hook 是 hook.py:

.. code-block:: python

    import functools
    import importlib
    import sys
    import time

    _hook_modules = {'hello'}


    class MetaPathFinder:

        def find_module(self, fullname, path=None):
            print('find_module {}'.format(fullname))
            if fullname in _hook_modules:
                return MetaPathLoader()


    class MetaPathLoader:

        def load_module(self, fullname):
            print('load_module {}'.format(fullname))
            # ``sys.modules`` 中保存的是已经导入过的 module
            if fullname in sys.modules:
                return sys.modules[fullname]

            # 先从 sys.meta_path 中删除自定义的 finder
            # 防止下面执行 import_module 的时候再次触发此 finder
            # 从而出现递归调用的问题
            finder = sys.meta_path.pop(0)
            # 导入 module
            module = importlib.import_module(fullname)

            module_hook(fullname, module)

            sys.meta_path.insert(0, finder)
            return module

    sys.meta_path.insert(0, MetaPathFinder())


    def module_hook(fullname, module):
        if fullname == 'hello':
            module.sleep = func_wrapper(module.sleep)


    def func_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('start func')
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print('spent {}s'.format(end - start))
            return result
        return wrapper

测试代码:

.. code-block:: python

    >>> import hook
    >>> import hello
    find_module hello
    load_module hello
    >>>
    >>> hello.sleep(3)
    start func
    spent 3.0029919147491455s
    3
    >>>

其实上面的代码已经实现了探针的基本功能。不过有一个问题就是上面的代码需要显示的
执行 ``import hook`` 操作才会注册上我们定义的 hook。

那么有没有办法在启动 python 解释器的时候自动执行 ``import hook`` 的操作呢？
答案就是可以通过定义 sitecustomize.py 的方式来实现这个功能。


sitecustomize.py
------------------

简单的说就是，python 解释器初始化的时候会自动 import ``PYTHONPATH`` 下存在的
``sitecustomize`` 和 ``usercustomize`` 模块:

实验项目的目录结构如下(代码可以从 github 上下载 `part4`_) ::

    $ tree
    .
    ├── sitecustomize.py
    └── usercustomize.p

``sitecustomize.py``::

    $ cat sitecustomize.py
    print('this is sitecustomize')

``usercustomize.py``::

    $ cat usercustomize.py
    print('this is usercustomize')

把当前目录加到 ``PYTHONPATH`` 中，然后看看效果::


    $ export PYTHONPATH=.
    $ python
    this is sitecustomize       <----
    this is usercustomize       <----
    Python 3.5.1 (default, Dec 24 2015, 17:20:27)
    [GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

可以看到确实自动导入了。所以我们可以把之前的探测程序改为支持自动执行 ``import hook``
(代码可以从 github 上下载 `part5`_) 。

目录结构::

    $ tree
    .
    ├── hello.py
    ├── hook.py
    ├── sitecustomize.py

sitecustomize.py::

    $ cat sitecustomize.py
    import hook

结果::

    $ export PYTHONPATH=.
    $ python
    find_module usercustomize
    Python 3.5.1 (default, Dec 24 2015, 17:20:27)
    [GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    find_module readline
    find_module atexit
    find_module rlcompleter
    >>>
    >>> import hello
    find_module hello
    load_module hello
    >>>
    >>> hello.sleep(3)
    start func
    spent 3.005002021789551s
    3

不过上面的探测程序其实还有一个问题，那就是需要手动修改 ``PYTHONPATH`` 。
用过探针程序的朋友应该会记得， 使用 newrelic 之类的探针只需要执行一条命令就
可以了： ``newrelic-admin run-program python hello.py``
实际上修改 ``PYTHONPATH`` 的操作是在 ``newrelic-admin`` 这个程序里完成的。

下面我们也要来实现一个类似的命令行程序，就叫 ``agent.py`` 吧。

agent
-------

还是在上一个程序的基础上修改。先调整一个目录结构，把 hook 操作放到一个单独的目录下，
方便设置 ``PYTHONPATH`` 后不会有其他的干扰（代码可以从 github 上下载 `part6`_ ）。

::

    $ mkdir bootstrap
    $ mv hook.py bootstrap/_hook.py
    $ touch bootstrap/__init__.py
    $ touch agent.py
    $ tree
    .
    ├── bootstrap
    │   ├── __init__.py
    │   ├── _hook.py
    │   └── sitecustomize.py
    ├── hello.py
    ├── test.py
    ├── agent.py

``bootstrap/sitecustomize.py`` 的内容修改为::

    $ cat bootstrap/sitecustomize.py
    import _hook

agent.py 的内容如下:

.. code-block:: python

    import os
    import sys

    current_dir = os.path.dirname(os.path.realpath(__file__))
    boot_dir = os.path.join(current_dir, 'bootstrap')


    def main():
        args = sys.argv[1:]
        os.environ['PYTHONPATH'] = boot_dir
        # 执行后面的 python 程序命令
        # sys.executable 是 python 解释器程序的绝对路径 ``which python``
        # >>> sys.executable
        # '/usr/local/var/pyenv/versions/3.5.1/bin/python3.5'
        os.execl(sys.executable, sys.executable, *args)

    if __name__ == '__main__':
        main()

``test.py`` 的内容为::

    $ cat test.py
    import sys
    import hello

    print(sys.argv)
    print(hello.sleep(3))

使用方法::

    $ python agent.py test.py arg1 arg2
    find_module usercustomize
    find_module hello
    load_module hello
    ['test.py', 'arg1', 'arg2']
    start func
    spent 3.005035161972046s
    3


至此，我们就实现了一个简单的 python 探针程序。当然，跟实际使用的探针程序相比肯定是有
很大的差距的，这篇文章主要是讲解一下探针背后的实现原理。

如果大家对商用探针程序的具体实现感兴趣的话，可以看一下国外的 `New Relic`_ 或国内的 `OneAPM`_, `TingYun`_
等这些 APM 厂商的商用 python 探针的源代码，相信你会发现一些很有趣的事情。

.. 浏览了一下这两家的代码（通过上面的链接可以下载到各自的源代码），
.. 其中 OneAPM 的代码跟 New Relic 的 太像了，目录结构，类，方法，函数之类的完全一个模子出来的， copy 成分居多（纯复制😓） 。
..
.. TingYun 的代码跟 New Relic 的目录结构差别比较大，里面的类，方法，函数之类的差别
.. 也比较大，应该是借鉴的成分居多（不排除有个别功能是 copy 的，没细看）。
..
.. 网络上 2014 年的讨论:
.. OneAPM: https://www.v2ex.com/t/125736
.. TingYun: https://www.v2ex.com/t/214359


.. _sys.meta_path: https://docs.python.org/3/library/sys.html#sys.meta_path
.. _PEP 0302: https://www.python.org/dev/peps/pep-0302/
.. _关于描述符的介绍: https://docs.python.org/3/howto/descriptor.html
.. _sitecustomize.py: 
.. _part1: https://github.com/mozillazg/apm-python-agent-principle/tree/master/part1
.. _part2: https://github.com/mozillazg/apm-python-agent-principle/tree/master/part2
.. _part3: https://github.com/mozillazg/apm-python-agent-principle/tree/master/part3
.. _part4: https://github.com/mozillazg/apm-python-agent-principle/tree/master/part4
.. _part5: https://github.com/mozillazg/apm-python-agent-principle/tree/master/part5
.. _part6: https://github.com/mozillazg/apm-python-agent-principle/tree/master/part6
.. _New Relic: https://pypi.python.org/pypi/newrelic
.. _OneAPM: http://pypi.oneapm.com/simple/blueware/
.. _TingYun: http://doc.tingyun.com/help/html/doc/sdkServerDownload.html?tabType=python
