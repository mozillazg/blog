[python] 解决 SQLAlchemy 提示 Instance is not bound to a Session 错误的问题
==========================================================================================

:slug: python-sqlalchemy-fix-Instance-is-not-bound-to-a-Session-error
:date: 2014-12-22

在使用 SQLAlchemy 的过程中，有时会出现下列错误:

* Parent instance '<User at 0x2b45b53509d0>' is not bound to a Session; lazy load operation of attribute  cannot proceed
* Instance '<User at 0x2b45b53509d0>' is not bound to a Session; attribute refresh operation cannot proceed

出现以上错误的原因是因为：session 已经被提交，导致操作的 model 对象已经不在当前 session 中了。
解决的办法就是：把对象重新加入到当前 session 中:

.. code-block:: python

    def foo(user):
        # do something...
        session.commit()

    user = session.query(User).filter_by(name='Jim').first()
    foo(user)
    print user in session  # False
    print user.name  # DetachedInstanceError: Instance <User at 0x2b45b53509d0> is not bound to a Session

    user = session.merge(user)
    print user in session  # True
    print user.name  # Jim
    session.refresh(user)
    print user.name  # Eric


参考资料
----------

* https://flask-webtest.readthedocs.org/en/latest/#using-flask-webtest-with-flask-sqlalchemy
