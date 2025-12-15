import asyncio
import aiohttp
import json

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://google.com",
    "https://yandex.ru"
]


async def fetch_urls(urls):
    semaphore = asyncio.Semaphore(5)  # Максимум 5 одновременных запросов

    async def get_url(url, session):
        """Функция для одного запроса."""

        async with semaphore:
            try:
                async with session.get(url, timeout=5) as response:
                    status = response.status
            except Exception:
                status = 0
            return json.dumps({"url": url, "status_code": status})

    # Сессия для запросов
    async with aiohttp.ClientSession() as session:
        # Создаем задачи
        tasks = [get_url(url, session) for url in urls]

        # Запускаем ВСЕ запросы одновременно
        results = await asyncio.gather(*tasks)

        with open('/Users/bragin/Desktop/results.json', 'w') as f:
            print(*results, file=f, sep='\n')

if __name__ == '__main__':
    asyncio.run(fetch_urls(urls))
