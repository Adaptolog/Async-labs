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

def async_map(
    data: List[str],
    async_function: Callable[[str, Callable[[Optional[str], Optional[str]], None]], None],
    callback: Callable[[Optional[List[Tuple[int, str]]], List[Optional[str]]], None],
) -> None:
    """
    Асинхронний аналог функції `map`, що підтримує колбеки.
    """
    results = [None] * len(data)
    errors = []
    completed = 0

    def handle_result(index: int, error: Optional[str], result: Optional[str]) -> None:
        nonlocal completed
        if error:
            errors.append((index, error))
        else:
            results[index] = result

        completed += 1
        if completed == len(data):  # Завершено
            callback(errors if errors else None, results)

    for index, item in enumerate(data):
        async_function(item, lambda error, result: handle_result(index, error, result))

def manage_orders() -> None:
    """
    Основна функція для запуску обробки замовлень.
    """
    orders = ["Кава", "Чай", "Піца", "Суші"]
    logging.info("Початок обробки замовлень...")

    def show_results(errors: Optional[List[Tuple[int, str]]], results: List[Optional[str]]) -> None:
        if errors:
            logging.error("Помилки під час обробки:")
            for index, error in errors:
                logging.error(f"  - Замовлення {orders[index]}: {error}")

        logging.info("Результати успішної обробки:")
        for result in results:
            if result:
                logging.info(f"  - {result}")

        logging.info("Обробка завершена.")

    async_map(orders, lambda order, cb: process_order(order, cb, min_time=1.5), show_results)

if __name__ == "__main__":
    manage_orders()