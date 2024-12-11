# Test Suite with Automated Validation
import unittest
from Parser import Parser

# Using assertions to automatically check whether the output of the parser matches the expected results
class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser("ab")

    # Expect an error for empty input
    def test_empty_input(self):
        self.parser.regex = ""
        with self.assertRaises(ValueError):
            self.parser.tokenize()

    # Missing closing parenthesis
    def test_invalid_regex(self):
        invalid_regex = "(a|b"
        self.parser.regex = invalid_regex
        with self.assertRaises(ValueError):
            self.parser.parse()

    # Invalid double star
    def test_invalid_regex_star(self):
        invalid_regex = "a**"
        self.parser.regex = invalid_regex
        with self.assertRaises(ValueError):
            self.parser.parse()

    def test_simple_regex_a(self):
        self.parser.regex = "a"
        sol:tuple = ('Literal', 'a')
        ast = self.parser.parse()
        self.assertEqual(ast, sol)

    def test_simple_regex_a_star(self):
        self.parser.regex = "a*"
        sol:tuple = ('Star', ('Literal', 'a'))
        ast = self.parser.parse()
        self.assertEqual(ast, sol)

    def test_simple_regex_a_u_b(self):
        self.parser.regex = "a|b"
        sol:tuple = ('Union', ('Literal', 'a'), ('Literal', 'b'))
        ast = self.parser.parse()
        self.assertEqual(ast, sol)

    def test_simple_regex_a_n_b(self):
        self.parser.regex = "ab"
        sol:tuple = ('Concat', ('Literal', 'a'), ('Literal', 'b'))
        ast = self.parser.parse()
        self.assertEqual(ast, sol)

    def test_simple_regex_a_u_b_star(self):
        self.parser.regex = "(a|b)*"
        sol:tuple = ('Star', ('Union', ('Literal', 'a'), ('Literal', 'b')))
        ast = self.parser.parse()
        self.assertEqual(ast, sol)

    def test_simple_regex_a_u_b_star_c(self):
        self.parser.regex = "a|b*c"
        sol:tuple = ('Union', ('Literal', 'a'), ('Concat', ('Star', ('Literal', 'b')), ('Literal', 'c')))
        ast = self.parser.parse()
        self.assertEqual(ast, sol)

if __name__ == "__main__":
    unittest.main()
