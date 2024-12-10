# Defining The parser
class Node:
    def __init__(self, type, left=None, right=None):
        self.type = type  # 'union', 'concat', 'star', 'char'
        self.left = left
        self.right = right
    
    # Mainly for my outputs, so that it is clear what is being done
    def __repr__(self):
        if self.type == 'char':
            return f"'{self.left}'"
        if self.type == 'star':
            return f"star({self.left})"
        if self.type == 'concat':
            return f"concat({self.left}, {self.right})"
        if self.type == 'union':
            return f"union({self.left}, {self.right})"
        return self.type

def parse(tokens):
    if not tokens:
        raise ValueError("Input regex cannot be empty")
    
    def regex():
        term_node = term()
        if tokens and tokens[0] == '|':
            tokens.pop(0)  # Consume '|'
            return Node('union', term_node, regex())
        return term_node

    def term():
        factors = []
        while tokens and tokens[0] not in {')', '|'}:
            factors.append(factor())
        if len(factors) == 1:
            return factors[0]
        # Combine all factors into a single concatenation node
        node = factors[0]
        for f in factors[1:]:
            node = Node('concat', node, f)
        return node

    def factor():
        base_node = base()
        if tokens and tokens[0] == '*':
            tokens.pop(0)  # Consume '*'
            return Node('star', base_node)
        return base_node

    def base():
        if tokens[0] == '(':
            tokens.pop(0)  # Consume '('
            node = regex()
            if not tokens or tokens[0] != ')':
                raise ValueError("Missing closing parenthesis")
            tokens.pop(0)  # Consume ')'
            return node
        elif tokens[0].isalnum():
            return Node('char', tokens.pop(0))
        else:
            raise ValueError(f"Unexpected token: {tokens[0]}")

    return regex()


# Implementation of the tokenizer
def tokenize (regex):
    if not regex:
        raise ValueError("Input regex cannot be empty")

    token = []
    for char in regex:
        if char in {'|', '*', '(', ')'}:
            token.append(char)
        # Check if the string is alphanumerical (i.e there is no spaces, puncuations, or special characters)
        elif char.isalnum(): 
            token.append(char)
        else:
            raise ValueError(f"Unexpected character: {char}")
    return token
