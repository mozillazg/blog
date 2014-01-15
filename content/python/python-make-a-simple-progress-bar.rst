[python]输出一个简单的进度条
=============================

:date: 2014-01-13
:tags: python
:slug: python-make-a-simple-progress-bar

使用 ``sys.stdout`` 或 ``sys.stderr`` 就可以输出一个简单的进度条：

.. code-block:: python

    import time
    import sys

    f = sys.stdout

    for n in range(1, 101):
        s = ('#' * n).ljust(100, '-')
        f.write(s)
        time.sleep(0.3)
        f.write('\r')
    f.write('\n')
