import json

import redis


class RedisQueue:
    def __init__(self):
        # Подключаемся к Redis серверу
        # Создаем объект соединения с Redis
        self.rc = redis.Redis(host="localhost", port=6379, db=0)
        # Задаем имя очереди - это ключ, под которым
        # будем хранить нашу очередь в Redis
        self.queue_name = "my_queue"

    def publish(self, msg):
        """Добавить сообщение в очередь."""

        # Превращаем словарь в строку JSON
        msg_json = json.dumps(msg)
        # Кладем сообщение в конец очереди (справа)
        # rpush = "right push" - добавить справа
        # self.r.rpush(self.queue_name, msg_json) делает:
        # 2. Отправляет команду в Redis: RPUSH "my_queue" '{"a": 1}'
        # 3. Redis:
        #   - Если ключа "my_queue" НЕТ → создает новый список
        #   - Если ключ "my_queue" ЕСТЬ → добавляет в существующий список
        self.rc.rpush(self.queue_name, msg_json)

    def consume(self) -> dict:
        """Взять сообщение из начала очереди."""

        # Берем и удаляем первый элемент из начала очереди (слева)
        # lpop = "left pop" - взять и удалить слева
        # self.r.lpop(self.queue_name) делает:
        # 1. Находит в Redis список под ключом "my_queue"
        # 2. Берет первый (самый старый) элемент из начала списка
        # 3. УДАЛЯЕТ его из списка
        # 4. Возвращает нам этот элемент
        msg_json = self.rc.lpop(self.queue_name)
        print(msg_json)

        if msg_json is None:
            return None  # Очередь пуста

        # Превращаем строку обратно в словарь
        return json.loads(msg_json.decode("utf-8"))


if __name__ == "__main__":
    q = RedisQueue()
    q.publish({"a": 1})
    q.publish({"b": 2})
    q.publish({"c": 3})

    assert q.consume() == {"a": 1}
    assert q.consume() == {"b": 2}
    assert q.consume() == {"c": 3}
