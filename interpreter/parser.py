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
            elif tok_type == "IF":
                statements.append(self.parse_if())
            elif tok_type == "WHILE":
                statements.append(self.parse_while())
            else:
                raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")
        return statements

    def peek(self, kind):
        return (self.pos + 1 < len(self.tokens)) and (self.tokens[self.pos + 1][0] == kind)

    def match(self, kind):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == kind:
            self.pos += 1
            return True
        return False

    def parse_block(self):
        if not self.match("LBRACE"):
            raise SyntaxError("Expected '{'")
        stmts = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != "RBRACE":
            tok_type = self.tokens[self.pos][0]
            if tok_type == "PRINT":
                self.pos += 1
                expr = self.bool_expr()
                stmts.append(("PRINT", expr))
            elif tok_type == "IDENT" and self.peek("ASSIGN"):
                name = self.tokens[self.pos][1]
                self.pos += 2
                expr = self.bool_expr()
                stmts.append(("ASSIGN", name, expr))
            elif tok_type == "IF":
                stmts.append(self.parse_if())
            elif tok_type == "WHILE":
                stmts.append(self.parse_while())
            else:
                raise SyntaxError(f"Unexpected token in block: {self.tokens[self.pos]}")
        if not self.match("RBRACE"):
            raise SyntaxError("Expected '}'")
        return stmts

    def parse_if(self):
        # parse: IF '(' bool_expr ')' block [ELSE block]
        self.pos += 1  # skip IF
        if not self.match("LPAREN"):
            raise SyntaxError("Expected '(' after 'if'")
        cond = self.bool_expr()
        if not self.match("RPAREN"):
            raise SyntaxError("Expected ')' after if condition")
        then_block = self.parse_block()
        else_block = None
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == "ELSE":
            self.pos += 1
            else_block = self.parse_block()
        return ("IF", cond, then_block, else_block)

    def parse_while(self):
        # parse: WHILE '(' bool_expr ')' block
        self.pos += 1  # skip WHILE
        if not self.match("LPAREN"):
            raise SyntaxError("Expected '(' after 'while'")
        cond = self.bool_expr()
        if not self.match("RPAREN"):
            raise SyntaxError("Expected ')' after while condition")
        body = self.parse_block()
        return ("WHILE", cond, body)

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
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ("MUL", "DIV", "MOD"):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        token_type, token_value = self.tokens[self.pos]
        # unary minus
        if token_type == "MINUS":
            self.pos += 1
            expr = self.factor()
            return ("NEG", expr)
        # input builtin
        if token_type == "INPUT":
            self.pos += 1
            if not self.match("LPAREN"):
                raise SyntaxError("Expected '(' after 'input'")
            prompt = self.bool_expr()
            if not self.match("RPAREN"):
                raise SyntaxError("Expected ')' after input call")
            return ("INPUT", prompt)
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
            if not self.match("RPAREN"):
                raise SyntaxError("Missing closing parenthesis")
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

