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
