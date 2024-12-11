class Parser:
    def __init__(self, regex):
        self.regex = regex
        self.tokens = []
        self.current_token = None
        self.open_parens = 0  # Counter to track unmatched parentheses

    def tokenize(self):
        if not self.regex:
            raise ValueError("Input regex cannot be empty")
        self.tokens = list(self.regex)
        self.current_token = self.tokens[0] if self.tokens else None
        return self.tokens

    def parse(self):
        #print(self.regex)
        self.tokenize()
        #print(self.tokens)
        if not self.tokens:
            raise ValueError("No tokens to parse")
        ast = self.regex_expression()
        if self.open_parens != 0:
            raise ValueError("Unmatched parentheses in regex")
        #print(ast)
        return ast

    def regex_expression(self):
        term = self.regex_term()
        if self.current_token == '|':
            self.consume('|')
            # The 'Union' is mainly for my outputs, so that it is clear what is being done
            return ('Union', term, self.regex_expression())
        return term

    def regex_term(self):
        factors = []
        while self.current_token and self.current_token not in ('|', ')'):
            factors.append(self.regex_factor())
        if len(factors) == 1:
            return factors[0]
        # The 'Concat' is mainly for my outputs, so that it is clear what is being done
        return ('Concat', *factors)

    def regex_factor(self):
        base = self.regex_base()
        if self.current_token == '*':
            self.consume('*')
            # The 'Star' is mainly for my outputs, so that it is clear what is being done
            return ('Star', base)
        return base

    def regex_base(self):
        if self.current_token == '(':
            self.consume('(')
            self.open_parens += 1
            expr = self.regex_expression()
            if self.current_token == ')':
                self.consume(')')
                self.open_parens -= 1
            else:
                raise ValueError("Unmatched opening parenthesis")
            return expr
        # Check if the string is alphanumerical (i.e there is no spaces, puncuations, or special characters)
        elif self.current_token and self.current_token.isalnum():
            char = self.current_token
            self.consume(self.current_token)
            # The 'Literal' is mainly for my outputs, so that it is clear what is being done
            return ('Literal', char)
        else:
            raise ValueError(f"Unexpected token: {self.current_token}")

    def consume(self, token):
        if self.tokens and self.tokens[0] == token:
            self.tokens.pop(0) # Consume token
            self.current_token = self.tokens[0] if self.tokens else None
        else:
            raise ValueError(f"Expected {token}, got {self.current_token}")

    def __repr__(self):
        return f"Parser(regex='{self.regex}')"

# Updated NFA Construction to Handle Empty Input
class NFA:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

    def add_state(self, state):
        self.states.add(state)

    def add_transition(self, from_state, to_state, symbol):
        if from_state not in self.transitions:
            self.transitions[from_state] = []
        self.transitions[from_state].append((to_state, symbol))

    def set_start_state(self, state):
        self.start_state = state
        self.add_state(state)

    def add_accept_state(self, state):
        self.accept_states.add(state)
        self.add_state(state)

    def simulate(self, input_string):
        if input_string == "":
            return True if self.start_state in self.accept_states else False

        # Rest of simulation logic
        def epsilon_closure(states):
            stack = list(states)
            closure = set(states)

            while stack:
                state = stack.pop()
                for to_state, symbol in self.transitions.get(state, []):
                    if symbol == "" and to_state not in closure:  # Epsilon transition
                        closure.add(to_state)
                        stack.append(to_state)
            return closure

        def move(states, symbol):
            next_states = set()
            for state in states:
                for to_state, trans_symbol in self.transitions.get(state, []):
                    if trans_symbol == symbol:
                        next_states.add(to_state)
            return next_states

        current_states = epsilon_closure({self.start_state})
        for char in input_string:
            current_states = epsilon_closure(move(current_states, char))

        return bool(current_states & self.accept_states)

    def __repr__(self):
        return (f"NFA(start_state={self.start_state}, accept_states={self.accept_states}, "
                f"transitions={self.transitions})")

# Test Suite with Automated Validation
import unittest

class TestRegexInterpreter(unittest.TestCase):
    def setUp(self):
        self.parser = Parser("ab")
        self.nfa = NFA()

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

    def test_nfa_accept_empty(self):
        self.nfa.set_start_state("q0")
        self.nfa.add_accept_state("q0")
        self.assertTrue(self.nfa.simulate(""), "NFA should accept empty string when start state is accept state")

    def test_nfa_reject_empty(self):
        self.nfa.set_start_state("q0")
        self.nfa.add_state("q1")
        self.nfa.add_accept_state("q1")
        self.assertFalse(self.nfa.simulate(""), "NFA should reject empty string when start state is not accept state")

    def test_single_transition(self):
        self.nfa.set_start_state("q0")
        self.nfa.add_accept_state("q1")
        self.nfa.add_transition("q0", "q1", "a")
        self.assertTrue(self.nfa.simulate("a"), "NFA should accept 'a'.")
        self.assertFalse(self.nfa.simulate("b"), "NFA should not accept 'b'.")

    def test_multiple_transitions(self):
        self.nfa.set_start_state("q0")
        self.nfa.add_state("q1")
        self.nfa.add_accept_state("q2")
        self.nfa.add_transition("q0", "q1", "a")
        self.nfa.add_transition("q1", "q2", "b")
        self.assertTrue(self.nfa.simulate("ab"), "NFA should accept 'ab'.")
        self.assertFalse(self.nfa.simulate("a"), "NFA should not accept 'a'.")

    def test_loop_transition(self):
        self.nfa.set_start_state("q0")
        self.nfa.add_accept_state("q0")
        self.nfa.add_transition("q0", "q0", "a")
        self.assertTrue(self.nfa.simulate(""), "NFA should accept empty string as start state is also an accept state.")
        self.assertTrue(self.nfa.simulate("aaa"), "NFA should accept 'aaa'.")

    def test_nfa_simple_match(self):
        self.nfa.set_start_state("q0")
        self.nfa.add_state("q1")
        self.nfa.add_accept_state("q1")
        self.nfa.add_transition("q0", "q1", "a")
        self.assertTrue(self.nfa.simulate("a"), "NFA should accept 'a'")

    def test_nfa_simple_no_match(self):
        self.nfa.set_start_state("q0")
        self.nfa.add_state("q1")
        self.nfa.add_accept_state("q1")
        self.nfa.add_transition("q0", "q1", "a")
        self.assertFalse(self.nfa.simulate("b"), "NFA should reject 'b'")

if __name__ == "__main__":
    unittest.main()

# # Example Usage
# if __name__ == "__main__":
#     parser = Parser("a|b")
#     ast = parser.parse()
#     print(ast)
