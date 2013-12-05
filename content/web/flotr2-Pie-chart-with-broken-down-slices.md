Title: [JavaScript] 使用 flotr2 绘制包含子项的饼图
Date: 2013-12-05
Tags: javascript, flotr2
Slug: flotr2-pie-chart-with-broken-down-slices

> [Flotr2](http://www.humblesoftware.com/flotr2/) 是一个用于绘制 HTML5 图形和图表的开源 JS 库

由于 flotr2 不支持环形饼图，所以对于包含子项的饼图只能通过其他办法来实现。

我的实现方法是，首先显示最外层的饼图，再通过点击某一个项显示它包含的子项的饼图。
具体代码请见：

<iframe width="100%" height="350" src="http://jsfiddle.net/M8rT7/embedded/" allowfullscreen="allowfullscreen" frameborder="0"></iframe>



当然，由于 flotr2 的局限性，这个图并不完美。如果想要更好的效果，
可以试试其他的 JS 图表插件实现的效果：

* [Highcharts - Donut chart](http://www.highcharts.com/demo/pie-donut)
* [Pie chart with broken down slices | amCharts](http://www.amcharts.com/javascript-charts/pie-chart-with-broken-down-slice/)
* [Sequences sunburst](http://bl.ocks.org/kerryrodden/7090426)


