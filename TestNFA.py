import unittest
from NFA import nfa_for_char, nfa_for_concat, nfa_for_union, nfa_for_star

class TestNFA(unittest.TestCase):

    def test_nfa_for_char(self):
        nfa = nfa_for_char('a')
        self.assertEqual(nfa.states, {'q0', 'q1'})
        self.assertEqual(nfa.transitions, {'q0': {'a': {'q1'}}})
        self.assertEqual(nfa.start_state, 'q0')
        self.assertEqual(nfa.accept_state, 'q1')

    def test_nfa_for_star(self):
        nfa = nfa_for_char('a')
        nfa = nfa_for_star(nfa)
        self.assertIn('q_star_start', nfa.states)
        self.assertIn('q_star_end', nfa.states)
        self.assertIn('q_star_end', nfa.transitions.get('q_star_start', {}).get('ε', {}))
        self.assertIn('q_star_start', nfa.transitions.get('q1', {}).get('ε', {}))

    def test_nfa_for_union(self):
        nfa1 = nfa_for_char('a')
        nfa2 = nfa_for_char('b')
        nfa = nfa_for_union(nfa1, nfa2)
        
        # Verify states
        assert 'q_start' in nfa.states, "Start state is missing in the NFA states"
        assert 'q_end' in nfa.states, "End state is missing in the NFA states"

        # Verify transitions from q_start
        assert 'ε' in nfa.transitions['q_start'], "No epsilon transitions from q_start"
        assert nfa1.start_state in nfa.transitions['q_start']['ε'], "Missing epsilon transition to nfa1's start state"
        assert nfa2.start_state in nfa.transitions['q_start']['ε'], "Missing epsilon transition to nfa2's start state"

        # Renamed accept states for nfa1 and nfa2 (to handle state name conflicts after combining)
        renamed_nfa1_accept_state = nfa1.accept_state
        renamed_nfa2_accept_state = nfa2.accept_state

        # Verify epsilon transitions to the unified accept state
        assert 'ε' in nfa.transitions[renamed_nfa1_accept_state], "No epsilon transitions from nfa1's accept state"
        assert 'ε' in nfa.transitions[renamed_nfa2_accept_state], "No epsilon transitions from nfa2's accept state"
        assert nfa.accept_state in nfa.transitions[renamed_nfa1_accept_state]['ε'], "Missing epsilon transition from nfa1's accept state to union's accept state"
        assert nfa.accept_state in nfa.transitions[renamed_nfa2_accept_state]['ε'], "Missing epsilon transition from nfa2's accept state to union's accept state"

        print("All tests passed.")
    
    def test_nfa_for_concat(self):
        nfa1 = nfa_for_char('a')
        nfa2 = nfa_for_char('b')
        # Concatenate the two NFAs
        concatenated_nfa = nfa_for_concat(nfa1, nfa2)
        
        # Check that the start state of the concatenated NFA is the start state of nfa1
        assert concatenated_nfa.start_state == nfa1.start_state, "Start state mismatch in concatenated NFA."
        
        # Check that the accept state of the concatenated NFA is the accept state of nfa2
        assert concatenated_nfa.accept_state == nfa2.accept_state, "Accept state mismatch in concatenated NFA."
        
        # Verify that there is an epsilon transition from nfa1's accept state to nfa2's start state
        assert 'ε' in concatenated_nfa.transitions[nfa1.accept_state], "Epsilon transition missing from nfa1's accept state."
        assert nfa2.start_state in concatenated_nfa.transitions[nfa1.accept_state]['ε'], "Epsilon transition target incorrect."
        
        # Verify that the set of states in the concatenated NFA is the union of states from nfa1 and nfa2
        expected_states = nfa1.states.union(nfa2.states)
        assert concatenated_nfa.states == expected_states, "States in concatenated NFA do not match expected states."
        
        # Verify that all transitions from nfa1 are correctly present in the concatenated NFA
        for state in nfa1.transitions:
            assert state in concatenated_nfa.transitions, f"State {state} from nfa1 missing in concatenated NFA."
            assert nfa1.transitions[state] == concatenated_nfa.transitions[state], f"Transitions for state {state} do not match."
        
        # Verify that all transitions from nfa2 are correctly present in the concatenated NFA
        for state in nfa2.transitions:
            assert state in concatenated_nfa.transitions, f"State {state} from nfa2 missing in concatenated NFA."
            assert nfa2.transitions[state] == concatenated_nfa.transitions[state], f"Transitions for state {state} do not match."
        
        print("All tests passed.")


if __name__ == "__main__":
    unittest.main()

# Old code for concat:

    # nfa = nfa_for_concat(nfa1, nfa2)

    # # Verify states
    # self.assertIn('q0', nfa.states)
    # self.assertIn('q1', nfa.states)
    # self.assertIn('q2', nfa.states)

    # # Check transitions
    # self.assertIn(nfa1.accept_state, nfa.transitions)
    # self.assertIn(nfa2.start_state, nfa.transitions.get(nfa1.accept_state, {}).get('ε', {}))

    # # Verify start and accept states
    # self.assertEqual(nfa.start_state, 'q0')
    # self.assertEqual(nfa.accept_state, nfa2.accept_state)

# Old code for Union:
    # Verify states]
        # self.assertIn('q_start', nfa.states)
        # self.assertIn('q_end', nfa.states)

        # # Check transitions from q_start
        # renamed_nfa1_accept_state = nfa1.accept_state
        # renamed_nfa2_accept_state = nfa2.accept_state

        # self.assertIn(nfa.accept_state, nfa.transitions[renamed_nfa1_accept_state]["ε"])
        # self.assertIn(nfa.accept_state, nfa.transitions[renamed_nfa2_accept_state]["ε"])