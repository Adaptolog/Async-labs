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
