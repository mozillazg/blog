go-httpheader：将 struct 转换为 http.Header
====================================================

:date: 2017-07-02
:slug: go-intro-go-httpheader

最近在开发 `go-cos <https://github.com/mozillazg/go-cos>`_ 时，
因为 cos API 的很多可选参数都是放在 header 中，
所以开发了一个将 struct 转换为 http.Header 的包。

项目地址： https://github.com/mozillazg/go-httpheader

示例：

.. code-block:: go

    package main

    import (
        "fmt"
        "net/http"

        "github.com/mozillazg/go-httpheader"
    )

    type Options struct {
        hide         string
        ContentType  string `header:"Content-Type"`
        Length       int
        XArray       []string `header:"X-Array"`
        TestHide     string   `header:"-"`
        IgnoreEmpty  string   `header:"X-Empty,omitempty"`
        IgnoreEmptyN string   `header:"X-Empty-N,omitempty"`
        CustomHeader http.Header
    }

    func main() {
        opt := Options{
            hide:         "hide",
            ContentType:  "application/json",
            Length:       2,
            XArray:       []string{"test1", "test2"},
            TestHide:     "hide",
            IgnoreEmptyN: "n",
            CustomHeader: http.Header{
                "X-Test-1": []string{"233"},
                "X-Test-2": []string{"666"},
            },
        }
        h, _ := httpheader.Header(opt)
        // h:
        // http.Header{
        //	"X-Test-1":     []string{"233"},
        //	"X-Test-2":     []string{"666"},
        //	"Content-Type": []string{"application/json"},
        //	"Length":       []string{"2"},
        //	"X-Array":      []string{"test1", "test2"},
        //	"X-Empty-N":    []string{"n"},
        //}
    }


更多信息详见项目文档：https://godoc.org/github.com/mozillazg/go-httpheader

希望能对有同样需求的人有所帮助。
