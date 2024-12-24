import random
import time
from typing import List, Callable, Optional, Tuple

def process_order(order: str, min_time: float = 1.5) -> str:
    """
    Синхронна функція для обробки замовлення.
    """
    preparation_time = random.uniform(0.5, 3)
    time.sleep(preparation_time)
    elapsed_time = max(preparation_time, min_time)

    if random.random() < 0.2:  # 20% шанс на помилку
        raise Exception(f"Помилка обробки замовлення: {order}")
    return f"Замовлення {order} готове за {elapsed_time:.2f} секунд."
