from Parser import Parser
from NFA import NFA

# Defining The Interactive Menu
class Menu:
    nfa = NFA()  # Create a single NFA instance for the session

    @staticmethod
    def show_main_menu():
        print("\nMain Menu:")
        print("1. Parser")
        print("2. NFA Menu")
        print("3. Combo")
        print("4. Exit")

    @staticmethod
    def show_nfa_menu():
        print("\nNFA Menu:")
        print("1. Display Current NFA")
        print("2. Add State")
        print("3. Add Transition")
        print("4. Set Start State")
        print("5. Add Accept State")
        print("6. Simulate NFA")
        print("7. Back to Main Menu")

    @staticmethod
    def get_choice():
        while True:
            try:
                choice = int(input("Enter your choice: "))
                return choice
            except ValueError:
                print("Invalid input. Please enter a number.")

    @staticmethod
    def handle_main_choice(choice):
        if choice == 1:
            print("You chose Option 1, Parser")
            regex = input("Please provide a regex operation: ")
            try:
                parser = Parser(regex)
                ast = parser.parse()
                print("Parsed AST:", ast)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == 2:
            Menu.nfa_menu()

        elif choice == 3:
            print("You chose Option 3, Combination of both Parser and NFA. \nNFA creation from AST is a work in progress.")
            regex = input("Please provide a regex operation: ")
            try:
                parser = Parser(regex)
                ast = parser.parse()
                print("Parsed AST:", ast)
                nfa = parser.to_nfa(ast)
                print("Generated NFA:", nfa)
            except ValueError as e:
                print(f"Error: {e}")                
        elif choice == 4:
            print("Exiting...")
            return True  # Return True to exit the loop
        else:
            print("Invalid choice. Please try again.")
        return False  # Return False to continue the loop

    @staticmethod
    def handle_nfa_choice(choice):
        if choice == 1:
            print("Current NFA:")
            print(Menu.nfa)

        elif choice == 2:
            state = input("Enter the state to add: ")
            Menu.nfa.add_state(state)
            print(f"State '{state}' added to the NFA.")

        elif choice == 3:
            from_state = input("Enter the from state: ")
            to_state = input("Enter the to state: ")
            symbol = input("Enter the transition symbol: ")
            Menu.nfa.add_transition(from_state, to_state, symbol)
            print(f"Transition from '{from_state}' to '{to_state}' on symbol '{symbol}' added.")

        elif choice == 4:
            start_state = input("Enter the start state: ")
            Menu.nfa.set_start_state(start_state)
            print(f"Start state set to '{start_state}'.")

        elif choice == 5:
            accept_state = input("Enter the accept state: ")
            Menu.nfa.add_accept_state(accept_state)
            print(f"Accept state '{accept_state}' added to the NFA.")

        elif choice == 6:
            input_str = input("Enter a string to simulate the NFA: ")
            result = Menu.nfa.simulate(input_str)
            print("Simulation result:", "Accepted" if result else "Rejected")

        elif choice == 7:
            return True  # Return True to go back to main menu
        else:
            print("Invalid choice. Please try again.")
        return False  # Return False to continue the NFA menu loop

    @staticmethod
    def main():
        while True:
            Menu.show_main_menu()
            choice = Menu.get_choice()
            if Menu.handle_main_choice(choice):
                break

    @staticmethod
    def nfa_menu():
        while True:
            Menu.show_nfa_menu()
            choice = Menu.get_choice()
            if Menu.handle_nfa_choice(choice):
                break

if __name__ == "__main__":
    Menu.main()