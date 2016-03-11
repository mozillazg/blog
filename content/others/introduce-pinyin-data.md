title: pinyin-data: 汉字拼音数据库
slug: introduce-pinyin-data
date: 2016-03-07
tags: pinyin

## 缘起

<!-- 因为我维护了三个拼音相关的仓库（
[python-pinyin][1]
[go-pinyin][2]
[rust-pinyin][3]
），每次修改拼音数据的时候都需要手动修改不同编程语言版本的
拼音库，感觉这样不是很方便。

同时也  -->

希望建立一个跟编程语言无关的拼音数据库，
方便大家使用这个拼音数据库去开发不同编程语言的拼音模块。


## 项目介绍

项目地址: <https://github.com/mozillazg/pinyin-data>

主要用的是 [Unicode.org](http://unicode.org/) 旗下的 [Unihan Database](http://www.unicode.org/charts/unihan.html) 项目里的拼音数据。
通过程序自动解析和合并 [Unihan Database](http://www.unicode.org/charts/unihan.html) 中的拼音数据。

**数据介绍**

数据格式：`{code point}: {pinyins}  # {hanzi}` （示例：`U+4E2D: zhōng,zhòng  # 中`）

* `kHanyuPinyin.txt`: [Unihan Database](http://www.unicode.org/charts/unihan.html) 中 [kHanyuPinyin](http://www.unicode.org/reports/tr38/#kHanyuPinyin) 部分的拼音数据（来源于《漢語大字典》的拼音数据）
* `kHanyuPinlu.txt`: [Unihan Database](http://www.unicode.org/charts/unihan.html) 中 [kHanyuPinlu](http://www.unicode.org/reports/tr38/#kHanyuPinlu) 部分的拼音数据（来源于《現代漢語頻率詞典》的拼音数据）
* `kXHC1983.txt`: [Unihan Database](http://www.unicode.org/charts/unihan.html) 中 [kXHC1983](http://www.unicode.org/reports/tr38/#kXHC1983) 部分的拼音数据（来源于《现代汉语词典》的拼音数据）
* `nonCJKUI.txt`: 不属于 [CJK Unified Ideograph](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs) 但是却有拼音的字符
* `kMandarin.txt`: [Unihan Database](http://www.unicode.org/charts/unihan.html) 中 [kMandarin](http://www.unicode.org/reports/tr38/#kMandarin) 部分的拼音数据（普通话中最常用的一个读音。zh-CN 为主，如果 zh-CN 中没有则使用 zh-TW 中的拼音）
* `overwrite.txt`: 手工校验的拼音数据（上面的拼音数据都是自动生成的，修改的话只修改这个就可以了）
* `pinyin.txt`: 合并上述文件后的拼音数据
* `zdic.txt`: [汉典网](http://zdic.net) 的拼音数据

## 后续计划

* 将 [python-pinyin][1], [go-pinyin][2], [rust-pinyin][3] 里的拼音数据改为基于 [pinyin-data][4] 自动生成相关代码。
  然后统一在 [pinyin-data][3] 这个项目中维护拼音数据（在 README 或 CONTRIBUTING.md 中增加提示）。
* 向 [hotoo/pinyin](https://github.com/hotoo/pinyin) 提一下这个仓库，看他是否有意使用这个仓库的数据。

[1]: https://github.com/mozillazg/python-pinyin
[2]: https://github.com/mozillazg/go-pinyin
[3]: https://github.com/mozillazg/rust-pinyin
[4]: https://github.com/mozillazg/pinyin-data
