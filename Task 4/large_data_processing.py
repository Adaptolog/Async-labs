import asyncio
import random
import logging
from typing import AsyncIterator

logging.basicConfig(level=logging.INFO)

async def async_stream_large_dataset(total_size: int, batch_size: int = 10) -> AsyncIterator[list]:
    """
    Потокова генерація великих даних невеликими порціями.
    """
    for i in range(0, total_size, batch_size):
        await asyncio.sleep(0.1)  # Імітуємо затримку
        yield [random.randint(1, 100) for _ in range(batch_size)]  # Генеруємо порцію даних

async def process_batch(batch: list):
    """
    Імітація обробки порції даних із ймовірністю помилки.
    """
    await asyncio.sleep(random.uniform(0.2, 0.5))  # Імітуємо час обробки
    if random.random() < 0.05:  # 5% ймовірність помилки
        raise ValueError(f"Помилка при обробці порції: {batch}")
    return f"Оброблено порцію: {batch}"

async def handle_large_dataset():
    """
    Обробляє великий набір даних за допомогою асинхронних потоків.
    """
    total_size = 100
    batch_size = 10
    processed = []
    errors = []

    logging.info("Початок обробки великих даних...")
    logging.info(f"Всього елементів: {total_size}, розмір порції: {batch_size}\n")

    # Асинхронний цикл для потокової обробки
    async for batch in async_stream_large_dataset(total_size, batch_size):
        try:
            result = await process_batch(batch)
            processed.append(result)
        except Exception as e:
            errors.append(str(e))

    # Виведення підсумків
    logging.info("\nЗавершення обробки.\n")
    logging.info("Оброблені порції:")
    for res in processed:
        logging.info(f"  - {res}")

    if errors:
        logging.error("\nПомилки:")
        for err in errors:
            logging.error(f"  - {err}")

async def demo():
    """
    Демонстрація обробки великих даних.
    """
    await handle_large_dataset()

if __name__ == "__main__":
    asyncio.run(demo())
