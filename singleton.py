import singleton_module


class Single_new:
    """1. Способ через __new__"""

    one = None

    def __new__(cls):
        if cls.one is None:
            cls.one = super().__new__(cls)
        return cls.one


a = Single_new()
b = Single_new()
print('1. Способ через __new__ -', a is b)  # True - один объект

# 2. Способ через модуль
x = singleton_module.the_one
y = singleton_module.the_one
print('2. Способ через модуль -', x is y)  # True - один объект


class SingleMeta(type):
    """3. Способ через метакласс."""

    all = {}

    def __call__(cls):
        if cls not in cls.all:
            cls.all[cls] = super().__call__()
        return cls.all[cls]


class Single3(metaclass=SingleMeta):
    pass


# Проверка:
p = Single3()
q = Single3()
print('3. Способ через метакласс -', p is q)  # True - один объект
