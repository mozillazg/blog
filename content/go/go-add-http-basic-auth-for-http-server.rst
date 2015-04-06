[go] 如何为 HTTP Server 增加 HTTP Basic Auth
====================================================

:date: 2015-04-07
:slug: go-add-http-basic-auth-for-http-server

一句话总结就是：增加一个装饰器函数 ``BasicAuth`` 装饰被保护的函数。

.. code-block:: go

    package main

    import (
        "bytes"
        "encoding/base64"
        "io"
        "log"
        "net/http"
        "strings"
    )

    type ViewFunc func(http.ResponseWriter, *http.Request)

    func BasicAuth(f ViewFunc, user, passwd []byte) ViewFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            basicAuthPrefix := "Basic "

            // 获取 request header
            auth := r.Header.Get("Authorization")
            // 如果是 http basic auth
            if strings.HasPrefix(auth, basicAuthPrefix) {
                // 解码认证信息
                payload, err := base64.StdEncoding.DecodeString(
                    auth[len(basicAuthPrefix):],
                )
                if err == nil {
                    pair := bytes.SplitN(payload, []byte(":"), 2)
                    if len(pair) == 2 && bytes.Equal(pair[0], user) &&
                        bytes.Equal(pair[1], passwd) {
                        // 执行被装饰的函数
                        f(w, r)
                        return
                    }
                }
            }

            // 认证失败，提示 401 Unauthorized
            // Restricted 可以改成其他的值，作用类似于 session ,这样就不会每次访问页面都提示登录
            w.Header().Set("WWW-Authenticate", `Basic realm="Restricted"`)
            // 401 状态码
            w.WriteHeader(http.StatusUnauthorized)
        }
    }

    // 需要被保护的内容
    func HelloServer(w http.ResponseWriter, req *http.Request) {
        io.WriteString(w, "hello, world!\n")
    }

    func main() {
        user := []byte("foo")
        passwd := []byte("bar")

        // 装饰需要保护的 handler
        http.HandleFunc("/hello", BasicAuth(HelloServer, user, passwd))

        log.Println("Listen :8000")
        err := http.ListenAndServe(":8000", nil)
        if err != nil {
            log.Fatal("ListenAndServe: ", err)
        }
    }


效果
--------


未输入用户名和密码的情况下，提示未认证：

.. code-block:: console

     ~$ curl -i http://127.0.0.1:8000/hello
    HTTP/1.1 401 Unauthorized
    Www-Authenticate: Basic realm="Restricted"
    Date: Mon, 06 Apr 2015 11:56:10 GMT
    Content-Length: 0
    Content-Type: text/plain; charset=utf-8

输入用户名和密码，显示被保护的内容：

.. code-block:: console

     ~$ curl -i --user "foo:bar" http://127.0.0.1:8000/hello
    HTTP/1.1 200 OK
    Date: Mon, 06 Apr 2015 11:56:23 GMT
    Content-Length: 14
    Content-Type: text/plain; charset=utf-8

    hello, world!


参考资料
-------------

* https://godoc.org/net/http
* http://tools.ietf.org/html/rfc2617#section-2
* http://stackoverflow.com/questions/12701085/what-is-the-realm-in-basic-authentication
