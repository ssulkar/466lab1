import unittest
import alg

class TestDecisionTree(unittest.TestCase):
    def test_split(self):
        D = [[]]
        expect = alg.split(D, A, 3)
        self.assertEqual('', expect)

if __name__ == '__main__':
    unittest.main()