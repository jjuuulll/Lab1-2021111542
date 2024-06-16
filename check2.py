import unittest
from lab import calcShortestPath

class TestMathModule(unittest.TestCase):
    def test_1(self):
        self.assertEqual(calcShortestPath("to","and",None,1), 
                         "show_all_two_words")
    def test_2(self):
        self.assertEqual(calcShortestPath("to","and",None,None), 
                         "show_one_two_words")
    def test_3(self):
        self.assertEqual(calcShortestPath("civilizations","to",None,None), 
                         "It's impossible to reach to from civilizations")
    def test_4(self):
        self.assertEqual(calcShortestPath("to",None,1,1), 
                         "show_all_one_word")
    def test_5(self):
        self.assertEqual(calcShortestPath("to",None,1,None), 
                         "show_one_one_word")
    def test_6(self):
        self.assertEqual(calcShortestPath("civilizations",None,1,None), 
                         "It's impossible to reach to from civilizations")
    def test_7(self):
        self.assertEqual(calcShortestPath("civilizations",None,1,1), 
                         "It's impossible to reach to from civilizations")

if __name__ == '__main__':
    unittest.main(verbosity=2)
    
