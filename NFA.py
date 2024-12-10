# NFA class represents a Non-deterministic Finite Automaton
# has states ( A set of all states in the NFA), and transitions (a dic map
# states to possible transitions.)
class NFA:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start_state = None # The initial state of the NFA
        self.accept_state = None # The final(accepting) state of the NFA

#Simple Character(a) NFA creation 
def nfa_for_char(char):
    nfa = NFA()
    start = "q0"
    end = "q1"
    nfa.states = {start, end}
    nfa.transitions = {start: {char: {end}}}
    nfa.start_state = start
    nfa.accept_state = end
    return nfa

# rename states of an NFA to ensure uniquness when combinin NFAs
# Example if nfa.states = {'q0', 'q1'} and offset = 2, renamed states become {'q2', 'q3'}.
def rename_states(nfa, offset):
    """Renames states of an NFA to ensure uniqueness."""
    state_map = {state: f"q{idx + offset}" for idx, state in enumerate(nfa.states)}
    renamed_nfa = NFA()
    renamed_nfa.states = {state_map[state] for state in nfa.states}
    renamed_nfa.start_state = state_map[nfa.start_state]
    renamed_nfa.accept_state = state_map[nfa.accept_state]
    renamed_nfa.transitions = {
        state_map[src]: {key: {state_map[dest] for dest in dests} for key, dests in trans.items()}
        for src, trans in nfa.transitions.items()
    }
    return renamed_nfa


# Concatenation (Intersection) (ab)
# Had an issue before that when concat was being called again for "Update" it was having troubles differentiating between
# The new q0 and the old one
def nfa_for_concat(nfa1, nfa2):
    print("\n", "Entered Concat:", nfa1, " ", nfa2, "\n")
    # Rename states of the second NFA to ensure uniqueness
    offset = len(nfa1.states)
    nfa2 = rename_states(nfa2, offset)

    print("NFA States:", nfa1.states)
    print("NFA States:", nfa2.states)

    # Preserve the original accept state of nfa1
    original_accept_state = nfa1.accept_state

    # Link the original accept state of nfa1 to the start state of renamed nfa2
    if original_accept_state not in nfa1.transitions:
        nfa1.transitions[original_accept_state] = {}
    
    # Add an epsilon trans state
    nfa1.transitions[original_accept_state].setdefault('ε', set()).add(nfa2.start_state)

    # # Update the states and transitions
    # nfa1.states.update(nfa2.states)
    # nfa1.transitions.update(nfa2.transitions)

    # Merge states and transitions
    nfa1.states.update(nfa2.states)
    for state, trans in nfa2.transitions.items():
        if state in nfa1.transitions:
            for symbol, destinations in trans.items():
                nfa1.transitions[state].setdefault(symbol, set()).update(destinations)
        else:
            nfa1.transitions[state] = trans

    # Update the accept state of nfa1 to nfa2's accept state
    nfa1.accept_state = nfa2.accept_state

    print("Transitions:", nfa1.transitions, "Update: ", nfa2.transitions)
    return nfa1

# Union (a|b)
def nfa_for_union(nfa1, nfa2):
    # Rename states of both NFAs to ensure uniqueness
    offset1 = 0
    offset2 = len(nfa1.states)
    nfa1 = rename_states(nfa1, offset1)
    nfa2 = rename_states(nfa2, offset2)

    # print("\n", "Entered Union:", nfa1, " ", nfa2, "\n")
    nfa = NFA()
    start = "q_start"
    end = "q_end"

    nfa.states = {start, end} | nfa1.states | nfa2.states
    # print("NFA States:", nfa.states)
    nfa.transitions = {
        start: {"ε": {nfa1.start_state, nfa2.start_state}},
        nfa1.accept_state: {"ε": {end}},
        nfa2.accept_state: {"ε": {end}},
        **nfa1.transitions,
        **nfa2.transitions
    }
    # print("Transitions from q_start:", nfa.transitions['q_start'])
    nfa.start_state = start
    nfa.accept_state = end
    # print("Start: ", nfa.start_state, "End: ", nfa.accept_state)
    return nfa

# Kleen Star (a*)
# had to add a missing transition to ensure that the Kleene star func allows repeated execution of the NFA.
def nfa_for_star(nfa):
    # print("\n", "Entered Star:", nfa, "\n")
    nfa_with_star = NFA()
    start = "q_star_start"
    end = "q_star_end"

    nfa_with_star.states = {start, end} | nfa.states
    # print("NFA States:", nfa.states)
    nfa_with_star.transitions = {
        start: {"ε": {nfa.start_state, end}},  # Link new start to original start and new end
        nfa.accept_state: {"ε": {nfa.start_state, end, start}},  # Loop back to new start
        **nfa.transitions
    }
    # print("Transitions:", nfa_with_star.transitions)
    nfa_with_star.start_state = start
    nfa_with_star.accept_state = end
    return nfa_with_star
