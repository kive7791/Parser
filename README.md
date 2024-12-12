# Regular Expression Interpreter
### Introduction
Welcome to the Regular Expression Interpreter project! This project is part of a Theory of Computation course and aims to build an interpreter that converts regular expressions (regex) into finite automata, specifically Non-deterministic Finite Automata (NFA). This interpreter demonstrates the practical applications of automata theory and highlights the computational aspects of regex.

## Motivation
The significance of this project lies in its ability to bridge theoretical computation concepts with practical software tools. Regex is widely used in various computing tasks such as data validation, search engines, and syntax parsing. This project explores the connection between regex, automata theory, and computational limits, making it directly relevant to our coursework.

### Features
- Parser: Converts regex strings into an Abstract Syntax Tree (AST) to illustrate the structure.
- NFA Construction: Implements Thompson’s construction algorithm to translate regex into an NFA.
- Menu: Provides interactive options to create, view, and manipulate NFAs and Parse regex language.

## Video Demonstration
[Download Demo Video](Parser_NFA.mp4)
## Installation
Clone the repository:
- git clone https://github.com/kive7791/Parser.git
- Ensure you have Python installed (Python 3.6 or later).

Run the Menu.py file:
- python3 Menu.py

### Usage of the Main Menu
Options:
- Parser: Input a regex to see its AST.
- NFA Menu: Interact with and manipulate NFAs.
- Combo: Combine parsing and NFA generation.
- Exit: Close the menu.

#### NFA Menu Options:
- Display Current NFA: Shows the NFA's states, transitions, and accept states.
- Add State: Add new states to the NFA.
- Add Transition: Define transitions between states.
- Set Start State: Define the start state.
- Add Accept State: Add accept states.
- Simulate NFA: Test input strings against the NFA.
- Back to Main Menu: Return to the main menu.

## Bibliography
Rabin, M. O., & Scott, D. (1959). Finite Automata and Their Decision Problems. IBM Journal of Research and Development, 3(2), 114-125. https://doi.org/10.1147/rd.32.0114

Thompson, K. (1968). Programming Techniques: Regular Expression Search Algorithm. Communications of the ACM, 11(6), 419–422. https://doi.org/10.1145/363347.363387