import unittest
from src.power import evaluate

class TestCalculator(unittest.TestCase):

    def test_basic_operations(self):
        self.assertEqual(evaluate("2+3"), 5)
        self.assertEqual(evaluate("5-2"), 3)
        self.assertEqual(evaluate("4*3"), 12)
        self.assertEqual(evaluate("10/2"), 5.0)

    def test_precedence(self):
        self.assertEqual(evaluate("2+3*4"), 14)
        self.assertEqual(evaluate("10-2*3"), 4)

    def test_parentheses(self):
        self.assertEqual(evaluate("(2+3)*4"), 20)
        self.assertEqual(evaluate("2*(3+4)"), 14)

    def test_unary(self):
        self.assertEqual(evaluate("-5"), -5)
        self.assertEqual(evaluate("--5"), 5)
        self.assertEqual(evaluate("-(2+3)"), -5)
        self.assertEqual(evaluate("+5"), 5)

    def test_power(self):
        self.assertEqual(evaluate("2**3"), 8)
        self.assertEqual(evaluate("2**3**2"), 512)

    def test_floor_div_mod(self):
        self.assertEqual(evaluate("7//2"), 3)
        self.assertEqual(evaluate("7%2"), 1)

    def test_floats(self):
        self.assertAlmostEqual(evaluate("3.5+2.1"), 5.6, places=1)

    def test_errors(self):
        with self.assertRaises(ValueError):
            evaluate("5/0")
        with self.assertRaises(ValueError):
            evaluate("5//0")
        with self.assertRaises(ValueError):
            evaluate("5%0")
        with self.assertRaises(ValueError):
            evaluate("5//2.0")
        with self.assertRaises(ValueError):
            evaluate("2+")
        with self.assertRaises(ValueError):
            evaluate("(2+3")

def test_power_and_floor_div(self):
    self.assertEqual(evaluate("2**3"), 8)
    self.assertEqual(evaluate("8//3"), 2)
    self.assertEqual(evaluate("10%3"), 1)
    self.assertEqual(evaluate("2**3**2"), 512)

def test_floor_div_and_mod_with_floats(self):
    self.assertEqual(evaluate("8.0 // 2"), 4.0)
    self.assertEqual(evaluate("10 % 3.0"), 1.0)
    self.assertEqual(evaluate("(9 / 3) // 1"), 3.0)
    self.assertEqual(evaluate("7.0 % 2"), 1.0)

def test_floor_div_mod_non_integer_error(self):
    with self.assertRaises(ValueError):
        evaluate("7.5 // 2")
    with self.assertRaises(ValueError):
        evaluate("10 % 3.2")

if __name__ == '__main__':
    unittest.main()