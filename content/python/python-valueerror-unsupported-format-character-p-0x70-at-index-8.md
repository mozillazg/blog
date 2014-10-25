Title: [python]解决使用 argparse 时出现：ValueError: unsupported format character 'p' (0x70) at index 8
Date: 2013-06-07
Tags: python, argparse
Slug: python-valueerror-unsupported-format-character-p-0x70-at-index-8

将程序从 optparse 转到 argparse 后，出现了如下错误：

>     ...
>       File "C:\PYTHON26\lib\site-packages\argparse-1.2.1-py2.6.egg\argparse.py", line 230, in format_help
>         func(*args)
>       File "C:\PYTHON26\lib\site-packages\argparse-1.2.1-py2.6.egg\argparse.py", line 317, in _format_usage
>         usage = usage % dict(prog=self._prog)
>     ValueError: unsupported format character 'p' (0x70) at index 8
>     

将程序中的 `%prog` 改为 `%(prog)s` ，`%default` 改为 `%(default)s` 即可。


## 参考

* [\[Python-Dev\] Pronouncement on PEP 389: argparse?](http://mail.python.org/pipermail/python-dev/2009-December/094598.html)
* [argparse — Parser for command-line options, arguments and sub-commands - Python 2.7 Documentation](http://docs.python.org/2/library/argparse.html)
