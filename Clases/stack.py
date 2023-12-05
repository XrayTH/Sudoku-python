class Stack:
    def __init__(self):
        self.items = []
        self.current = -1
        self.redo_items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.current += 1
        self.items = self.items[:self.current]
        self.items.append(item)
        self.redo_items = []

    def pop(self):
        if not self.is_empty():
            item = self.items.pop()
            self.current -= 1
            self.redo_items.append(item)
            return item
        return None

    def redo(self):
        if self.redo_items:
            item = self.redo_items.pop()
            self.items.append(item)
            self.current += 1
            return item
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[self.current]
        return None

    def size(self):
        return len(self.items)
