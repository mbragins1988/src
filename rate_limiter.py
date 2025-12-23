import random
import time

import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    """Ограничитель скорости."""

    def __init__(self):
        # Подключаемся к Redis серверу
        self.redis = redis.Redis()
        # Ключ, под которым храним данные в Redis
        self.key = "requests"

    def test(self):
        now = time.time()

        # Удаляем старые запросы.
        # zremrangebyscore - удаляет из sorted set по значению score
        # z - Sorted Set (тип данных)
        # rem - remove (удалить)
        # range - диапазон
        # by score - по значению score
        # Удаляем все записи со score от 0 до (now - 3)
        # То есть удаляем запросы, которые были более 3 секунд назад
        self.redis.zremrangebyscore(self.key, 0, now - 3)

        # Считаем сколько осталось
        # zcard - количество элементов в sorted set
        # Теперь в sorted set только запросы за последние 3 секунды!
        count = self.redis.zcard(self.key)

        # Если уже 5 или больше запросов, то превышает
        if count >= 5:
            return False

        # Добавляем новый
        # Сохраняет время запроса как элемент sorted set
        self.redis.zadd(self.key, {str(now): now})
        return True  # Запрос разрешен


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == "__main__":
    rate_limiter = RateLimiter()
    # Удаляем все старые записи под ключом "requests"
    rate_limiter.redis.delete("requests")

    for i in range(50):
        time.sleep(random.randint(100, 500) / 1000.0)
        try:
            # Пытаемся сделать запрос
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
