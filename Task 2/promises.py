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

def async_map_with_promises(
    data: List[str], process_function: Callable[[str], str]
) -> Tuple[List[Tuple[int, str]], List[str]]:
    """
    Реалізація асинхронного map за допомогою `concurrent.futures` (аналог промісів).
    """
    from concurrent.futures import ThreadPoolExecutor

    results = []
    errors = []

    def handle_result(index: int, future):
        try:
            result = future.result()
            results.append((index, result))
        except Exception as e:
            errors.append((index, str(e)))

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_function, order) for order in data]
        for index, future in enumerate(futures):
            future.add_done_callback(lambda fut, idx=index: handle_result(idx, fut))

    return errors, [res[1] for res in sorted(results)]

def demo_with_promises():
    orders = ["Кава", "Чай", "Піца", "Суші"]
    print("Початок обробки замовлень за допомогою промісів...")
    errors, results = async_map_with_promises(orders, process_order)

    if errors:
        print("\nПомилки:")
        for index, error in errors:
            print(f"  - Замовлення {orders[index]}: {error}")

    print("\nРезультати:")
    for result in results:
        print(f"  - {result}")


if __name__ == "__main__":
    demo_with_promises()
