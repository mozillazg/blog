Title: 给终端文字加点颜色和特效
Date: 2013-08-25
Tags: ansi, color, terminal
Slug: ansi-escape-sequences

这个叫做：ANSI Escape Sequences/Code 。

文字特效相关的字符格式是：`ESC[#;#;....;#m` ，其中 # 的取值见下表：

| # 的值   |   功能    |
|----------|-----------|
| 00 或 0  |  正常显示 |
| 01 或 1  |  粗体     |
| 02 或 2  |  模糊     |
| 03 或 3  |  斜体     |
| 04 或 4  |  下划线     |
| 05 或 5  |  闪烁（慢） |
| 06 或 6  |  闪烁（快） |
| 07 或 7  |  反转显示（前景色与背景色调过来）     |
| 08 或 8  |  隐藏     |
| 22       |  正常       |
| 23       |  不斜体 |
| 24       |  无下划线  |
| 25       |  不闪烁    |
| 27       |  不反转    |
| 28       |  不隐藏    |
|                       |
|     前景色        |
| 30       |  黑色  |
| 31       |  红色  |
| 32       |  绿色  |
| 33       |  黄色  |
| 34       |  蓝色  |
| 35       |  品红/紫红 |
| 36       |  青色/蓝绿 |
| 37       |  白色  |
| 38       |  xterm-256 色  |
| 39       |  默认色 |
|
|    背景色         |
| 40       | 黑色   |
| 41       |  红色  |
| 42       |  绿色  |
| 43       |  黄色  |
| 44       |  蓝色  |
| 45       |  品红/紫红 |
| 46       |  青色/蓝绿 |
| 47       |  白色  |
| 48       |  xterm-256 色  |
| 49       |  默认色 |

<!--
https://github.com/robertknight/konsole/blob/master/tests/color-spaces.pl
Quoting <https://github.com/robertknight/konsole/blob/master/user-doc/README.moreColors>:
   ESC[ … 38;2;<r>;<g>;<b> … m Select RGB foreground color
   ESC[ … 48;2;<r>;<g>;<b> … m Select RGB background color

## 示例

print('\033[31m \033[44m' + 'some red text' + '\033[0;39m' + 'ab')
-->

## 参考

* [ANSI Escape Sequences](http://www.isthe.com/chongo/tech/comp/ansi_escapes.html)
* [ANSI escape code - Wikipedia, the free encyclopedia](http://en.wikipedia.org/wiki/ANSI_escape_code)
* [Terminal colour highlights](http://www.pixelbeat.org/docs/terminal_colours/)
