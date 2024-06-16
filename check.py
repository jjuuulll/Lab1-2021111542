import unittest
from lab import queryBridgeWords

class TestMathModule(unittest.TestCase):
    def test_1(self):
        self.assertEqual(queryBridgeWords("to", "new"), 
                         "The bridge words from \"to\" to \"new\" are: seek, and day")
    def test_2(self):
        self.assertEqual(queryBridgeWords("to", ""), "No \"\" in the graph!")
    def test_3(self):
        self.assertEqual(queryBridgeWords("got", "new"), "No \"got\" in the graph!")
    def test_4(self):
        self.assertEqual(queryBridgeWords("got", "sad233"), "No \"got\" and \"sad233\" in the graph!")
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
