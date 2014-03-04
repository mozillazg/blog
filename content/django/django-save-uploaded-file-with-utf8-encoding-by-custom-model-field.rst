[django]通过自定义 Model Field 的方式将上传的文本文件按 UTF-8 编码保存
========================================================================

:date: 2014-03-04
:tags: python, django
:slug: django-save-uploaded-file-with-utf8-encoding-by-custom-model-field

默认情况下上传的文件都是按原始编码进行保存的，用户上传什么编码的文件就保存什么编码的文件。

下面将举例说明如何通过自定义 Model Field 的方式将文件的编码改为 UTF-8。

假设有个文件: app/fields.py

.. code-block:: python

    import chardet
    from django.db import models
    from south.modelsinspector import add_introspection_rules

    class UTF8TextFileField(models.FileField):
        """上传的文本文件将按 utf8 编码保存"""

        def clean(self, *args, **kwargs):
            uploaded_file = super(UTF8TextFileField, self).clean(*args, **kwargs)
            content_raw = uploaded_file.file.read()
            # 猜测原始文件编码
            encoding = chardet.detect(content_raw)['encoding'] or 'utf8'
            # 解码并按 utf8 编码，忽略不能编/解码的字符
            content_utf8 = content_raw.decode(encoding, 'ignore'
                                              ).encode('utf8', 'ignore')
            # 将编码后的内容写回文件
            uploaded_file.close()
            uploaded_file.open('wb')
            uploaded_file.file.write(content_utf8)
            uploaded_file.close()
            uploaded_file.open(uploaded_file.mode)

            return uploaded_file

    # 告诉 South 我们定义了一个 Model Field
    # 如果不用 South 可以去掉这句
    add_introspection_rules([], ["^app\.fields\.UTF8TextFileField"])

参照这个 ``UTF8TextFileField`` ，也可以自定义一个可以按指定编码保存文件的 ``TextFileField`` ，这个可以随便发挥，我只是举个简单的例子。

如何使用这个 ``UTF8TextFileField`` 呢，与 ``FileField`` 的使用方式是一样的 ::

    from django.db import models

    from app.fields import UTF8TextFileField


    class Foo(models.Model):
        txt = UTF8TextFileField(u'文本文件')


参考资料
---------

* `django/django/core/files/base.py at master · django/django · GitHub <https://github.com/django/django/blob/master/django/core/files/base.py>`__
* `Part 4: Custom Fields — South 0.8.4 documentation <http://south.readthedocs.org/en/latest/tutorial/part4.html#part-4-custom-fields>`__
* `File Uploads | Django documentation | Django <https://docs.djangoproject.com/en/dev/topics/http/file-uploads/>`__
* `Model field reference | Django documentation | Django <https://docs.djangoproject.com/en/dev/ref/models/fields/#filefield>`__
