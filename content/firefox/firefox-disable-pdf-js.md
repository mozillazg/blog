Title: [firefox]禁用在线查看 PDF 文件的功能
Date: 2013-03-06
Tags: firefox, pdf.js
Slug: firefox-disable-pdf-js


最近更新了 firefox 后发现没法下载 PDF 文件了，因为默认情况下 firefox 会直接在浏览器中打开 PDF 文件。问题是，有的 PDF 文件很大啊，你也给我直接打开，我的网速受不了啊。有时我就是想保存 PDF 文件，不想直接打开。

下面说一下如何禁用这个功能，恢复保存 PDF 文件的功能。

打开 [about:config](about:config) 输入 `pdfjs.disabled` 双击它，将它的值改为 true：

![set pdfjs.disabled to true](/static/images/2013-03-06-firefox-pdf-js.jpg)
