title: multipart form data 的数据格式
slug: http-multipart-form-data
tags: http
date: 2016-02-19

假设 form 如下：

    <form action="/upload" enctype="multipart/form-data" method="post">
        Username: <input type="text" name="username">
        Password: <input type="password" name="password">
        File: <input type="file" name="file">
        <input type="submit">
    </form>

## header

    Content-Type: multipart/form-data; boundary={boundary}\r\n


## body

### 普通 input 数据

    --{boundary}\r\n
    Content-Disposition: form-data; name="username"\r\n
    \r\n
    Tom\r\n


### 文件上传 input 数据

    --{boundary}\r\n
    Content-Disposition: form-data; name="file"; filename="myfile.txt"\r\n
    Content-Type: text/plain\r\n
    Content-Transfer-Encoding: binary\r\n
    \r\n
    hello word\r\n

### 结束标志

    --{boundary}--\r\n


数据示例：

    POST /upload HTTP/1.1
    Host: 172.16.100.128:5000
    Content-Length: 394 
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryLumpDpF3AwbRwRBn
    Referer: http://172.16.100.128:5000/
    
    ------WebKitFormBoundaryUNZIuug9PIVmZWuw
    Content-Disposition: form-data; name="username"
    
    Tom
    ------WebKitFormBoundaryUNZIuug9PIVmZWuw
    Content-Disposition: form-data; name="password"
    
    passwd
    ------WebKitFormBoundaryUNZIuug9PIVmZWuw
    Content-Disposition: form-data; name="file"; filename="myfile.txt"
    Content-Type: text/plain
    
    hello world
    ------WebKitFormBoundaryUNZIuug9PIVmZWuw--


## 参考资料

* <https://tools.ietf.org/html/rfc2388>
* <https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.2>
* <http://d.hatena.ne.jp/satox/20110726/1311665904>
* <http://mugenup-tech.hatenadiary.com/entry/2014/08/28/100910>