from collections import deque


class Stack:
    """ Wrapper class around deque that only allows
        user to push/pop on the right
    """
    def __init__(self, iterable=[]):
        self._deque = deque(iterable)

    def pop(self):
        self._deque.pop()

    def push(self, elem):
        self._deque.append(elem)
