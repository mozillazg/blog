


Foo.objects.filter(name='foo').delete(using='writedb')

foos = Foo.objects.filter(name='foo')
for foo in foos:
    foos.delete(using='writedb')
