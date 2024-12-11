# Defining The parser
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
