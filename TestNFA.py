# Test Suite with Automated Validation
import unittest
from NFA import NFA

class TestRegexInterpreter(unittest.TestCase):
    def setUp(self):
        self.nfa = NFA()

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
