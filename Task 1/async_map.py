import asyncio
import random
import logging
from typing import Callable, Optional, List, Tuple

logging.basicConfig(level=logging.INFO)

async def async_filter_map(
    data: List[str],
    async_filter_map_fn: Callable[[str], Optional[str]],
    debounce_time: Optional[float] = None
) -> List[str]:
    """
    Асинхронний аналог комбінації `filter` і `map`.
    Виконує асинхронний колбек для кожного елемента, фільтруючи й трансформуючи дані.
    """
    results = []

    async def process_item(item: str) -> None:
        result = await async_filter_map_fn(item)
        if result is not None:
            results.append(result)

        # Додаткове очікування для debounce
        if debounce_time is not None:
            await asyncio.sleep(debounce_time)

    await asyncio.gather(*(process_item(item) for item in data))
    return results

async def filter_map_callback(item: str) -> Optional[str]:
    """
    Асинхронний колбек для `filterMap`.
    Симулює асинхронну обробку і повертає результат або None для фільтрації.
    """
    await asyncio.sleep(random.uniform(0.5, 1.5))  # Імітація роботи
    if random.random() > 0.3:  # 70% шанс зберегти елемент
        return f"Оброблений елемент: {item}"
    return None  # Фільтруємо елементи

async def demo_cases():
    """
    Основна функція для демонстрації використання асинхронного `filterMap`.
    """
    data = ["Кава", "Чай", "Піца", "Суші"]
    logging.info("Початок обробки...")

    # Запуск без debounce
    results = await async_filter_map(data, filter_map_callback)
    logging.info("Результати без debounce:")
    for result in results:
        logging.info(f"  - {result}")

    # Запуск із debounce (додаткова затримка 0.5 секунди)
    results_with_debounce = await async_filter_map(data, filter_map_callback, debounce_time=0.5)
    logging.info("Результати з debounce:")
    for result in results_with_debounce:
        logging.info(f"  - {result}")

if __name__ == "__main__":
    asyncio.run(demo_cases())
