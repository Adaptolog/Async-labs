import random
import time
import logging
from typing import List, Callable, Optional, Tuple

logging.basicConfig(level=logging.INFO)

def process_order(order: str, callback: Callable[[Optional[str], Optional[str]], None], min_time: float = 1.5) -> None:
    """
    Імітує обробку замовлення з випадковою затримкою.
    Якщо час обробки менше `min_time`, додається додаткова затримка.
    """
    preparation_time = random.uniform(0.5, 3)  # Час виконання
    time.sleep(preparation_time)  # Блокує виконання для імітації
    elapsed_time = max(preparation_time, min_time)

    if preparation_time < min_time:
        time.sleep(min_time - preparation_time)

    if random.random() < 0.2:  # 20% шанс на помилку
        callback(f"Помилка обробки замовлення: {order}", None)
    else:
        callback(None, f"Замовлення {order} готове за {elapsed_time:.2f} секунд.")
