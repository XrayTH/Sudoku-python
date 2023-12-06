class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and not found:
            if current.data == data:
                found = True
            else:
                previous = current
                current = current.next
        if current is None:
            raise ValueError("Data not found in the list")
        if previous is None:
            self.head = current.next
        else:
            previous.next = current.next

    def search(self, x):
        current = self.head
        found = False
        while current and not found:
            if current.data == x:
                found = True
            else:
                current = current.next
        return found

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next