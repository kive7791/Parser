import unittest # using module for better readability and maintainability of test cases
from Parser import parse, tokenize

# Using assertions to automatically check whether the output of the parser matches the expected results

# Define test cases: (input, expected_output)
test_cases = [
    ("a", "'a'"),
    ("a*", "star('a')"),
    ("a|b", "union('a', 'b')"),
    ("ab", "concat('a', 'b')"),
    ("(a|b)*", "star(union('a', 'b'))"),
    ("a|b*c", "union('a', concat(star('b'), 'c'))"),
    ("", ValueError),  # Expect an error for empty input
    ("a**", ValueError),  # Invalid double star
    ("(a", ValueError),  # Missing closing parenthesis
]

# Run tests
for regex, expected in test_cases:
    try:
        tokens = tokenize(regex)
        ast = parse(tokens)
        result = repr(ast)  # Use repr to get a string representation
        assert result == expected, f"Test failed for '{regex}': {result} != {expected}"
        print(f"Test passed for: '{regex}'")
    except Exception as e:
        if isinstance(expected, type) and isinstance(e, expected):
            print(f"Test passed for: '{regex}' (raised {expected.__name__} as expected)")
        else:
            print(f"Test failed for '{regex}': {e}")

# Start of Parser Test 

class TestParser(unittest.TestCase):

    def test_simple_cases(self):
        self.assertEqual(repr(parse(tokenize("a"))), "'a'")
        self.assertEqual(repr(parse(tokenize("a*"))), "star('a')")
        self.assertEqual(repr(parse(tokenize("a|b"))), "union('a', 'b')")

    def test_complex_cases(self):
        self.assertEqual(repr(parse(tokenize("ab"))), "concat('a', 'b')")
        self.assertEqual(repr(parse(tokenize("(a|b)*"))), "star(union('a', 'b'))")

    def test_edge_cases(self):
        with self.assertRaises(ValueError):
            parse(tokenize(""))
        with self.assertRaises(ValueError):
            parse(tokenize("a**"))
        with self.assertRaises(ValueError):
            parse(tokenize("(a"))

if __name__ == "__main__":
    unittest.main()