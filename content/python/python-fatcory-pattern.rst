Python: 工厂模式(fatcory pattern)
======================================
:date: 2016-08-20
:slug: python-fatcory-pattern
:tags: design pattern, 设计模式


工厂模式是说调用方可以通过调用一个简单函数就可以创建
不同的对象。工厂模式一般包含工厂方法和抽象工厂两种模式。


工厂方法(factory method)
---------------------------

工厂方法模式是指定义一个可以根据输入参数的不同返回不同对象的函数。

.. code-block:: python


    class JSONParser:
        def parse(self, raw_data):
            return json.loads(raw_data)


    class XMLParser:
        def parse(self, raw_data):
            return xml2dict(raw_data)


    def new_parser(type, **kwargs):
        if type == 'json':
            return JSONParser()
        elif type == 'xml':
            return XMLParser()


    parser = new_parser('json')
    with open('hello.json') as fp:
        data = parser.parse(fp.read())
    print(data)


抽象工厂(abstract factory)
---------------------------------

一系列的工厂方法组合在一起实现了一个抽象工厂。

还是上面那个例子，我们再加一个工厂方法:

.. code-block:: python

    class DBSaver:
        def save(self, obj, **kwargs):
            model = Model(**obj)
            model.save()


    class FileSaver:
        def __init__(self, save_dir):
            self.save_dir = save_dir

        def save(self, obj, name):
            path = os.path.join(self.save_dir, name)
            with open(path, 'wb') as fp:
                data = json.dumps(obj)
                fp.write(data)


    def new_saver(type, **kwargs):
        if type == 'db':
            return DBSaver()
        elif type == 'file':
            save_dir = kwargs['save_dir']
            return FileSaver(save_dir)


    class FileHandler:
        def __init__(self, parse_type, save_type, **kwargs):
            self.parser = new_parser(parse_type, **kwargs)
            self.saver = new_saver(save_type, **kwargs)

        def do(self, data, filename):
            obj = self.parser.parse(data)
            self.saver.save(obj, filename)

    handler = FileHandler('json', 'file', save_dir='save')
    with open('hello.json') as fp:
        data = fp.read()
    handler.do(data, 'data.json')


工厂方法和抽象工厂的选择:
先使用工厂方法，当发现需要使用一系列工厂方法来创建多个对象的时候，
可以考虑把这些创建对象的过程合并到一个抽象工厂。


参考资料
-----------
* `《Mastering Python Design Patterns》 <https://book.douban.com/subject/26336439/>`_
