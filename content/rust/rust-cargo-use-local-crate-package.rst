Rust: Cargo 使用本地的 crate（本地包代码）
=============================================================================

:slug: rust-cargo-use-local-crate-package
:date: 2017-10-06
:tags: crate, cargo


默认在 Cargo.toml 中指定了包以后，Cargo build 的时候会从 crates.io 上下载远程
的对应包代码。本文将介绍如何在 Cargo.toml 中指定使用本地机器上某个目录下的包，
方便调试本地开发的包或者在没网的环境下开发和调试。


待调用的本地包
--------------------


假设我们要使用的包是 hello, 通过 ``cargo new hello`` 创建：


.. code-block:: console

    $ cargo new hello
     Created library `hello` project

    $ tree hello
    hello
    ├── Cargo.toml
    └── src
        └── lib.rs

    1 directory, 2 files


我们给这个包加一个 ``hi`` 函数:

.. code-block:: rust

    // cat hello/src/lib.rs
    pub fn hi(name: &str) {
        println!("hi {}!", name);
    }


现在我们要在别的地方使用 ``hello`` 这个包，比如调用 ``hello.hi`` 函数，该如何设置呢？


配置使用本地包
---------------


假设我们在 hello 的同级目录有一个 ``demo`` 项目，这个项目将使用 ``hello`` 包里的函数。

先创建这个 ``demo`` 项目::

    $ cargo new demo --bin
     Created binary (application) `demo` project


然后在项目中增加调用代码:

.. code-block:: rust

    // cat demo/src/main.rs
    extern crate hello;

    fn main() {
        hello::hi("mozillazg");
    }

最后关键的一步就是配置 Cargo.toml 使用本地的 ``hello`` 包。

先来看一下当前的目录结构::

    $ tree .
    .
    ├── demo
    │   ├── Cargo.toml
    │   └── src
    │       └── main.rs
    └── hello
        ├── Cargo.toml
        └── src
            └── lib.rs

    4 directories, 4 files


可以看出来， ``hello`` **相对于** ``demo/Cargo.toml`` 的目录位置是 ``../hello`` 。
然后我们配置一下 ``demo/Cargo.toml`` 指定使用这个目录下的 ``hello`` 包::

    [dependencies]
    hello = { path = "../hello" }

在 ``demo`` 项目目录下执行 ``cargo run`` 看看效果::

    # ~/demo
    $ cargo run
       Compiling hello v0.1.0 (file:///Users/mozillazg/hello)
       Compiling demo v0.1.0 (file:///Users/mozillazg/demo)
        Finished dev [unoptimized + debuginfo] target(s) in 0.47 secs
         Running `target/debug/demo`
    hi mozillazg!


可以看到 ``demo`` 确实使用了本地的 ``hello`` 包的代码。👍


P.S. 上面的::

    [dependencies]
    hello = { path = "../hello" }

也可以改为::

    [dependencies.hello]
    path = "../hello"

😁


参考资料
--------

* `Documentation should include exemples of depending on local modules · Issue #640 · rust-lang/cargo <https://github.com/rust-lang/cargo/issues/640>`__
* `Specifying Dependencies <http://doc.crates.io/specifying-dependencies.html#specifying-path-dependencies>`__
