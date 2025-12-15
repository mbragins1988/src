import http.client


def wsgi_app(environ, start_response):
    """
    WSGI приложение.
    environ - словарь с информацией о запросе
    start_response - функция для отправки заголовков
    """

    # Получаем путь, например: /USD -> currency = "USD"
    path = environ.get("PATH_INFO", "/")
    currency = path[1:].upper()  # Убрали / и привели к верхнему регистру

    # Запрашиваем данные с API
    # Устанавливаем соединение
    conn = http.client.HTTPSConnection("api.exchangerate-api.com")
    conn.request("GET", f"/v4/latest/{currency}")
    # Получили ответ АПИ
    response = conn.getresponse()

    if response.status != 200:
        # Ошибка
        start_response(
            "500 Internal Server Error", [("Content-Type", "application/json")]
        )
        return [b'{"error": "Failed to fetch exchange rates"}']

    # Читаем данные
    data = response.read()
    conn.close()

    # Отправляем успешный ответ
    start_response(
        "200 OK",
        [
            ("Content-Type", "application/json"),
        ],
    )

    return [data]
