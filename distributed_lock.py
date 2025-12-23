import datetime
import time

# Глобальный флаг для блокировки
is_running = False


def single(max_processing_time=datetime.timedelta(minutes=2)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            global is_running

            # Ждем, пока функция не освободится
            while is_running:
                time.sleep(0.1)  # Не перегружать CPU

            # Захватываем блокировку
            is_running = True

            try:
                # Выполняем оригинальную функцию с таймером
                start_time = time.time()
                result = func(*args, **kwargs)

                # Проверяем время выполнения
                work_time = time.time() - start_time

                if work_time > max_processing_time.total_seconds():
                    print(f"Функция работала {work_time:.1f} сек, больше допусимого!")

                return result
            finally:
                # Всегда освобождаем блокировку
                is_running = False

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    time.sleep(2)


if __name__ == "__main__":
    print("Начало выполнения")
    result = process_transaction()
    print("Выполнено")
