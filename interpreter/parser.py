class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][0] == "PRINT":
            self.pos += 1
            return ("PRINT", self.bool_expr())
        else:
            return self.bool_expr()

    def bool_expr(self):
        node = self.compare_expr()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("AND", "OR"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.compare_expr()
            node = (op[0], node, right)
        return node

    def compare_expr(self):
        node = self.expr()
        comparisons = []

        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("EQ", "NEQ", "LT", "GT", "LE", "GE"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.expr()
            comparisons.append((op[0], right))

        if comparisons:
            return ("CHAIN", node, comparisons)
        else:
            return node


    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("PLUS", "MINUS"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.term()
            node = (op[0], node, right)
        return node

    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("MUL", "DIV"):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.factor()
            node = (op[0], node, right)
        return node

    def factor(self):
        if self.tokens[self.pos][0] == "NOT":
            self.pos += 1
            if self.tokens[self.pos][0] == "LPAREN":
                self.pos += 1
                node = self.bool_expr()
                if self.tokens[self.pos][0] != "RPAREN":
                    raise SyntaxError("Missing closing parenthesis")
                self.pos += 1
                return ("NOT", node)
            else:
                node = self.factor()
                return ("NOT", node)

        elif self.tokens[self.pos][0] == "TRUE":
            self.pos += 1
            return ("BOOL", True)

        elif self.tokens[self.pos][0] == "FALSE":
            self.pos += 1
            return ("BOOL", False)

        elif self.tokens[self.pos][0] == "MINUS":
            self.pos += 1
            node = self.factor()
            return ("NEGATE", node)

        elif self.tokens[self.pos][0] == "NUMBER":
            value = self.tokens[self.pos][1]
            self.pos += 1
            return ("NUMBER", value)

        elif self.tokens[self.pos][0] == "LPAREN":
            self.pos += 1
            node = self.bool_expr()
            if self.tokens[self.pos][0] != "RPAREN":
                raise SyntaxError("Missing closing parenthesis")
            self.pos += 1
            return node
        elif self.tokens[self.pos][0] == "STRING":
            value = self.tokens[self.pos][1][1:-1]  # remove quotes
            self.pos += 1
            return ("STRING", value)
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")