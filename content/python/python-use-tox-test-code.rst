[python]使用 tox 测试代码在不同环境下的兼容性
=================================================

:date: 2014-07-16
:tag: python, tox, test
:slug: python-use-tox-test-code


Tox 是什么？
--------------

Tox 是个标准的 `virtualenv`_ 管理器和命令行测试工具。你可以用于:

* 检查你的软件包能否在不同的 Python 版本或解释器下正常安装
* 在不同的环境中运行运行你的测试代码
* 作为持续集成服务器的前端，大大减少测试工作所需时间

.. _virtualenv: https://pypi.python.org/pypi/virtualenv


安装
-------

``pip install tox``


简单使用
---------

**使用前，请确保系统中已经安装了不同版本的 Python 解释器** : ::

     ~$ python -V
    Python 2.7.6
     ~$ python2.6 -V
    Python 2.6.9
     ~$ python3.3 -V
    Python 3.3.2+
     ~$ python3.4 -V
    Python 3.4.0
     ~$ pypy -V
    Python 2.7.3 (2.2.1+dfsg-1, Nov 28 2013, 05:13:10)
    [PyPy 2.2.1 with GCC 4.8.2]

假设有个项目叫 hello_tox, 包含 test_hello.py 和 setup.py 两个文件。

``test_hello.py`` 内容如下： ::

    def test_hell():
        print 'hello'

``setup.py`` 内容如下： ::

    from setuptools import setup

    setup(
        name="test_tox",
        script=['test_hello'],
    )

下面将演示如何使用 tox 测试这个程序。


建立配置文件
+++++++++++++

可以通过 ``tox-quickstart`` 命令或文本编辑器在 **项目根目录/setup.py 所在目录** 建立配置文件 tox.ini : ::

    # content of: tox.ini , put in same dir as setup.py
    [tox]
    # 要测试的 Python 版本
    envlist = py27,py34
    [testenv]
    # 安装依赖
    deps=pytest
    # 测试时要执行的命令
    commands=py.test

现在目录结构如下： ::

     ~/hello_tox$ tree
    .
    ├── setup.py
    ├── test_hello.py
    └── tox.ini

    0 directories, 3 files

执行 ``tox`` 命令: ::

     ~/hello_tox$ tox
    GLOB sdist-make: /home/xxx/hello_tox/setup.py
    py27 create: /home/xxx/hello_tox/.tox/py27
    py27 installdeps: pytest
    py27 inst: /home/xxx/hello_tox/.tox/dist/test_tox-0.0.0.zip
    py27 runtests: PYTHONHASHSEED='2501568866'
    py27 runtests: commands[0] | py.test
    ================================================================ test session starts ================================================================
    platform linux2 -- Python 2.7.6 -- py-1.4.21 -- pytest-2.5.2
    collected 1 items 

    test_hello.py .

    ============================================================= 1 passed in 0.01 seconds ==============================================================
    py34 create: /home/xxx/hello_tox/.tox/py34
    py34 installdeps: pytest
    py34 inst: /home/xxx/hello_tox/.tox/dist/test_tox-0.0.0.zip
    py34 runtests: PYTHONHASHSEED='2501568866'
    py34 runtests: commands[0] | py.test
    ================================================================ test session starts ================================================================
    platform linux -- Python 3.4.0 -- py-1.4.21 -- pytest-2.5.2
    collected 0 items / 1 errors 

    ====================================================================== ERRORS =======================================================================
    __________________________________________________________ ERROR collecting test_hello.py ___________________________________________________________
    .tox/py34/lib/python3.4/site-packages/_pytest/python.py:451: in _importtestmodule
        mod = self.fspath.pyimport(ensuresyspath=True)
    .tox/py34/lib/python3.4/site-packages/py/_path/local.py:620: in pyimport
        __import__(modname)
    E     File "/home/xxx/hello_tox/test_hello.py", line 2
    E       print 'hello'
    E                   ^
    E   SyntaxError: invalid syntax
    ============================================================== 1 error in 0.05 seconds ==============================================================
    ERROR: InvocationError: '/home/xxx/hello_tox/.tox/py34/bin/py.test'
    ______________________________________________________________________ summary ______________________________________________________________________
      py27: commands succeeded
    ERROR:   py34: commands failed
     ~/hello_tox$ 

上面就是测试的结果了。


高级使用
--------

自定义环境
++++++++++

默认支持如下环境名称：

* py24  (python 2.4)
* py25  (python 2.5)
* py26  (python 2.6)
* py27  (python 2.7)
* py30  (python 3.0)
* py31  (python 3.1)
* py32  (python 3.2)
* py33  (python 3.3)
* py34  (python 3.4)
* jython (jpython)
* pypy   (pypy)

自定义不同的环境，比如说

* py26-webpy  (python 2.6 + web.py)
* py33-bottle (python 3.3 + bottle)

修改上面的 tox.ini 文件: ::

    # content of: tox.ini , put in same dir as setup.py
    [tox]
    # 环境列表
    envlist = py26-webpy,py33-bottle

    [testenv]
    # 测试时要执行的命令
    commands = py.test

    # 定义名为 base 的环境
    [base]
    deps = pytest

    # 定义名为 py26-webpy 的环境
    [testenv:py26-webpy]
    # Python 解释器
    basepython = python2.6
    # 依赖
    # 同时应用 base 中定义的 deps 变量
    deps =
      {[base]deps}
      web.py

    # 定义名为 py33-bottle 的环境
    [testenv:py33-bottle]
    basepython = python3.3
    deps =
      {[base]deps}
      bottle

更改 test_hello.py 文件: ::

    import web
    import bottle


    def test_hell():
        print 'hello'

执行 `tox` 命令: ::

     ~/hello_tox$ tox
    GLOB sdist-make: /home/xxx/hello_tox/setup.py
    py26-webpy create: /home/xxx/hello_tox/.tox/py26-webpy
    py26-webpy installdeps: pytest, web.py
    py26-webpy inst: /home/xxx/hello_tox/.tox/dist/test_tox-0.0.0.zip
    py26-webpy runtests: PYTHONHASHSEED='4132868947'
    py26-webpy runtests: commands[0] | py.test
    =================================================== test session starts ====================================================
    platform linux2 -- Python 2.6.9 -- py-1.4.21 -- pytest-2.5.2
    collected 0 items / 1 errors 

    ========================================================== ERRORS ==========================================================
    ______________________________________________ ERROR collecting test_hello.py ______________________________________________
    test_hello.py:2: in <module>
        import bottle
    E   ImportError: No module named bottle
    ================================================= 1 error in 0.05 seconds ==================================================
    ERROR: InvocationError: '/home/xxx/hello_tox/.tox/py26-webpy/bin/py.test'
    py33-bottle create: /home/xxx/hello_tox/.tox/py33-bottle
    py33-bottle installdeps: pytest, bottle
    py33-bottle inst: /home/xxx/hello_tox/.tox/dist/test_tox-0.0.0.zip
    py33-bottle runtests: PYTHONHASHSEED='4132868947'
    py33-bottle runtests: commands[0] | py.test
    =================================================== test session starts ====================================================
    platform linux -- Python 3.3.2 -- py-1.4.21 -- pytest-2.5.2
    collected 0 items / 1 errors 

    ========================================================== ERRORS ==========================================================
    ______________________________________________ ERROR collecting test_hello.py ______________________________________________
    .tox/py33-bottle/lib/python3.3/site-packages/_pytest/python.py:451: in _importtestmodule
        mod = self.fspath.pyimport(ensuresyspath=True)
    .tox/py33-bottle/lib/python3.3/site-packages/py/_path/local.py:620: in pyimport
        __import__(modname)
    E     File "/home/xxx/hello_tox/test_hello.py", line 6
    E       print 'hello'
    E                   ^
    E   SyntaxError: invalid syntax
    ================================================= 1 error in 0.04 seconds ==================================================
    ERROR: InvocationError: '/home/xxx/hello_tox/.tox/py33-bottle/bin/py.test'
    _________________________________________________________ summary __________________________________________________________
    ERROR:   py26-webpy: commands failed
    ERROR:   py33-bottle: commands failed
     ~/hello_tox$

其他用法请阅读 `Tox 官方文档`_ 或后续更新。

.. _`Tox 官方文档`: http://tox.readthedocs.org/en/latest/