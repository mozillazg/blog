[go]等待 goroutine 结束
=============================

:date: 2014-10-27
:tags: goroutine
:slug: go-wait-all-goroutines-end

默认情况下，程序不会等待 goroutine 结束就退出了。
下面将讲解一种等待所有 goroutine 结束的方法：使用 ``sync.WaitGroup`` 。

.. code-block:: go

    package main

    import (
        "fmt"
        "sync"
    )

    func main() {
        var wg sync.WaitGroup // 定义 WaitGroup
        arr := [3]string{"a", "b", "c"}

        for _, v := range arr {
            wg.Add(1) // 增加一个 wait 任务
            go func(s string) {
                defer wg.Done() // 函数结束时，通知此 wait 任务已经完成
                fmt.Println(s)
            }(v)
        }

        // 等待所有任务完成
        wg.Wait()

    }

在线演示地址：http://play.golang.org/p/fECMMK8Rja


参考资料
--------

* http://stackoverflow.com/questions/18207772/how-to-wait-for-all-goroutines-to-finish-without-using-time-sleep
* http://nathanleclaire.com/blog/2014/02/15/how-to-wait-for-all-goroutines-to-finish-executing-before-continuing/