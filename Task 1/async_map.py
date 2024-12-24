import asyncio
import random
import logging
from typing import Callable, Optional, List

logging.basicConfig(level=logging.INFO)

def async_filter_map(
    data: List[str],
    async_filter_map_fn: Callable[[str], asyncio.Future],
    debounce_time: Optional[float] = None,
    callback: Callable[[List[str]], None] = None
) -> asyncio.Future:
    """
    Асинхронний аналог комбінації `filter` і `map`.
    Виконує асинхронний колбек для кожного елемента, фільтруючи й трансформуючи дані.
    """
    loop = asyncio.get_event_loop()
    results = []
    pending = len(data)
    done_future = asyncio.Future()

    def process_done(item: str, future: asyncio.Future):
        nonlocal pending
        try:
            result = future.result()
            if result is not None:
                results.append(result)
        except Exception as e:
            logging.error(f"Помилка під час обробки елемента '{item}': {e}")
        
        pending -= 1
        if pending == 0:
            if callback:
                callback(results)
            done_future.set_result(results)

    for item in data:
        task = async_filter_map_fn(item)
        task.add_done_callback(lambda future, item=item: process_done(item, future))
        if debounce_time:
            loop.call_later(debounce_time, lambda: None)

    return done_future

def filter_map_callback(item: str) -> asyncio.Future:
    """
    Асинхронний колбек для `filterMap`.
    Симулює асинхронну обробку і повертає Future з результатом або None.
    """
    future = asyncio.Future()

    def process():
        try:
            if random.random() > 0.3:  # 70% шанс зберегти елемент
                future.set_result(f"Оброблений елемент: {item}")
            else:
                future.set_result(None)  # Фільтруємо елементи
        except Exception as e:
            future.set_exception(e)

    delay = random.uniform(0.5, 1.5)  # Імітація роботи
    asyncio.get_event_loop().call_later(delay, process)
    return future

def demo_cases():
    """
    Основна функція для демонстрації використання асинхронного `filterMap`.
    """
    loop = asyncio.new_event_loop()  # Створюємо новий цикл подій
    asyncio.set_event_loop(loop)  # Встановлюємо його як поточний цикл подій
    data = ["Кава", "Чай", "Піца", "Суші"]

    def on_complete(results):
        logging.info("Результати:")
        for result in results:
            logging.info(f"  - {result}")

    # Запуск без debounce
    logging.info("Демо: без debounce")
    loop.run_until_complete(async_filter_map(data, filter_map_callback, callback=on_complete))

    # Запуск із debounce
    logging.info("Демо: з debounce (0.5 сек)")
    loop.run_until_complete(async_filter_map(data, filter_map_callback, debounce_time=0.5, callback=on_complete))

if __name__ == "__main__":
    demo_cases()
