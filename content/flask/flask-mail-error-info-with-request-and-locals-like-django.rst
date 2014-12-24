[flask]出错时发送异常信息邮件（包含异常堆栈，request 信息，发生异常时的局部变量）
=======================================================================================================

:date: 2014-12-24
:slug: flask-mail-error-exception-message-with-request-and-locals-variables-like-django

最终效果（邮件内容）::


    Message type:       ERROR
    Location:           /home/xxx/site-packages/flask_restful/__init__.py:292
    Module:             __init__
    Function:           handle_error
    Time:               2014-12-24 17:59:47,876

    Message:

    Internal Error

        
    Traceback (most recent call last):
      File "/home/xxx/site-packages/flask/app.py", line 1475, in full_dispatch_request
        rv = self.dispatch_request()
      ....
      File "/home/xx/foo.py", line 81, in get
        raise Exception(u'a')
    Exception: a


    Locals:

    {
        'self': <Bar object at 0x2ab4ed05d710>,
        'data': <Foo 10, bar>,
        'id': 10,
    }

    Request:

    {
        'view_args': {
            'id': 10,
        },
        'url_rule': <Rule '/api/foos/<id>' (HEAD, GET, PATCH, POST, OPTIONS, DELETE) -> foo.xapi>,
        'cookies': {
        },
        'shallow': False,
        'environ': {
            'wsgi.multiprocess': True,
            'SERVER_SOFTWARE': 'Werkzeug/0.9.6',
            'SCRIPT_NAME': '',
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/api/foos/10',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'QUERY_STRING': '',
            'werkzeug.server.shutdown': <function shutdown_server at 0x2ab4ed05ea28>,
            'CONTENT_LENGTH': '',
            'HTTP_USER_AGENT': 'foo/0.8.0',
            'HTTP_CONNECTION': 'keep-alive',
            'SERVER_NAME': '0.0.0.0',
            'REMOTE_PORT': 56413,
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8900',
            'werkzeug.request': <Request 'http://localhost:8000/api/foos/10' [GET]>,
            'wsgi.input': <socket._fileobject object at 0x2ab4ed066050>,
            'HTTP_HOST': 'localhost:8900',
            'wsgi.multithread': False,
            'HTTP_ACCEPT': '*/*',
            'wsgi.version': (1, 0),
            'wsgi.run_once': False,
            'wsgi.errors': <open file '<stderr>', mode 'w' at 0x2ab4e6b811e0>,
            'REMOTE_ADDR': '127.0.0.1',
            'CONTENT_TYPE': '',
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
        },
    }


主要通过配置 logging SMTPHandler 来实现:

.. code-block:: python

    import inspect
    from logging.handlers import SMTPHandler
    from flask import request

    mail_handler = SMTPHandler('127.0.0.1', 'foo@example.com',
                               'dev@bar.com, 'App exception')
    mail_handler.setFormatter(NewFormatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s

    '''))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


    class NewFormatter(logging.Formatter):
        def format(self, record):
            s = super(NewFormatter, self).format(record)
            msg = '''

    Locals:

    %(locals)s

    Request:

    %(request)s
            '''
            s += msg % {
                'locals': pretty_dict_to_string(inspect.trace()[-1][0].f_locals),
                'request': pretty_dict_to_string(request.__dict__),
            }

            return s


pertty_dict_to_string 函数:

.. code-block:: python

    def pretty_dict_to_string(d, tab=1):
        s = ['{\n']
        for k, v in d.items():
            if isinstance(v, dict):
                v = pretty_dict_to_string(v, tab + 1)
            else:
                v = repr(v)
            s.append('%s%r: %s,\n' % ('    ' * tab, k, v))
        s.append('%s}' % ('    ' * (tab - 1)))
        return ''.join(s)


参考资料
----------

* `Logging Application Errors — Flask Documentation (0.10)`__
* `15.7. logging — Logging facility for Python — Python 2.7.9 documentation`__
* `cpython/Lib/logging at 2.7 · python/cpython`__

__ http://flask.pocoo.org/docs/0.10/errorhandling/
__ https://docs.python.org/2/library/logging.html
__ https://github.com/python/cpython/tree/2.7/Lib/logging