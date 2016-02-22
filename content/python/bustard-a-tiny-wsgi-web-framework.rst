[python]bustard: 一个玩具式的 web 框架
=================================================
:slug: bustard-a-tiny-wsgi-web-framework
:date: 2016-02-22
:tags: wsgi, framework, orm, template, router

最近一直在填一个玩具式（仅供学习交流，不可用于生产环境）的 WEB 框架的坑，现在大部分功能都已经完成的差不多了， 所以写篇博文介绍一下这个框架。

| 项目地址： https://github.com/mozillazg/bustard
| 安装： ``pip install bustard``

包含的功能：

* `路由 <https://github.com/mozillazg/bustard/blob/master/bustard/router.py>`__
* `Request 和 Response <https://github.com/mozillazg/bustard/blob/master/bustard/http.py>`__
* `Cookies <https://github.com/mozillazg/bustard/blob/master/bustard/http.py>`__ 和 `Session <https://github.com/mozillazg/bustard/blob/master/bustard/sessions.py>`__
* `ORM <https://github.com/mozillazg/bustard/blob/master/bustard/orm.py>`__
* `模版 <https://github.com/mozillazg/bustard/blob/master/bustard/template.py>`__
* `WSGI server <https://github.com/mozillazg/bustard/blob/master/bustard/servers.py>`__

依赖:

* Python 3.5
* psycopg2


Hello World
----------------

`bustard`_ 参考了 `Flask`_ 和 `Django`_ 的设计，路由风格跟 `Flask`_
类似采用装饰器风格，view 方式风格跟 `Django`_ 类似采用显示传入 ``request``
的方式。 ::

	from bustard.app import Bustard
    
	app = Bustard()
    
    
	@app.route('/')
	def helloword(request):
		return 'Hello World!'
    
	if __name__ == '__main__':
		app.run()


路由
----------

支持以下三种方式的路由:

* 静态路由 ::

        @app.route('/hello')
        def hello(request):
            return 'hello'

* 类似 `Flask`_ 的动态路由(``<name>``) ::

        @app.route('/hello/<name>')
        def hello(request, name):
            return 'hello {}'.format(name)

* 类似 `Django`_ 的动态路由(正则表达式) ::

    @app.route('/hello/(?P<name>\w+)')
    def hello(request, name):
        return 'hello {}'.format(name)

``app.route`` 支持一个可选参数 ``methods`` 用于指定支持的 http method: ::

    @app.route('/', methods=['GET',' POST'])
    def hello(request):
        return 'hello'


Request
----------

``request`` 对象跟 `Flask`_ 里的 ``request`` 对象类似，常用的方法和属性如下:

* ``request.headers``: url 参数
* ``request.args``: url 参数
* ``request.form``: POST 表单数据（不包含文件）
* ``request.files``: POST 表单里的文件数据
* ``request.data``: POST body
* ``request.cookies``: Cookies


Response
------------

::

    response = Response(b'data', status_code=200, content_type='text/html',
                        headers={'X-Total': 23})

``response`` 对象常用的方法和属性如下:

* ``response.status_code``
* ``response.content_type``
* ``response.headers``
* ``response.content``
* ``response.set_cookie(...)``
* ``response.delete_cookie(...)``


Session
-------------

访问 ``request.session`` 来获取 ``session`` 数据，它是一个类 ``dict`` 对象`:  ::

    user_id = request.session['user_id']
    request.session['name'] = 'Tom'


ORM
------

``ORM`` 只支持 `postgresql`_ 数据库，用法类似 `Django`_ ORM 和 `SQLAlchemy`_ 的结合体: ::

    from bustard.orm import (
        Model, Engine, Session, AutoField, CharField, BooleanField
    )

    class User(Model):
        __tablename__ = 'users'

        id = AutoField(primary_key=True)
        username = CharField(max_length=80, index=True)
        password = CharField(max_length=200, default='')
        is_actived = orm.BooleanField(default=False, server_default=False)

    engine = Engine('postgresql://dbuser:password@localhost/exampledb')
    session = Session(engine)

新增: ::

    user = User(username='tom', is_actived=False)
    session.insert(user)
    session.commit()

查询: ::

    session.query(User).filter(User.id > 10)
    session.query(User).filter(id=10)
    session.query(User).filter(User.id > 10).order_by(User.is_actived)
    session.query(User).filter(User.id > 10).limit(3).offset(1)

更新: ::

    session.query(User).filter(User.id > 10).update(is_actived=True)
    session.commit()

    user.is_actived = True
    session.update(user)
    session.commit()

删除: ::

    session.query(User).filter(User.id > 10).delete()
    session.commit()

    session.delete(user)
    session.commit()


模版
-------

模版语法类似 `Jinja2`_ : ::

    {% for user in users %}
        {{ user.name }}
        {% if user.is_actived %}
            is_actived
        {% endif %}
    {% endfor %}


更多使用示例详见 `examples`_


.. _WSGI: https://www.python.org/dev/peps/pep-3333/
.. _Flask: https://github.com/mitsuhiko/flask
.. _Django: https://github.com/django/django
.. _postgresql: http://www.postgresql.org/docs/9.5/static/index.html
.. _SQLAlchemy: https://bitbucket.org/zzzeek/sqlalchemy/
.. _Jinja2: http://jinja.pocoo.org
.. _bustard: https://github.com/mozillazg/bustard
.. _examples: https://github.com/mozillazg/bustard/tree/master/examples
