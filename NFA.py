# NFA class represents a Non-deterministic Finite Automaton
# has states ( A set of all states in the NFA), and transitions (a dic map
# states to possible transitions.)
class NFA:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start_state = None # The initial state of the NFA
        self.accept_states = set() # The final(accepting) state of the NFA

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
        return (f"NFA(states={self.states}, start_state={self.start_state}, accept_states={self.accept_states}, "
                f"transitions={self.transitions})")
