import asyncio
import random
import logging

logging.basicConfig(level=logging.INFO)

class EventEmitter:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        """
        Додає нового спостерігача.
        """
        self.subscribers.append(callback)

    def emit(self, message):
        """
        Надсилає повідомлення всім спостерігачам.
        """
        for subscriber in self.subscribers:
            subscriber(message)

async def producer(queue: asyncio.Queue, emitter: EventEmitter):
    """
    Емітує події на основі випадкових затримок.
    """
    for i in range(10):
        await asyncio.sleep(random.uniform(0.5, 2))
        message = f"Подія {i}"
        logging.info(f"Емітер: Генерую {message}")
        emitter.emit(message)
        await queue.put(message)

async def consumer(queue: asyncio.Queue, consumer_id: int):
    """
    Отримує події з черги.
    """
    while True:
        message = await queue.get()
        logging.info(f"Споживач {consumer_id}: Обробляю {message}")
        await asyncio.sleep(random.uniform(0.5, 1.5))  # Імітація обробки
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    emitter = EventEmitter()

    # Реєструємо підписників
    emitter.subscribe(lambda message: logging.info(f"Логер: отримано {message}"))

    # Запускаємо продюсера та споживачів
    producer_task = asyncio.create_task(producer(queue, emitter))
    consumer_tasks = [asyncio.create_task(consumer(queue, i)) for i in range(3)]

    await producer_task  # Чекаємо завершення генерації подій
    await queue.join()  # Чекаємо, поки черга стане порожньою

    for task in consumer_tasks:
        task.cancel()  # Завершуємо роботу споживачів

if __name__ == "__main__":
    asyncio.run(main())
