class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            tok_type, tok_val = self.tokens[self.pos]
            if tok_type == "PRINT":
                self.pos += 1
                expr = self.bool_expr()
                statements.append(("PRINT", expr))
            elif tok_type == "IDENT" and self.peek("ASSIGN"):
                name = tok_val
                self.pos += 2  # skip IDENT and ASSIGN
                expr = self.bool_expr()
                statements.append(("ASSIGN", name, expr))
            else:
                raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")
        return statements

    def peek(self, kind):
        return (self.pos + 1 < len(self.tokens)) and (self.tokens[self.pos + 1][0] == kind)

    def bool_expr(self):
        node = self.compare_expr()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("AND", "OR"):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.compare_expr()
            node = (op, node, right)
        return node

    def compare_expr(self):
        node = self.expr()
        comparisons = []
        
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("EQ", "NEQ", "LT", "GT", "LE", "GE"):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.expr()
            comparisons.append((op, right))
        if comparisons:
            return ("CHAIN", node, comparisons)
        return node


    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("PLUS", "MINUS"):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.term()
            node = (op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("MUL", "DIV"):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        token_type, token_value = self.tokens[self.pos]
        # Unary minus
        if token_type == "MINUS":
            self.pos += 1
            expr = self.factor()
            return ("NEG", expr)
        if token_type == "NUMBER":
            self.pos += 1
            return ("NUMBER", token_value)
        elif token_type == "STRING":
            self.pos += 1
            return ("STRING", token_value)
        elif token_type == "TRUE":
            self.pos += 1
            return ("BOOL", True)
        elif token_type == "FALSE":
            self.pos += 1
            return ("BOOL", False)
        elif token_type == "IDENT":
            self.pos += 1
            return ("VAR", token_value)
        elif token_type == "NOT":
            self.pos += 1
            expr = self.factor()
            return ("NOT", expr)
        elif token_type == "LPAREN":
            self.pos += 1
            expr = self.bool_expr()
            if self.pos >= len(self.tokens) or self.tokens[self.pos][0] != "RPAREN":
                raise SyntaxError("Missing closing parenthesis")
            self.pos += 1
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")