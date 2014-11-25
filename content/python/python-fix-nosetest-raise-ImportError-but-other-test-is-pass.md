[python]修复 nosetest 命令报 ImportError 错误，但是实际上并不存在 ImportError 并且所有的测试程序都是通过的
Date: 2014-11-20
Tags: 
Slug: python-fix-nosetest-raise-ImportError-but-other-test-is-pass


这是因为 nose 默认会调整模板导入路径，可以先设置 `PYTHONPATH`, 然后按下述三种方式解决：

* `.noserc` 文件中加入:

    [nosetests]
    no-path-adjustment=1

* NOSE_NOPATH=y nosetest
* nosetest --no-path-adjustment


参考资料
========

* [python - Import errors when running nosetests that I can&#39;t reproduce outside of nose - Stack Overflow](http://stackoverflow.com/questions/16200333/import-errors-when-running-nosetests-that-i-cant-reproduce-outside-of-nose)
