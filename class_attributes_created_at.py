import datetime


class MetaWithTime(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.datetime.now()
        return super().__new__(cls, name, bases, attrs)


# Использование
class MyClass(metaclass=MetaWithTime):
    pass


print(MyClass.created_at)  # Выведет текущее время
