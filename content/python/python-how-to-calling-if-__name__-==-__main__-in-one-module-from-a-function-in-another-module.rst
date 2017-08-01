Python: 如何在一个模块中执行另一个模块的 if __name__ == '__main__' 部分的代码
==================================================================================

:slug: python-how-to-calling-if-__name__-==-__main__-in-one-module-from-a-function-in-another-module
:date: 2017-08-01
:tags: subprocess, runpy

如题所述，我们将一起来看一下如果想在一个模块中执行另一个模块中的
``if __name__ == '__main__'`` 部分的代码有哪些常用的方法。

要执行的模块的代码:

.. code:: python

    $ cat another.py
    # -*- coding: utf-8 -*-
    import sys


    def main(args):
        print(args)


    if __name__ == '__main__':
        print("run code below __name__ == '__main__'")
        main(sys.argv[1:])

通过 ``python another.py`` 运行：

::

    $ python3.6 another.py test
    run code below __name__ == '__main__'
    ['test']

使用 subprocess 模块
--------------------

示例代码如下：

.. code-block:: python

    $ cat test_a.py
    # -*- coding: utf-8 -*-
    import subprocess

    process = subprocess.run(
        ['python', 'another.py', 'test'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    print(process.stdout)

测试：

::

    $ python3.6 test_a.py
    b"run code below __name__ == '__main__'\n['test']\n"

使用 ``subprocess`` 的优点就是因为其实是通过创建一个子进程来执行的程序，所以不受子程序的影响，不会出现程序抛异常或主动退出进程导致主程序也退出的尴尬问题。 缺点就是需要创建子进程，相对来说资源消耗比较大。

``subprocess`` 详细的用法详见
`官方文档 <https://docs.python.org/3/library/subprocess.html>`__

使用 runpy 模块
-------------------

示例代码：

.. code-block:: python

    $ cat test_b.py
    # -*- coding: utf-8 -*-
    import runpy

    runpy.run_path('another.py', run_name='__main__')

测试：

::

    $ python3.6 test_b.py
    run code below __name__ == '__main__'
    []

使用 ``runpy`` 的优点就是不需要创建子进程，相对来说资源消耗比较小。 缺点就是主程序会受待执行程序的影响，会出现待执行程序中抛异常或主动退出会导致主程序也退出的尴尬问题。

``runpy`` 的详细用法详见 `官方文档 <https://docs.python.org/3/library/runpy.html>`__


结束语
---------

这两种方法就是比较常用的在一个模块中执行另一个模块的
``if __name__ == '__main__'``
部分的代码的方法。总结来说就是，一个是在子进程中执行代码，一个是在当前进程中执行代码。

希望本文能对你有所帮助。


参考资料
--------

-  `17.5. subprocess — Subprocess management — Python 3.6.2
   documentation <https://docs.python.org/3/library/subprocess.html>`__
-  `31.4. runpy — Locating and executing Python modules — Python 3.6.2
   documentation <https://docs.python.org/3/library/runpy.html>`__
-  `PEP 299 -- Special \_\_main\_\_() function in modules \|
   Python.org <https://www.python.org/dev/peps/pep-0299/>`__
