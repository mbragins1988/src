import concurrent.futures
import json
import random
import time
from multiprocessing import Pool, Process, Queue, cpu_count

from tabulate import tabulate


def generate_data(n):
    """Генерируем числа."""

    return [random.randint(1, 1000) for _ in range(n)]


def process_number(number):
    """Рабочая функция."""

    result = 0

    # I/O имитация - для работы потоков (освобождает GIL)
    time.sleep(0.001)
    for i in range(10):
        result += (number * i) ** 0.5

    return {"number": number, "result": result}


def single_process(numbers):
    """Однопоточный."""

    results = []
    for num in numbers:
        results.append(process_number(num))
    results.insert(0, "Однопоточный")
    return results


def threads(numbers):
    """Многопоточный (concurrent.futures)."""

    results = []
    # Создаём пул потоков
    with concurrent.futures.ThreadPoolExecutor() as pool:
        futures = []
        for num in numbers:
            future = pool.submit(process_number, num)
            futures.append(future)

        # Собираем результаты после работы всех потоков
        for future in futures:
            results.append(future.result())
    results.insert(0, "Многопоточный")
    return results


def pool(numbers):
    """Process Pool (процессы)."""

    # Создаем пул процессов (количество ядер определяется автоматичкски)
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_number, numbers)
    results.insert(0, "Process Pool (процессы)")
    return results


def worker(input_q, output_q):
    """Рабочая функция для процесса."""

    while True:
        num = input_q.get()  # Получаем число из очереди
        if num is None:  # Сигнал остановки
            break

        # Вызываем рабочую функцию process_number
        # Обрабатывает число
        result = process_number(num)
        # Кладёт результат в output_q
        output_q.put(result)


def process_queues(numbers):
    """Process + Queue (процессы с очередями)."""

    # Очереди
    input_q = Queue()
    output_q = Queue()

    # Создаём процессы по количеству ядер
    processes = []
    for _ in range(cpu_count()):
        # Создаёт объект процесса
        p = Process(target=worker, args=(input_q, output_q))
        # Запуск процесса
        p.start()
        processes.append(p)

    # Основной процесс кладёт все данные
    for num in numbers:
        input_q.put(num)

    # Сигналы остановки
    for _ in range(cpu_count()):
        input_q.put(None)

    # Собираем результаты
    results = []
    for _ in range(len(numbers)):
        results.append(output_q.get())

    # Ждём завершения
    for p in processes:
        p.join()

    results.insert(0, "Process + Queue (процессы с очередями)")
    return results


if __name__ == "__main__":
    # Генерируем числа для теста
    test_numbers = generate_data(10000)

    # Список всех способов
    all_ways = [
        ("Обычный (1 процесс)", single_process),
        ("Потоки", threads),
        ("Процессы с Pool", pool),
        ("Процессы с очередями", process_queues),
    ]

    print(f"Тестируем {len(all_ways)} способа:")

    # Проверяем каждый
    times = {}
    for name, func in all_ways:
        start = time.time()
        results = func(test_numbers)
        time_process = time.time() - start
        times[name] = time_process

        with open("/Users/bragin/Desktop/src/results.json", "a", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    # Преобразуем словарь в список списков для tabulate
    table_data = []
    for method, time_process in times.items():
        table_data.append([method, f"{time_process:.3f} сек"])

    # Определяем заголовки
    headers = ["Метод", "Время"]

    print(tabulate(table_data, headers=headers))
