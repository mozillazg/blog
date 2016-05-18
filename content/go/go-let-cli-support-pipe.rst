[go]如何让命令行程序支持管道和重定向输入
==================================================
:slug: go-let-cli-support-pipe-read-data-from-stdin
:date: 2016-03-12

管道和重定向输入的数据都是通过标准输入传入程序的， ``os.Stdin`` 即为标准输入。

可以通过 ``golang.org/x/crypto/ssh/terminal`` 的 ``terminal.IsTerminal(0)``
判断是否是管道和重定向输入，为什么是 ``0`` ：因为标准输入的文件描述符是 ``0``

* 为 ``true`` 时表示是交互式环境
* 为 ``false`` 时是我们要的场景

首先需要安装 ``golang.org/x/crypto/ssh/terminal`` 这个包（安装时需要 VPN 的辅助）::

    go get golang.org/x/crypto/ssh/terminal

也可以使用 ``github.com/mattn/go-isatty`` 这个包::

    !isatty.IsTerminal(os.Stdin.Fd())


下面是示例代码:

.. code-block:: go

    package main
    
    import (
    	"flag"
    	"fmt"
    	"io/ioutil"
    	"os"
    	"strings"
    
    	"golang.org/x/crypto/ssh/terminal"
    )
    
    func main() {
    	flag.Parse()
    	data := flag.Args()
    	if !terminal.IsTerminal(0) {
    		b, err := ioutil.ReadAll(os.Stdin)
    		if err == nil {
    			data = append(data, string(b))
    		}
    	}
    	fmt.Println(strings.Join(data, " "))
    }


测试效果:

.. code-block:: shell

    $ echo "hello" > hello.txt
    $ go run main.go hello world       # 参数输入
    hello world
    $ cat hello.txt | go run main.go   # 管道输入
    hello

    $ go run main.go < hello.txt       # 重定向输入
    hello

    $


参考资料
------------

* `terminal - GoDoc <https://godoc.org/golang.org/x/crypto/ssh/terminal>`__
* `os - GoDoc <https://godoc.org/os>`__
* `ioutil - GoDoc <https://godoc.org/io/ioutil>`__
