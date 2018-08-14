
class Buffer:
	def __init__(self, size, start_val):
		self._size = size
		self.start_val = list(start_val)

import unittest as ut

class BufferTest(ut.TestCase):
	def testCreation(self):
		b = Buffer(10, 'hello')
		self.

if __name__ == '__main__':
	ut.main()