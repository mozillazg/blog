让我们一起来构建一个 Web 服务器（二）
================================================================

:slug: let-us-build-a-web-server-part-2-zh-cn
:date: 2015-06-06
:modified: 2015-06-10
:tags: server, http, wsgi, lsbaws

本文译自：http://ruslanspivak.com/lsbaws-part2/


还记得吗？在 `第一部分`_ 我向你问了一个问题：”如何在你新鲜出炉的 Web 服务器上不做任何修改的就运行 Django 应用，Flask 应用， Pyramid 应用?“
往下读就可以找到答案。


在过去，当你选择的 Python Web 框架会限制你所能选择的 Web 服务器, 如果那个框架和服务器被设计的可以一起工作的话，那就皆大欢喜了：

|Server Framework Fit|


但是，当你尝试把一个服务器和一个框架一起使用的时候可能会（可能你已经）面临它们被设计为不兼容的情况：

|Server Framework Clash|


一般来说你必须使用能够一起工作的组件而不仅仅是你想使用的组件。


那么，你如何确保你能够在你的 Web 服务器上运行多个 Web 框架，并且不需要修改 Web 服务器或 Web 框架的现有的代码呢？
解决这个问题的答案就是 Python Web Server Gateway Interface (或简称 WSGI , 读作 “wizgy”)

|WSGI Interface|


WSGI_ 允许开发者自由选择 Web 框架和 Web 服务器。现在你可以任意混搭不同的 Web 服务器和 Web 框架，并选择一个你需要的合适的组合。
比如，你可以 用 Gunicorn_ or `Nginx/uWSGI`_ or Waitress_ 运行 Django_, Flask_, 或 Pyramid_ . 
真正的随意混搭，感谢那些服务器和框架对 WSGI 的支持：

|Mix & Match|


因此，WSGI_ 就是我在 `第一部分`_ 向你问的并在文章开头重复过的问题的答案。
你的 Web 服务器必须实现 WSGI 接口的服务器端部分，
所有的现代 Python Web 框架都已经实现了 WSGI 接口的框架端部分，
这部分允许你不需要修改你的服务器代码去适应某个特定的框架就可以使用这些框架。



现在你已经知道了被 Web 服务器和 Web 框架所支持的 WSGI 允许你选择适合你的组合，
它同样也对服务器和框架的开发者有益，因为他们可以专注于标准中他们各自的区域，不会出现因为越界而踩到对方的脚趾。
其他语言也有类似的接口：例如，Java 有 `Servlet API <http://en.wikipedia.org/wiki/Java_servlet>`_，Ruby 有 `Rack <http://en.wikipedia.org/wiki/Rack_%28web_server_interface%29>`_.


一切都很棒，但是我猜你会说”Show me the code!“，好吧，一起来看看下面这个非常简约的 WSGI 服务器实现吧：

.. code-block:: python

    # Tested with Python 2.7.9, Linux & Mac OS X
    import socket
    import StringIO
    import sys


    class WSGIServer(object):

        address_family = socket.AF_INET
        socket_type = socket.SOCK_STREAM
        request_queue_size = 1

        def __init__(self, server_address):
            # Create a listening socket
            self.listen_socket = listen_socket = socket.socket(
                self.address_family,
                self.socket_type
            )
            # Allow to reuse the same address
            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind
            listen_socket.bind(server_address)
            # Activate
            listen_socket.listen(self.request_queue_size)
            # Get server host name and port
            host, port = self.listen_socket.getsockname()[:2]
            self.server_name = socket.getfqdn(host)
            self.server_port = port
            # Return headers set by Web framework/Web application
            self.headers_set = []

        def set_app(self, application):
            self.application = application

        def serve_forever(self):
            listen_socket = self.listen_socket
            while True:
                # New client connection
                self.client_connection, client_address = listen_socket.accept()
                # Handle one request and close the client connection. Then
                # loop over to wait for another client connection
                self.handle_one_request()

        def handle_one_request(self):
            self.request_data = request_data = self.client_connection.recv(1024)
            # Print formatted request data a la 'curl -v'
            print(''.join(
                '< {line}\n'.format(line=line)
                for line in request_data.splitlines()
            ))

            self.parse_request(request_data)

            # Construct environment dictionary using request data
            env = self.get_environ()

            # It's time to call our application callable and get
            # back a result that will become HTTP response body
            result = self.application(env, self.start_response)

            # Construct a response and send it back to the client
            self.finish_response(result)

        def parse_request(self, text):
            request_line = text.splitlines()[0]
            request_line = request_line.rstrip('\r\n')
            # Break down the request line into components
            (self.request_method,  # GET
             self.path,            # /hello
             self.request_version  # HTTP/1.1
             ) = request_line.split()

        def get_environ(self):
            env = {}
            # The following code snippet does not follow PEP8 conventions
            # but it's formatted the way it is for demonstration purposes
            # to emphasize the required variables and their values
            #
            # Required WSGI variables
            env['wsgi.version']      = (1, 0)
            env['wsgi.url_scheme']   = 'http'
            env['wsgi.input']        = StringIO.StringIO(self.request_data)
            env['wsgi.errors']       = sys.stderr
            env['wsgi.multithread']  = False
            env['wsgi.multiprocess'] = False
            env['wsgi.run_once']     = False
            # Required CGI variables
            env['REQUEST_METHOD']    = self.request_method    # GET
            env['PATH_INFO']         = self.path              # /hello
            env['SERVER_NAME']       = self.server_name       # localhost
            env['SERVER_PORT']       = str(self.server_port)  # 8888
            return env

        def start_response(self, status, response_headers, exc_info=None):
            # Add necessary server headers
            server_headers = [
                ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
                ('Server', 'WSGIServer 0.2'),
            ]
            self.headers_set = [status, response_headers + server_headers]
            # To adhere to WSGI specification the start_response must return
            # a 'write' callable. We simplicity's sake we'll ignore that detail
            # for now.
            # return self.finish_response

        def finish_response(self, result):
            try:
                status, response_headers = self.headers_set
                response = 'HTTP/1.1 {status}\r\n'.format(status=status)
                for header in response_headers:
                    response += '{0}: {1}\r\n'.format(*header)
                response += '\r\n'
                for data in result:
                    response += data
                # Print formatted response data a la 'curl -v'
                print(''.join(
                    '> {line}\n'.format(line=line)
                    for line in response.splitlines()
                ))
                self.client_connection.sendall(response)
            finally:
                self.client_connection.close()


    SERVER_ADDRESS = (HOST, PORT) = '', 8888


    def make_server(server_address, application):
        server = WSGIServer(server_address)
        server.set_app(application)
        return server


    if __name__ == '__main__':
        if len(sys.argv) < 2:
            sys.exit('Provide a WSGI application object as module:callable')
        app_path = sys.argv[1]
        module, application = app_path.split(':')
        module = __import__(module)
        application = getattr(module, application)
        httpd = make_server(SERVER_ADDRESS, application)
        print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
        httpd.serve_forever()



上面的代码比 `第一部分`_ 的服务器代码更长，但是，为了让你能够理解而不至于陷入细节的泥潭中，它已经足够小了（只有不到 150 行）。
上面的服务器代码同样也能做更多的工作——它能运行用你上面所见的 Web 框架（Pyramid_, Flask_, Django_, 或其他的 Python WSGI 框架）所写的基础 Web 应用，



不信？动手试一下吧。把上面的代码保存为 ``webserver2.py`` 或者直接从 `GitHub  <https://github.com/rspivak/lsbaws/blob/master/part2/webserver2.py>`__ 上下载下来。如果你不带任何参数就运行这个程序的话，它会向你抱怨，然后退出。 ::

    $ python webserver2.py
    Provide a WSGI application object as module:callable



它真的非常想要服务你的 Web 应用，这是个非常有趣的开始。
为了能够运行这个服务器你只需要安装 Python 就可以了。
但是，为了运行用 Pyramid_, Flask_, 或 Django_ 开发的应用，你需要首先安装这些框架。
让我们来安装这三个框架吧。
我喜欢使用 virtualenv_. 只需按照下面的步骤去创建并激活一个虚拟环境，然后就可以安装这三个框架了。 ::

    $ [sudo] pip install virtualenv
    $ mkdir ~/envs
    $ virtualenv ~/envs/lsbaws/
    $ cd ~/envs/lsbaws/
    $ ls
    bin  include  lib
    $ source bin/activate
    (lsbaws) $ pip install pyramid
    (lsbaws) $ pip install flask
    (lsbaws) $ pip install django


到这一步的时候你需要创建一个 Web 应用。让我们先用 Pyramid_ 开始吧。把下面的代码保存为 ``pyramidapp.py``  并放到你之前所保存的 ``webserver2.py`` 文件或直接从 `GitHub <https://github.com/rspivak/lsbaws/blob/master/part2/pyramidapp.py>`__ 所下载的文件所在目录（即：把 ``pyramidapp.py`` 放在 ``webserver2.py`` 所在目录）：

.. code-block:: python

    from pyramid.config import Configurator
    from pyramid.response import Response


    def hello_world(request):
        return Response(
            'Hello world from Pyramid!\n',
            content_type='text/plain',
        )

    config = Configurator()
    config.add_route('hello', '/hello')
    config.add_view(hello_world, route_name='hello')
    app = config.make_wsgi_app()
    
    

现在，你可以准备用你自己的 Web 服务器来服务你的 Pyramid 应用了： ::

    (lsbaws) $ python webserver2.py pyramidapp:app
    WSGIServer: Serving HTTP on port 8888 ...



你只需告诉你的服务器从 python 模块 ``pyramidapp`` 中载入一个可调用的 ``app`` 对象，你的服务器现在已经准备好
接收请求并把它们转发给你的 Pyramid 应用了。
这个应用目前只处理了一个路由：``/hello`` 路由。
在你的浏览器中输入 http://localhost:8888/hello 地址，然后按下回车键，注意返回的结果：

|Pyramid|


你也可以在命令行中使用 ``curl`` 命令来测试这个服务器： ::

    $ curl -v http://localhost:8888/hello
    ...


检查服务器以及 ``curl`` 打印到标准输出的内容。



现在轮到 Flask_ 了。让我们按照相同的步骤来操作。

.. code-block:: python

    from flask import Flask
    from flask import Response
    flask_app = Flask('flaskapp')


    @flask_app.route('/hello')
    def hello_world():
        return Response(
            'Hello world from Flask!\n',
            mimetype='text/plain'
        )

    app = flask_app.wsgi_app

    
把上面的代码保存为 ``flaskapp.py``  或从 `GitHub <https://github.com/rspivak/lsbaws/blob/master/part2/flaskapp.py>`__ 上下载，然后用以下方式运行服务器: ::

    (lsbaws) $ python webserver2.py flaskapp:app
    WSGIServer: Serving HTTP on port 8888 ...


    
现在在你的浏览器中输入 http://localhost:8888/hello 然后按下回车键：

|Flask|


再一次，尝试 ``curl`` 命令，然后看一下服务器返回的由这个 Flask 应用所生成的信息： ::

    $ curl -v http://localhost:8888/hello
    ...


    
这个服务器能处理 Django_ 应用吗啊？试一下就知道了！
这次涉及的东西有点复杂，我建议你克隆这个 `仓库 <https://github.com/rspivak/lsbaws/>`__ 然后使用  GitHub 仓库 中的 `djangoapp.py <https://github.com/rspivak/lsbaws/blob/master/part2/djangoapp.py>`__ 文件。
下面的源码主要是添加 Django ``helloworld`` 项目（预先使用 Django 的 ``django-admin.py startproject`` 命令）到当前 Python 路径
然后导入项目中的 WSGI 应用。

.. code-block:: python

    import sys
    sys.path.insert(0, './helloworld')
    from helloworld import wsgi


    app = wsgi.application



把上面的代码保存为 ``djangoapp.py``  然后用你的 Web 服务器运行这个 Django 应用： ::

    (lsbaws) $ python webserver2.py djangoapp:app
    WSGIServer: Serving HTTP on port 8888 ...



    
输入如下地址并回车：

|Django|


正如你之前做过的那几次一样，你也可以在命令行中进行测试。
确认这个 Django 应用处理了你这一次的请求： ::

    $ curl -v http://localhost:8888/hello
    ...


    
你试过了吗？你有确认过这个服务器可以与这三个框架一起工作吗？
如果还没有的话，一定要试一下。
阅读很重要，但是这个系列讲的是关于重新构建，这意味着你需要手动进行这些尝试。
快去试试吧。别担心，我会等你的。
我是认真的，你必须去尝试，最好能够亲自一个字一个字的敲下所有的字符，
并确保它能达到预期的效果。



好了，你已经熟悉 WSGI 的威力了：它允许你混搭你的 Web 服务器和 Web 框架。
WSGI 规定了 Python Web 服务器和  Python Web 框架之间的一些接口。
它非常的简单，不管是在服务器还是框架端都非常容易实现。
下面的片段展示了服务器和框架端的接口：

.. code-block:: python

    def run_application(application):
        """Server code."""
        # This is where an application/framework stores
        # an HTTP status and HTTP response headers for the server
        # to transmit to the client
        headers_set = []
        # Environment dictionary with WSGI/CGI variables
        environ = {}

        def start_response(status, response_headers, exc_info=None):
            headers_set[:] = [status, response_headers]

        # Server invokes the ‘application' callable and gets back the
        # response body
        result = application(environ, start_response)
        # Server builds an HTTP response and transmits it to the client
        …

    def app(environ, start_response):
        """A barebones WSGI app."""
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Hello world!']

    run_application(app)


    
它的工作原理是这样的：


1. 框架提供了一个 ``application`` 可调用对象（WSGI 规范没有规定它应该如何被实现）
2. 每当收到来自 HTTP 客户端的请求的时候，服务器就调用这个 ``application`` 可调用对象。
   它把一个包含 WSGI/CGI 变量的字典 ``environ`` 和一个 ``start_response`` 可调用对象作为参数传递给了 ``application`` 可调用对象。
3. 框架/应用生成一个 HTTP 状态信息和 HTTP 响应头信息，并把它们传递给了 ``start_response`` 可调用对象，
   让服务器把它们存起来。框架/应用也返回了一个响应 body 信息。
4. 服务器把状态信息，响应头信息以及响应 body 信息合并为一个 HTTP 响应，然后把它传输给客户端（这一步不是规范的一部分，
   但是它是流程中的下一个逻辑步骤，为了清晰可见我把它列在了这里）


下面是这个接口的可视化图表：

|WSGI Interface Visual|

到目前位置，你已经见过了 Pyramid_, Flask_ 以及 Django_ Web 应用，你也见过了实现 WSGI 规范的服务器端代码。
你也见过不用任何框架所实现的极简 WSGI 应用的代码片段。


事实是，当你用这些框架中某个开发一个 Web 应用的时候，你是在高层面进行工作，
并没有直接与 WSGI 打交到，但是我知道非常好奇框架端的 WSGI 接口实现，也是因为你正在阅读这篇文章。
那么，让我们来创建一个不使用 Pyramid_, Flask_, Django_ 的微型 WSGI Web 应用/Web 框架，
并用你的服务器来运行它：

.. code-block:: python

    def app(environ, start_response):
        """A barebones WSGI application.

        This is a starting point for your own Web framework :)
        """
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello world from a simple WSGI application!\n']




再一次的，把上面的代码保存为 ``wsgiapp.py`` 或直接从 `GitHub <https://github.com/rspivak/lsbaws/blob/master/part2/wsgiapp.py>`__ 上下载它，然后用你的
Web 服务器像下面这样运行这个应用： ::

    (lsbaws) $ python webserver2.py wsgiapp:app
    WSGIServer: Serving HTTP on port 8888 ...




输入如下地址并按下回车键。你应该会看到这样的结果：

|Simple WSGI Application|


在学习如何创建一个 Web 服务器的同时，你刚刚又写了一个你自己的微型 WSGI WEB 框架！
真是意外之喜！


现在，让我们回到服务器都给客户端传输了什么东西。
下面是当你使用 HTTP 客户端调用你的 Pyramind 应用时，服务器生成的 HTTP 响应：

|HTTP Response Part 1|


这个响应有一些你在 `第一部分`_ 看到过的东西，但是它也有一些新东西。比如说，它有四个你之前还没见过的 `HTTP headers`_：
``Content-Type`` , ``Content-Length`` , ``Date`` 以及 ``Server`` .
这些包含在响应里的头信息是一个 Web 服务器应该要生成的信息。
虽然它们中没有一个是严格要求必须提供的。
这些头信息的目的是传输关于 HTTP 请求/响应的附加信息。

现在你已经了解了关于 WSGI 接口的更详细的信息了，下面是同一个 HTTP 响应部分是如何产生的更详细的信息：

|HTTP Response Part 2|

我还没有说过任何有关 ``environ`` 字典相关的信息，但是，基本上就是它是一个 Python 字典，它必须包含某些由 WSGI 规范所规定的 WSGI 和 CGI 变量。
解析完请求信息后，服务器从 HTTP 请求中得到这个字典所需的一些值。
这个字典看起来像下面这样：

|Environ Python Dictionary|

Web 框架使用来自这个字典里的信息来决定那个 view 可以被用来服务，基于获得的路由，请求方法等信息,
决定可以从哪里读取请求的 body 信息以及哪里可以用来写入错误信息，如果有的话。


到目前为止，你已经创建了你自己的 WSGI Web 服务器，你也用不同的 Web 框架编写过 Web 应用了。同时，你也顺便创建过极其简陋的 Web 应用/Web 框架。
真是一个操蛋的旅程。让我们来重述一下为了服务一个针对 WSGI 应用的请求信息，你的 WSGI Web 框架需要做的事情：

1. 首先，服务器启动并载入一个由你的 Web 框架/应用所定义的 ``application`` 可调用对象
2. 然后，服务器读取一个请求
3. 然后，服务器解析这个请求
4. 然后，服务器用这个请求数据构建了一个 ``environ`` 字典
5. 然后，服务器以 ``environ`` 字典和一个 ``start_response`` 可调用对象作为参数来调用 ``application`` 对象，并获得一个返回的响应 body 。
6. 然后，服务器用通过调用 ``application`` 对象获得的 body 数据以及通过 ``start_reponse`` 可调用对象设置的状态信息和响应头信息一起构建了一个 HTTP 响应。
7. 最后，服务器把 HTTP 响应传输回客户端

|Server Summary|



就这些了。你现在有了一个可以工作的 WSGI 服务器，它能够服务那些用 WSGI 兼容的 Web 框架（比如：Django_, Flask_, Pyramid_ 或者是你自己开发的 WSGI 框架) 开发的基础的 Web 应用。最棒的是不需要修改任何的服务器代码就可以与多个 Web 框架一起使用。目前看起来还不赖嘛。



在你离开前，这里有另一个问题需要你思考，”如何让你的服务器能够在同一时刻处理多个请求？“


敬请期待，在 `第三部分 <https://mozillazg.com/2015/08/let-us-build-a-web-server-part-3-zh-cn.html>`_ 我将向你展示一种方法。加油！

.. _第一部分: http://mozillazg.com/2015/06/let-us-build-a-web-server-part-1-zh-cn.html
.. _Gunicorn: http://gunicorn.org/
.. _Nginx/uWSGI: http://uwsgi-docs.readthedocs.org/
.. _Waitress: http://waitress.readthedocs.org/
.. _Django: https://www.djangoproject.com/
.. _Flask: http://flask.pocoo.org/
.. _Pyramid: http://trypyramid.com/
.. _WSGI: https://www.python.org/dev/peps/pep-0333/
.. _HTTP headers: http://en.wikipedia.org/wiki/List_of_HTTP_header_fields
.. _virtualenv: https://virtualenv.pypa.io/

.. |Server Framework Fit| image:: /static/images/lsbaws-part2/lsbaws_part2_before_wsgi.png
.. |Server Framework Clash| image:: /static/images/lsbaws-part2/lsbaws_part2_after_wsgi.png
.. |WSGI Interface| image:: /static/images/lsbaws-part2/lsbaws_part2_wsgi_idea.png
.. |Mix & Match| image:: /static/images/lsbaws-part2/lsbaws_part2_wsgi_interop.png
.. |Pyramid| image:: /static/images/lsbaws-part2/lsbaws_part2_browser_pyramid.png
.. |Flask| image:: /static/images/lsbaws-part2/lsbaws_part2_browser_flask.png
.. |Django| image:: /static/images/lsbaws-part2/lsbaws_part2_browser_django.png
.. |WSGI Interface Visual| image:: /static/images/lsbaws-part2/lsbaws_part2_wsgi_interface.png
.. |Simple WSGI Application| image:: /static/images/lsbaws-part2/lsbaws_part2_browser_simple_wsgi_app.png
.. |HTTP Response Part 1| image:: /static/images/lsbaws-part2/lsbaws_part2_http_response.png
.. |HTTP Response Part 2| image:: /static/images/lsbaws-part2/lsbaws_part2_http_response_explanation.png
.. |Environ Python Dictionary| image:: /static/images/lsbaws-part2/lsbaws_part2_environ.png
.. |Server Summary| image:: /static/images/lsbaws-part2/lsbaws_part2_server_summary.png