title: 基于 Python 3 新增的函数注解（Function Annotations ）语法实现参数类型检查功能
slug: python-function-argument-type-check-base-on-function-annotations
date: 2016-01-06
tags: python 3, Function Annotations


## 函数注解（Function Annotations）

[函数注解语法](https://www.python.org/dev/peps/pep-3107/) 可以让你在定义函数的时候对参数和返回值添加注解：

    def foobar(a: int, b: "it's b", c: str = 5) -> tuple:
        return a, b, c

* `a: int` 这种是注解参数
* `c: str = 5` 是关键字参数的注解
* `-> tuple` 是注解返回值。

注解的内容既可以是个类型也可以是个字符串，甚至表达式：

    def foobar(a: 1+1) -> 2 * 2:
        return a

那么如何获取我们定义的函数注解呢？至少有两种办法：

* `__annotations__`:
    
        >>> foobar.__annotations__
        {'a': int, 'b': "it's b", 'c': str, 'return': tuple}
    
* `inspect.signature`:
    
        >>> import inspect
        >>> sig = inspect.signature(foobar)
        >>> # 获取函数参数
        >>> sig.paraments
        mappingproxy(OrderedDict([('a', <Parameter "a:int">), ('b', <Parameter "b:"it's b"">), ('c', <Parameter "c:str=5">)]))
        >>> # 获取函数参数注解
        >>> for k, v in sig.parameters.items():
                print('{k}: {a!r}'.format(k=k, a=v.annotation))     
        a: <class 'int'>
        b: "it's b"
        c: <class 'str'>
        >>> # 返回值注解
        >> sig.return_annotation
        tuple

既然可以得到函数中定义的注解，那么我们就可以用它进行参数类型检查了。

## 类型检查

Python 解释器并不会基于函数注解来自动进行类型检查，需要我们自己去实现类型检查功能：

    >>> foobar.__annotations__
    {'a': int, 'b': "it's b", 'c': str, 'return': tuple}

    >>> foobar(a='a', b=2, c=3)
    ('a', 2, 3)
 
既然通过 `inspect.signature` 我们可以获取函数定义的参数的顺序以及函数注解，
那么我们就可以通过定义一个装饰器来检查传入函数的参数的类型是否跟函数注解相符，
这里实现的装饰器函数（check_type.py）如下：

    # coding: utf8
    import collections
    import functools
    import inspect


    def check(func):
        msg = ('Expected type {expected!r} for argument {argument}, '
               'but got type {got!r} with value {value!r}')
        # 获取函数定义的参数
        sig = inspect.signature(func)
        parameters = sig.parameters          # 参数有序字典
        arg_keys = tuple(parameters.keys())   # 参数名称

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            CheckItem = collections.namedtuple('CheckItem', ('anno', 'arg_name', 'value'))
            check_list = []

            # collection args   *args 传入的参数以及对应的函数参数注解
            for i, value in enumerate(args):
                arg_name = arg_keys[i]
                anno = parameters[arg_name].annotation
                check_list.append(CheckItem(anno, arg_name, value))
                
            # collection kwargs  **kwargs 传入的参数以及对应的函数参数注解
            for arg_name, value in kwargs.items():
               anno = parameters[arg_name].annotation
               check_list.append(CheckItem(anno, arg_name, value))
               
            # check type
            for item in check_list:
                if not isinstance(item.value, item.anno):
                    error = msg.format(expected=item.anno, argument=item.arg_name,
                                       got=type(item.value), value=item.value)
                    raise TypeError(error)

            return func(*args, **kwargs)

        return wrapper

下面来测试一下我们的装饰器:

    @check
    def foobar(a: int, b: str, c: float = 3.2) -> tuple:
        return a, b, c

顺序传参测试:

    >>> foobar(1, 'b')
    (1, 'b', 3.2)

    >>> foobar(1, 'b', 3.5)
    (1, 'b', 3.5)

    >>> foobar(1, 2)
    ...
    TypeError: Expected type <class 'str'> for argument b, but got type <class 'int'> with value 2
    
    >>> foobar(1, 'b', 3)
    ...
    TypeError: Expected type <class 'float'> for argument c, but got type <class 'int'> with value 

关键字传参:

    >>> foobar(b='b', a=2)
    (2, 'b', 3.2)
    >>> foobar(b='b', a=2, c=3.5)
    (2, 'b', 3.5)

    >>>foobar(a='foo', b='bar')
    ...
    TypeError: Expected type <class 'int'> for argument a, but got type <class 'str'> with value 'foo'
    
    >>> foobar(a=2, b='bar', c=3)
    ...
    TypeError: Expected type <class 'float'> for argument c, but got type <class 'int'> with value 
    

借助于 Function Annotations 一个简单的参数类型检查的装饰器就这样实现了。


## 参考资料

* [PEP 3107 -- Function Annotations | Python.org](https://www.python.org/dev/peps/pep-3107/)