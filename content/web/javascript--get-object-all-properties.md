Title: [javascript]列出对象所有属性
Date: 2013-05-23
Tags: javascript, web
Slug: javascript-list-object-all-properties

当我们想知道某个对象拥有哪些的属性时，可以用下面的方法（现代浏览器）：

    :::javascript
    var properties = Object.keys(obj);


这个方法对于我们使用第三方 javascript 插件，而该插件的文档不是很详细时有很大的帮助

    :::javascript
    trackFormatter: function(obj){
      console.debug('properties:');
      console.debug(Object.keys(obj));
    }

![console debug object properties image](/static/images/2013-05-23_01.png)


## 参考

* [json - How to list the properties of a javascript object - Stack Overflow](http://stackoverflow.com/questions/208016/how-to-list-the-properties-of-a-javascript-object)
