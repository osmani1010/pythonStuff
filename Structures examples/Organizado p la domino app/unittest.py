# tests/test_domino.py
import unittest

class TestDomino(unittest.TestCase):
    def test_valid_domino_creation(self):
        domino = Domino(3, 4)
        self.assertEqual(domino.value1, 3)
        self.assertEqual(domino.value2, 4)
        
    def test_invalid_domino_values(self):
        with self.assertRaises(ValueError):
            Domino(8, 9)