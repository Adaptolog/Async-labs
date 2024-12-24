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
