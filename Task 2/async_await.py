import asyncio
import random
from typing import List, Optional, Tuple


async def process_order_async(order: str, min_time: float = 1.5) -> str:
    """
    Асинхронна функція для обробки замовлення.
    """
    preparation_time = random.uniform(0.5, 3)
    await asyncio.sleep(preparation_time)
    elapsed_time = max(preparation_time, min_time)

    if random.random() < 0.2:  # 20% шанс на помилку
        raise Exception(f"Помилка обробки замовлення: {order}")
    return f"Замовлення {order} готове за {elapsed_time:.2f} секунд."
