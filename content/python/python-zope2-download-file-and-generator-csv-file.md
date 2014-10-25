Title: [python]zope2 文件下载及导出为 csv 文件
Date: 2013-03-18
Tags: python, zope2, csv
Slug: python-zope2-download-file-and-generator-csv-file

本文将简单实现 zope2 导出数据库数据为 csv 文件并提供下载链接。

先建一个 **Z SQL Method**，ID 为 **query_sql**，内容就是查询所有结果的 sql 语句 ：

    select * from user

再建一个 **Script (Python)** ID 为 **hello_py**, 内容是调用上面定义的 Z SQL Method，并将结果转换为**逗号分隔**的 cvs 格式，下面将详细说明：

    :::python
    request = container.REQUEST
    response =  request.response

    query_result = context.query_sql()  # 获取数据库查询结果
    dics = query_result.dictionaries()  # 将查询结果转换为一个字典

    # 输出查询结果包含的字段名称，也就是 csv 文件的第一行
    print ','.join([str(x) for x in dics[0].keys()]) + '\r\n'

    for x in dics:
        #print x.keys()
        for y in x.keys():
            print str(x[y]) + ',',  # 输出每条查询结果中各字段的值
        print '\r\n'

    # 设置返回的 response 对象的 Header
    response.setHeader('Content-Type', 'application/ms-excel;charset=utf-8')  # 文件 MIME 类型及编码
    # 声明是个附件，不要打开而是下载，同时设置文件名
    response.setHeader('Content-Disposition', 'attachment; filename=txt.csv')

    return printed

然后建一个 DTML 文件，ID 为 **txt.csv** 用来调用上面的脚本，这个文件其实就是要下载的附件:

    <dtml-var hello_py>

最后就是再建一个 DTML 文件，ID 为 download 。主要是提供一个指向 txt.csv DTML 文件的链接：

    <html>
        <p><a href="txt.csv">Download txt.csv</a></p>
    </html>

<!--效果：-->


## 参考
* [用Zope上传下载文件](http://gqliu.blog.163.com/blog/static/22584907200831065054649/)
