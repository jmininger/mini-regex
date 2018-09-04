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

    def __len__(self):
        return len(self._deque)

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

    def test_gets_size(self):
        s = Stack()
        s.push(1, 3, 5, 7, 9)
        self.assertEqual(len(s), 5)

    def test_evaluates_to_false_when_empty(self):
        s = Stack()
        s.push(5)
        self.assertTrue(s)
        s.pop()
        self.assertFalse(s)


if __name__ == '__main__':
    ut.main()
