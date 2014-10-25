Title: [django]同时使用 render_to_response 和 set_cookie
Date: 2013-09-01
Tags: django, python
Slug: django-render_to_response-and-set_cookie

render_to_response 返回的其实也是一个 response 对象，直接使用这个 response 对象即可:

    :::python
    def foobar(request):
        #...
        response = render_to_response(template_name, context)
        response.set_cookie('foo', 'bar', 60 * 60 * 24)
        return response

## 参考

* [Django: use render_to_response and set cookie](http://stackoverflow.com/questions/4981601/django-use-render-to-response-and-set-cookie)
