在 python 中使用 str.strip 方法时需要注意的地方
======================================================

:slug: python-str-strip-lstrip-rstrip-warnning
:date: 2015-06-08

首先问大家一个问题：你觉得下面代码的输出会是什么？ ::

    print '12345-abc-12345-defg-54321'.strip('12345')

我猜有些同学的答案会是: ``-abc-12345-defg-54321`` ，实际的结果是: ::

    >>> print '12345-abc-12345-defg-54321'.strip('12345')
    -abc-12345-defg-

为什么不是 ``-abc-12345-defg-54321`` 呢？我们先来看一下 ``str.strip`` 的文档就知道了: ::

    S.strip([chars]) -> string or unicode

    Return a copy of the string S with leading and trailing
    whitespace removed.
    If chars is given and not None, remove characters in chars instead.
    If chars is unicode, S will be converted to unicode before stripping

通过文档我们可以知道:

* 如果未指定 chars 参数或参数值未 None, 去除字符串 **首尾空白符（空格、换行符等等）**
* 否则，只要 **首尾字符包含在 chars 定义的字符串内** ，就会被去除。并且会递归调用直到首尾字符不在 chars 内。类似: ::

        def _strip(s, chars):
            if s[0] in chars:
                return _strip(s[1:], chars)
            elif s[-1] in chars:
                return _strip(s[:-1], chars)
            else:
                return s

更多的例子: ::

    >>> '18349-13-3434'.strip('0123456789')
    '-13-'

    >>> '18349-13-3434'.strip('123')
    '8349-13-3434'

    >>> 'scene_scdefg'.strip('scene_')
    'defg'

    >>> '\r   \t\n '.strip()
    ''

现在我们知道 ``str.strip`` 是按 **字符** 进行移除操作的。
那么如何按字符串进行移除呢？

一种解决办法就是使用 ``re.sub``: ::

    def strip2(s, chars):
        re_chars = re.escape(chars)
        s = re.sub(r'^(?:%s)+(?P<right>.*)$' % re_chars, '\g<right>', s)
        s = re.sub(r'^(?P<left>.*?)(?:%s)+$' % re_chars, '\g<left>', s)
        return s

    >>> print strip2('12345-abc-12345-defg-54321', '12345')
    -abc-12345-defg-54321

.. 一种解决办法就是，使用 ``str.replace``: ::
..
..     >>> '12345-abc-12345-defg-54321'.replace('12345', '', 1)
..     '-abc-12345-defg-54321'
