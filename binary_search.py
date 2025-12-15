array = [1, 2, 3, 45, 356, 569, 600, 705, 923]


def search(array, number):
    """Бинарный поиск в отсортированном списке."""

    left = 0
    right = len(array) - 1

    while left <= right:
        middle = (left + right) // 2

        if array[middle] == number:
            return True  # Нашли значение
        elif array[middle] < number:
            left = middle + 1  # Ищем справа
        else:
            right = middle - 1  # Ищем слева

    return False  # Не нашли


print(search(array, 569))  # True
print(search(array, 570))  # False
