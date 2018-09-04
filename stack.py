from collections import deque
import unittest as ut


class Stack:
    """ Wrapper class around deque that only allows
        user to push/pop on the right
    """
    def __init__(self, iterable=[]):
        self._deque = deque(iterable)

    def __iter__(self):
        while self._deque:
            yield self.pop()

    def pop(self):
        return self._deque.pop()

    def top(self):
        return self._deque[-1]

    def push(self, *args):
        for elem in args:
            self._deque.append(elem)


class StackTest(ut.TestCase):
    def test_accepts_variable_inputs(self):
        s = Stack()
        s.push(*[2, 4, 6])
        actual = []
        for elem in s:
            actual.append(elem)
        self.assertListEqual(actual, [6, 4, 2])


if __name__ == '__main__':
    ut.main()
