import asyncio
import random
from typing import AsyncIterator

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
