Python: 建造者模式(builder pattern)
=====================================
:date: 2016-08-21
:slug: python-builder-pattern
:tags: design pattern, 设计模式

当一个对象必须经过多个步骤来创建，并且要求不同的参数可以产生不同的表现的时候，
我们可以使用建造者模式。

比如下面这个摘自《Mastering Python Design Patterns》 的例子:

.. code-block:: python

    class Computer:
        def __init__(self, serial_number):
            self.serial = serial_number
            self.memory = None
            self.cpu = None
            self.disk = None


        def __str__(self):
            return 'memory: {0} GB, cpu: {1}, disk: {2} GB'.format(
                self.memory, self.cpu, self.disk
            )


    class ComputerBuilder:
        def __init__(self):
            self.computer = Computer('SN-12345555')

        def configure_memory(self, memory):
            self.computer.memory = memory

        def configure_cpu(self, cpu):
            self.computer.cpu = cpu

        def configure_disk(self, disk):
            self.computer.disk = disk


    class HardwareEngineer:
        def __init__(self):
            self.builder = None

        def construct_computer(self, memory, cpu, disk):
            self.builder = ComputerBuilder()
            self.builder.configure_memory(memory)
            self.builder.configure_cpu(cpu)
            self.builder.configure_disk(disk)

        @property
        def computer(self):
            return self.builder.computer

    engineer = HardwareEngineer()
    engineer.construct_computer(16, 8, 500)
    computer = engineer.computer
    print(computer)


参考资料
-----------
* `《Mastering Python Design Patterns》 <https://book.douban.com/subject/26336439/>`_
