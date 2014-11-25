[go]比较两个 slice/struct/map 是否相等
=========================================

:date: 2014-11-20
:tags: 
:slug: go-compare-struct-slice-map-is-equal

可以通过 ``reflect.DeepEqual`` 比较两个 slice/struct/map 是否相等:

.. code-block:: go

    package main

    import (
        "fmt"
        "reflect"
    )

    type A struct {
        s string
    }

    func main() {

        a1 := A{s: "abc"}
        a2 := A{s: "abc"}
        if reflect.DeepEqual(a1, a2) {
            fmt.Println(a1, "==", a2)
        }

        b1 := []int{1, 2}
        b2 := []int{1, 2}
        if reflect.DeepEqual(b1, b2) {
            fmt.Println(b1, "==", b2)
        }

        c1 := map[string]int{"a": 1, "b": 2}
        c2 := map[string]int{"a": 1, "b": 2}
        if reflect.DeepEqual(c1, c2) {
            fmt.Println(c1, "==", c2)
        }
    }

在线演示地址： http://play.golang.org/p/SB8LeLNdA8


参考资料
---------

* `go - golang - how to compare struct, slice, map is equal? - Stack Overflow`__

__ http://stackoverflow.com/questions/24534072/golang-how-to-compare-struct-slice-map-is-equal