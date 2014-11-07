[flask]调整 Flask-RESTful 中 reqparse.RequestParser 对 None 值的处理
===========================================================================

:date: 2014-11-04
:tags: Flask-RESTful
:slug: flask-restful-reqparse-handle-none-value

默认情况下，``reqparse.RequestParser`` 对 ``None`` 的处理结果是：
就算你定义了 ``required=True``，它仍旧会接受客户端提交的 ``None`` 不会返回 400 错误码。

这往往违背了我们的初衷：一般对于 ``required=True`` 的字段，我们希望在它的值为 ``None`` 的时候能够返回 400 错误码，提示该字段不能为 ``None``，
因为 ``None`` 值可能会在保存数据的时候引起数据库抛出 ``NOT NULL`` 错误。

可以通过定义一个 ``argument_class`` 来改变 ``reqparse.RequestParser`` 的默认行为:

.. code-block:: python

   from flask.ext.restful import reqparse


   class Argument(reqparse.Argument):
       """
       继承自 reqparse.Argument, 增加 nullable 关键字参数，
       对于值为 None 并且 nullable=False 的字段 raise TypeError
       """
       def __init__(self, name, default=None, dest=None, required=False,
                    ignore=False, type=reqparse.text_type,
                    location=('json', 'values',), choices=(),
                    action='store', help=None, operators=('=',),
                    case_sensitive=True, nullable=False):
           self.nullable = nullable
           super(Argument, self).__init__(name, default=default, dest=dest,
                                          required=required, ignore=ignore,
                                          type=type, location=location,
                                          choices=choices, action=action,
                                          help=help, operators=operators,
                                          case_sensitive=case_sensitive)

       def convert(self, value, op):
           if value is None and not self.nullable:
               raise TypeError("%s can't be null" % self.name)
           return super(Argument, self).convert(value, op)

用法:

.. code-block:: python

   reqparse = reqparse.RequestParser(argument_class=Argument)
   reqparse.add_argument('name', type=unicode, required=True)
   reqparse.add_argument('description', type=unicode, required=False, nullable=True)


参考资料
-------------------

* `flask-restful/reqparse.py at master · twilio/flask-restful`__

__ https://github.com/twilio/flask-restful/blob/master/flask_restful/reqparse.py
