JSON Web Token (JWT) 简介
=============================
:date: 2015-06-24
:modified: 2015-06-30
:slug: hello-jwt
:tags: jwt

`JSON Web Token (JWT) <http://tools.ietf.org/html/rfc7519>`__
是一种基于 token 的认证方案。


JSON Web Token 的结构
-----------------------

一个 JWT token 看起来是这样的::

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjEzODY4OTkxMzEsImlzcyI6ImppcmE6MTU0ODk1OTUiLCJxc2giOiI4MDYzZmY0Y2ExZTQxZGY3YmM5MGM4YWI2ZDBmNjIwN2Q0OTFjZjZkYWQ3YzY2ZWE3OTdiNDYxNGI3MTkyMmU5IiwiaWF0IjoxMzg2ODk4OTUxfQ.uKqU9dTB6gKwG6jQCuXYAiMNdfNRw98Hw_IWuA5MaMo

可以简化为下面这样的结构::

    base64url_encode(Header) + '.' + base64url_encode(Claims) + '.' + base64url_encode(Signature)

Header
--------

Header 包含了一些元数据，至少会表明 token 类型以及 签名方法。比如 ::

    {
          "typ" : "JWT",
          "alg" : "HS256"
    }

* ``type``: 必需。token 类型，``JWT`` 表示是 JSON Web Token.
* ``alg``: 必需。token 所使用的签名算法，可用的值在 `这里 <http://tools.ietf.org/html/rfc7518#section-3.1>`__ 有规定。


Claims (Payload)
------------------

Claims 部分包含了一些跟这个 token 有关的重要信息。
JWT 标准规定了一些字段，下面节选一些字段:

* ``iss``: The issuer of the token，token 是给谁的
* ``sub``: The subject of the token，token 主题
* ``exp``: Expiration Time。 token 过期时间，Unix 时间戳格式
* ``iat``: Issued At。 token 创建时间， Unix 时间戳格式
* ``jti``: JWT ID。针对当前 token 的唯一标识

除了规定的字段外，可以包含其他任何 JSON 兼容的字段。

Payload 示例::

    {
        "iss": "mozillazg.com",
        "exp": 1435055117,
        "user_id": 1,
        "foo": "bar"
    }

Signature
------------

JWT 标准遵照 JSON Web Signature (JWS) 标准来生成签名。签名主要用于验证 token 是否有效，是否被篡改。 签名时可以 这些算法进行签名，比如 HMAC SHA-256::

    content = base64url_encode(Header) + '.' + base64url_encode(Claims)
    signature = hmacsha256.hash(content)

**说到这里有一点需要特别注意的是，默认情况下，JWT 中信息都是明文的，即 Claims 的内容并没有
被加密，可以通过 base64url_decode(text) 的方式解码得到 Claims** 。
所以，不要在 Claims 里包含敏感信息，如果一定要包含敏感信息的话，记得先将 Claims 的内容进行加密（比如，使用 JSON Web Encryption (JWE) 标准进行加密）
然后在进行 base64url_encode 操作。


Python 实现
---------------

**已有的轮子**: 上 PyPI 上 `搜索 JWT <https://pypi.python.org/pypi?%3Aaction=search&term=JWT&submit=search>`__ 即可。
用的比较多是 `PyJWT <https://pypi.python.org/pypi/PyJWT/>`_ 。

**手动简单实现** ::

    import base64
    import json
    import hashlib
    import hmac
    
    
    def base64url_encode(s):
        return base64.urlsafe_b64encode(s).replace('=', '')

    headers = json.dumps({
        "typ" : "JWT",
        "alg" : "HS256"
    })
    claims = json.dumps({
        "iss": "mozillazg.com",
        "exp": 1435055117,
        "user_id": 1,
        "foo": "bar"
    })
    content = base64url_encode(headers) + '.' + base64url_encode(claims)
    secret_key = 'your secret key'
    signature = hmac.new(secret_key, content, hashlib.sha256).digest()

    token = content + '.' + base64url_encode(signature)

最后得到的 token 的值是 ::

    eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAibW96aWxsYXpnLmNvbSIsICJmb28iOiAiYmFyIiwgInVzZXJfaWQiOiAxLCAiZXhwIjogMTQzNTA1NTExN30.iFAK1B-6xRlmlSHnS2P24wsS6Ko6iZjbSPHdldzIhp4

之所以用 ``base64url_encode`` 而不是 ``base64.b64encode`` 是因为 token 可能会被用作 url 参数，
而 base64 中的 ``+``， ``/``， ``=`` 在 url 里被转义成 ``%2B`` ``%2F`` ``%3D``，导致 token 的值变得更长了，所以这里使用 base64url 即进行如下替换 ``+`` -> ``-``, ``/`` -> ``_``, 删除 ``=``。

再次提示， **claims 的值并没有被加密**，就算不知道 secert_key 的值也可以得到 claims 的值。


参考资料
--------

* http://jwt.io/
* http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html
* https://developer.atlassian.com/static/connect/docs/latest/concepts/understanding-jwt.html
* http://www.intridea.com/blog/2013/11/7/json-web-token-the-useful-little-standard-you-haven-t-heard-about
* https://auth0.com/blog/2014/01/27/ten-things-you-should-know-about-tokens-and-cookies/
* http://www.toptal.com/web/cookie-free-authentication-with-json-web-tokens-an-example-in-laravel-and-angularjs
* https://scotch.io/tutorials/the-anatomy-of-a-json-web-token
* https://github.com/jpadilla/pyjwt/
* https://en.wikipedia.org/wiki/JSON_Web_Token
* http://tools.ietf.org/html/rfc7519
* https://en.wikipedia.org/wiki/Base64#URL_applications
* https://tools.ietf.org/html/rfc4648#section-5
