import asyncio
import random
import time

async def process_order(order: str, min_time: float = 1.5) -> str:
    """
    Імітує асинхронну обробку замовлення.
    """
    preparation_time = random.uniform(0.5, 3)
    await asyncio.sleep(preparation_time)
    elapsed_time = max(preparation_time, min_time)

    if random.random() < 0.2:  # 20% шанс на помилку
        raise Exception(f"Помилка обробки замовлення: {order}")
    return f"Замовлення {order} готове за {elapsed_time:.2f} секунд."

async def async_map_with_abort(data: list, async_function: callable, timeout: float = 5.0) -> list:
    """
    Виконує асинхронну обробку замовлень з можливістю скасування за допомогою asyncio.
    """
    results = []
    errors = []
    tasks = []

    async def handle_item(index, item, cancel_event):
        try:
            if cancel_event.is_set():
                return  # Якщо задачу скасували, припиняємо її виконання.
            result = await asyncio.wait_for(async_function(item), timeout=timeout)
            results.append((index, result))
        except asyncio.TimeoutError:
            errors.append((index, "Час обробки вичерпано"))
        except Exception as e:
            errors.append((index, str(e)))

    cancel_event = asyncio.Event()

    for index, item in enumerate(data):
        task = asyncio.create_task(handle_item(index, item, cancel_event))
        tasks.append(task)

    try:
        # Очікуємо завершення задач
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        # Якщо задачі було скасовано, обробляємо цей випадок
        print("Обробка була скасована.")
        cancel_event.set()

    return errors, [result[1] for result in sorted(results)]
