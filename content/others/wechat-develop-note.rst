微信开发过程中遇到的问题
===============================

:date: 2015-06-08
:tags: 微信
:slug: wechat-develop-note


JSSDK
-------

**invalid signature**, 排查:

前端：

* ``url`` 参数动态获取
* 注意参数大小写::

    appId: '',         //  I 大写
    timestamp: 134xxx, // 全小写, 必须与后端签名时 timestamp 的值一致
    nonceStr: '',      //  ** 尤其注意 S 是大写 **, 必须与后端签名时 noncestr 的值一致

后端：

* 确保 jsapi_ticket 未过期
* 确认参与签名的参数，注意大小写::

    noncestr        // 全小写，** 尤其注意 s 是小写 **
    jsapi_ticket    // 全小写
    timestamp       // 全小写
    url             // 小写，必须是前端动态获取
* 签名算法
  * 是否按字段名的ASCII 码从小到大排序
  * 使用 sha1 签名


微信支付 **商户签名错误**, 排查:

前端:

* 检查参数大小写::

    timestamp: 0,                     // ** 小写 **
    nonceStr: '',                     // S 大写
    package: 'prepay_id=wx2015xxxx',  // 内容是否对了？
    paySign: 'MD5',                   // 新版是 MD5

后端:

* 检查参与签名的参数大小写::

    appId            // I 大写
    timeStamp        // ** S 大写 **
    nonceStr         // S 大写
    package          // prepay_id=wx2015xxxx
    signType         // 新版是 MD5
* `签名算法 <http://pay.weixin.qq.com/wiki/doc/api/index.php?chapter=4_3>`__ 是否正确


微信支付
---------

使用 ``requests`` 模块发送请求时，如何使用商户证书?  ::

    cert = ('/path/to/apiclient_cert.pem', '/path/to/apiclient_key.pem')
    requests.post(url, data=data, cert=cert)

使用证书发送请求时，出现 ``UnicodeEncodeError`` ::

    File "/xxx/lib/python2.7/ssl.py", line 198, in send
    v = self._sslobj.write(data)
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 363-364: ordinal not in range(128)

ssl data 不支持 unicode, data 参数不要传 ``unicode``, 改为 ``utf-8`` 编码字符串::

    xml = u'<xml>巴拉巴拉巴拉<xml>'
    requests.post(url, data=xml, cert=cert)   # UnicodeEncodeError
    改为
    requests.post(url, data=xml.encode('utf8'), cert=cert)


企业付款
----------

**参数错误:输入的商户号有误**

* 检查提交的参数名称是否有误::

    mch_appid         # ** 在其他支付 api 中参数的名称是 appid **
    mchid             # ** 在其他支付 api 中参数的名称是 mch_id **
