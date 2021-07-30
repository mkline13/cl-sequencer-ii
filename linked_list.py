

class LinkedList:
    def __init__(self, value):
        self.value = value
        self.head = self
        self.foot = self
        self.prev = None
        self.next = None

    def insert_after(self, value):
        new_link = LinkedList(value)

        new_link.head = self.head
        new_link.prev = self
        new_link.next = self.next

        if new_link.next is not None:
            new_link.next.prev = new_link

        if self.foot is self:
            new_link.foot = new_link
            self.foot = new_link
        else:
            new_link.foot = self.foot

        self.next = new_link

    def items(self):
        link = self.head

        while link is not None:
            yield link
            link = link.next

    def __repr__(self):
        return f"LinkedList({self.value})"


if __name__ == '__main__':
    x = LinkedList(0)
    x.insert_after(3)
    x.insert_after(2)
    x.insert_after(1)
    for i in x.items():
        print(i.value, i.head, i.foot, i.prev, i.next)
