title:[django]修复使用 QueryDict 时出现 “UnicodeEncodeError” 错误的问题
slug: django-fix-QueryDict-raise-UnicodeEncodeError
date: 2015-03-17

当给 QueryDict 传入一个 unicode 字符串的时候会出现 “UnicodeEncoderError” 错误：

    In [1]: from django.http.request import QueryDict

    In [2]: s = u'a=%E4%BD%A0%E5%A5%BD'
    In [3]: QueryDict(s)
    ---------------------------------------------------------------------------
    UnicodeEncodeError                        Traceback (most recent call last)
    <ipython-input-10-e865795305d5> in <module>()
    ----> 1 QueryDict(s)

    /.../django/http/request.pyc in __init__(self, query_string, mutable, encoding)
        328                                         keep_blank_values=True):
        329                 try:
    --> 330                     value = value.decode(encoding)
        331                 except UnicodeDecodeError:
        332                     value = value.decode('iso-8859-1')

    /.../encodings/utf_8.pyc in decode(input, errors)
         14 
         15 def decode(input, errors='strict'):
    ---> 16     return codecs.utf_8_decode(input, errors, True)
         17 
         18 class IncrementalEncoder(codecs.IncrementalEncoder):

    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-5: ordinal not in range(128)

从异常信息中我们可以发现，出现异常时因为 request.py 中尝试执行 `decode` 操作，
但是我们传递的是一个 unicode 编码的字符串所以就报错了。传递一个 str 字符串就可以了。

    In [4]: s
    Out[4]: u'a=%E4%BD%A0%E5%A5%BD'

    In [5]: QueryDict(s.encode('utf8'))
    Out[5]: <QueryDict: {u'a': [u'\u4f60\u597d']}>