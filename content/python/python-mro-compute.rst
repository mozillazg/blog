Python: 多继承模式下 MRO(Method Resolution Order) 的计算方式
================================================================

:slug: python-mro-compute
:date: 2016-11-06


大家可能已经知道了，在 Python 3(Python 2 的新式类)中多继承模式是使用 C3 算法来确定 MRO(Method Resolution Order) 的。

那么具体是怎么计算的呢？本文将基于 https://www.python.org/download/releases/2.3/mro/ 中的几个例子来讲解 MRO 是怎么计算的。


我们首先来定义一些符号： ::

    用 CN 表示一个类：C1, C2, C3, ..., CN
    C1 C2 C3 ... CN 表示的是一个包含多个类的列表 [C1, C2, C3, ..., CN]

其中： ::

    head = C1
    tail = C2 ... CN


加法运算: ::


    C + (C1 C2 ... CN) = C C1 C2 ... CN
    [C] + [C1, C2, ... ,CN] = [C, C1, C2, ..., CN]


L[C] 表示类 C 的线性值，其实就是 C 的 MRO, 其中 ::

    L[object] = object

比如有个类 : ::

    class C(B1, B2, ..., BN): pass

那么: ::

   L[C(B1 ... BN)] = C + merge(L[B1] ... L[BN], B1 ... BN)

merge 的计算规则如下：


    1. take the head of the first list, i.e L[B1][0];
    2. if this head is not in the tail of any of the other lists, then add it to the linearization of C and remove it from the lists in the merge, otherwise look at the head of the next list and take it, if it is a good head.
    3. Then repeat the operation until all the class are removed or it is impossible to find good heads. In this case, it is impossible to construct the merge, Python 2.3 will refuse to create the class C and will raise an exception.


计算 MRO
~~~~~~~~~~~

先从简单的类说起： ::

    class B(object): pass

    L[B] = L[B(object)]
         = B + merge(L[object])
         = B + L[object]
         = B object

    >>> B.mro()
    [<class '__main__.B'>, <type 'object'>]


简单的子类: ::

    class C(B): pass

    L[C] = L[C(B)]
         = C + merge(L[B])
         = C + L[B]
         = C B object     # 从上面已经知道了 L[B] = B object

    >>> C.mro()
    [<class '__main__.C'>, <class '__main__.B'>, <type 'object'>]


下面来看一个复杂的例子: ::

    >>> O = object
    >>> class F(O): pass
    >>> class E(O): pass
    >>> class D(O): pass
    >>> class C(D,F): pass
    >>> class B(D,E): pass
    >>> class A(B,C): pass

很容易就可以想到: ::


    L[O] = O = object
    L[F] = L[F(O)] = F  O
    L[E] = L[E(O)] = E  O
    L[D] = L[D(O)] = D  O


下面来计算 C, B, A:

``L[C]``: ::

    L[C] = L[C(D, F)]
         = C + merge(L[D], L[F], DF)
         # 从前面可知 L[D] 和 L[F] 的结果
         = C +  merge(DO, FO, DF)
         # 因为 D 是顺序第一个并且在几个包含 D 的 list 中是 head，
         # 所以这一次取 D 同时从列表中删除 D
         = C + D + merge(O, FO, F)
         # 因为 O 虽然是顺序第一个但在其他 list (FO)中不是 head, 跳过,
         # 改为检查第二个list FO # F 是第二个 list 和其他 list 的 head, 
         # 取 F同时从列表中删除 F
         = C + D + F + merge(O)
         = C D F O

    >>> C.mro()
    [<class '__main__.C'>, <class '__main__.D'>, <class '__main__.F'>, <type 'object'>]

``L[B]``: ::

    L[B] = L[B(D, E)]
         = B + merge(L[D], L[E], DE)
         = B + merge(DO, EO, DE)
         = B + D + merge(O, EO, E)
         = B + D + E + merge(O)
         = B D E O

    >>> B.mro()
    [<class '__main__.B'>, <class '__main__.D'>, <class '__main__.E'>, <type 'object'>]

``L[A]``: ::

    L[A] = L[A(B, C)]
         = A + merge(L(B), L(C), BC)
         = A + merge(BDEO, CDFO, BC)
         = A + B + merge(DEO, CDFO, C)
         # 注意这里是 C , 因为第一个list 的 head D 不是其他list 的 head
         # 所以改为从下一个 list CDFO 开始
         = A + B + C + merge(DEO, DFO)
         = A + B + C + D + merge(EO, FO)
         = A + B + C  + D + E + merge(O, FO)
         = A + B + C + D + E + F + merge(O)
         = A B C D E F O

    >>> A.mro()
    [<class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>,
     <class '__main__.D'>, <class '__main__.E'>, <class '__main__.F'>, <type 'object'>]


到这里应该已经有一点眉目了。下面再来个上面那些类的变种，可以先自己算算看，后面有详细的计算过程。

::

    >>> O = object
    >>> class F(O): pass
    >>> class E(O): pass
    >>> class D(O): pass
    >>> class C(D,F): pass
    >>> class B(E,D): pass
    >>> class A(B,C): pass

跟之前唯一的区别是 ``B(D, E)`` 变成了 ``B(E, D)`` ::


    L[O] = O = object
    L[F(O)] = F  O
    L[E(O)] = E  O
    L[D(O)] = D  O

    L[C] = L[C(D, F)]
         = C + merge(L[D], L[F], DF)
         = C D F O

    L[B] = L[B(E, D)]
         = B + merge(L[E], L[D], ED)
         = B + merge(EO, DO, ED)
         = B + E + merge(O, DO, D)
         = B + E + D + merge(O)
         = B E D O
    >>> B.mro()
    [<class '__main__.B'>, <class '__main__.E'>, <class '__main__.D'>, <type 'object'>]

    L[A] = L[A(B, C)]
         = A + merge(L[B], L[C], BC)
         = A + merge(BEDO, CDFO, BC)
         = A + B + merge(EDO, CDFO, C)
         = A + B + E + merge(DO, CDFO, C)
         = A + B + E + C + merge(DO, DFO)
         = A + B + E + C + D + merge(O, FO)
         = A + B + E + C + D + F + merge(O)
         = A B E C D F O
    >>> A.mro()
    [<class '__main__.A'>, <class '__main__.B'>, <class '__main__.E'>,
     <class '__main__.C'>, <class '__main__.D'>, <class '__main__.F'>, <type 'object'>]

通过这几个例子应该对如何计算 MRO 已经有所了解了，更详细的信息可以阅读 `python MRO 文档 <https://www.python.org/download/releases/2.3/mro/>`__
以及 wikipedia 中的 `C3 算法 <https://en.wikipedia.org/wiki/C3_linearization>`__.


参考资料
~~~~~~~~~~~

* `The Python 2.3 Method Resolution Order | Python.org <https://www.python.org/download/releases/2.3/mro/>`__
* `C3 linearization - Wikipedia <https://en.wikipedia.org/wiki/C3_linearization>`__
