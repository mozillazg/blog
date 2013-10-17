Title: 给终端文字加点颜色和特效
Date: 2013-08-25
Tags: ansi, color, terminal
Slug: ansi-escape-sequences

这个叫做：ANSI Escape Sequences/Code 。

文字特效相关的字符格式是：`ESC[#;#;....;#m` ，其中 # 的取值见下表：

| # 的值   |   功能    |    python 代码                           |  截图 |
|----------|-----------|------------------------------------------|-------|
| 00 或 0  |  正常显示 |`'\033[00m' + 'hello' + '\033[0;39m'`     | 
| 01 或 1  |  粗体     |`'\033[01m' + 'hello' + '\033[0;39m'`     | 
| 02 或 2  |  模糊     |`'\033[02m' + 'hello' + '\033[0;39m'`     | 
| 03 或 3  |  斜体     |`'\033[03m' + 'hello' + '\033[0;39m'`     | 
| 04 或 4  |  下划线     |`'\033[04m' + 'hello' + '\033[0;39m'`   | 
| 05 或 5  |  闪烁（慢） |`'\033[05m' + 'hello' + '\033[0;39m'`   | 
| 06 或 6  |  闪烁（快） |`'\033[06m' + 'hello' + '\033[0;39m'`   | 
| 07 或 7  |  反转显示（前景色与背景色调过来）     |`'\033[07m' + 'hello' + '\033[0;39m'`   | 
| 08 或 8  |  隐藏     |`'\033[08m' + 'hello' + '\033[0;39m'`   | 
| 22       |  正常       |`'\033[22m' + 'hello' + '\033[0;39m'`   | 
| 23       |  不斜体 |`'\033[23m' + 'hello' + '\033[0;39m'`   | 
| 24       |  无下划线  |`'\033[24m' + 'hello' + '\033[0;39m'`   | 
| 25       |  不闪烁    |`'\033[25m' + 'hello' + '\033[0;39m'`   | 
| 27       |  不反转    |`'\033[26m' + 'hello' + '\033[0;39m'`   | 
| 28       |  不隐藏    |`'\033[27m' + 'hello' + '\033[0;39m'`   | 
|                       |
|     前景色        |
| 30       |  黑色  |`'\033[30m' + 'hello' + '\033[0;39m'`   | 
| 31       |  红色  |`'\033[31m' + 'hello' + '\033[0;39m'`   | 
| 32       |  绿色  |`'\033[32m' + 'hello' + '\033[0;39m'`   | 
| 33       |  黄色  |`'\033[33m' + 'hello' + '\033[0;39m'`   | 
| 34       |  蓝色  |`'\033[34m' + 'hello' + '\033[0;39m'`   | 
| 35       |  品红/紫红 |`'\033[35m' + 'hello' + '\033[0;39m'`   | 
| 36       |  青色/蓝绿 |`'\033[36m' + 'hello' + '\033[0;39m'`   | 
| 37       |  白色  |`'\033[37m' + 'hello' + '\033[0;39m'`   | 
| 38       |  xterm-256 色  |`'\033[38;5;7m' + 'hello' + '\033[0;39m'`  |  
| 39       |  默认色 |`'\033[39m' + 'hello' + '\033[0;39m'`   | 
|
|    背景色         |
| 40       | 黑色   |`'\033[40m' + 'hello' + '\033[0;39m'`   | 
| 41       |  红色  |`'\033[41m' + 'hello' + '\033[0;39m'`   | 
| 42       |  绿色  |`'\033[42m' + 'hello' + '\033[0;39m'`   | 
| 43       |  黄色  |`'\033[43m' + 'hello' + '\033[0;39m'`   | 
| 44       |  蓝色  |`'\033[44m' + 'hello' + '\033[0;39m'`   | 
| 45       |  品红/紫红 |`'\033[45m' + 'hello' + '\033[0;39m'`   | 
| 46       |  青色/蓝绿 |`'\033[46m' + 'hello' + '\033[0;39m'`   | 
| 47       |  白色  |`'\033[47m' + 'hello' + '\033[0;39m'`   | 
| 48       |  xterm-256 色  |`'\033[48;5;7m' + 'hello' + '\033[0;39m'`  | 
| 49       |  默认色 |`'\033[49m' + 'hello' + '\033[0;39m'`   | 

<!--
https://github.com/robertknight/konsole/blob/master/tests/color-spaces.pl
Quoting <https://github.com/robertknight/konsole/blob/master/user-doc/README.moreColors>:
   ESC[ … 38;2;<r>;<g>;<b> … m Select RGB foreground color
   ESC[ … 48;2;<r>;<g>;<b> … m Select RGB background color

## 示例

print('\033[31m \033[44m' + 'some red text' + '\033[0;39m' + 'ab')
-->

`'\033[47;31m' + 'hello' + '\033[0;39m'`


## 参考

* [ANSI Escape Sequences](http://www.isthe.com/chongo/tech/comp/ansi_escapes.html)
* [ANSI escape code - Wikipedia, the free encyclopedia](http://en.wikipedia.org/wiki/ANSI_escape_code)
* [Terminal colour highlights](http://www.pixelbeat.org/docs/terminal_colours/)
* [xterm - Wikipedia, the free encyclopedia](http://en.wikipedia.org/wiki/Xterm)
