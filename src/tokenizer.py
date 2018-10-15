import unittest as ut

class TokenizerTest(ut.TestCase):
    def setUp():
        self.pattern = 'hi (Jon|Tom)!*'

    def test_recognizes_various_tokens_in_stream(self):
        tknzr = Tokenizer(self.pattern)
        tknzr.next()

if __name__ == '__main__':
    ut.main()
