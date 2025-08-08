class MyQueue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError('Очередь пуста')
        return self.items.pop(0)

    def size(self):
        return len(self.items)


# Пример использования:
queue = MyQueue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)

print("Размер очереди:", queue.size())  # Размер очереди: 3

while not queue.is_empty():
    item = queue.dequeue()
    print("Извлечен элемент:", item)
