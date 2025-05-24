# interpreter/parser.py

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            tok_type, _ = self.tokens[self.pos]
            if tok_type == "PRINT":
                self.pos += 1
                expr = self.bool_expr()
                statements.append(("PRINT", expr))
            elif tok_type == "IDENT" and self.peek("ASSIGN"):
                name = self.tokens[self.pos][1]
                self.pos += 2
                expr = self.bool_expr()
                statements.append(("ASSIGN", name, expr))
            elif tok_type == "IDENT" and self.peek("LPAREN"):
                statements.append(self.parse_call())
            elif tok_type == "IF":
                statements.append(self.parse_if())
            elif tok_type == "WHILE":
                statements.append(self.parse_while())
            else:
                raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")
        return statements

    def peek(self, kind):
        return (self.pos + 1 < len(self.tokens)
                and self.tokens[self.pos + 1][0] == kind)

    def match(self, kind):
        if (self.pos < len(self.tokens)
            and self.tokens[self.pos][0] == kind):
            self.pos += 1
            return True
        return False

    def parse_block(self):
        if not self.match("LBRACE"):
            raise SyntaxError("Expected '{'")
        stmts = []
        while not self.match("RBRACE"):
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        tok_type, _ = self.tokens[self.pos]
        if tok_type == "PRINT":
            self.pos += 1
            expr = self.bool_expr()
            return ("PRINT", expr)
        elif tok_type == "IDENT" and self.peek("ASSIGN"):
            name = self.tokens[self.pos][1]
            self.pos += 2
            expr = self.bool_expr()
            return ("ASSIGN", name, expr)
        elif tok_type == "IDENT" and self.peek("LPAREN"):
            return self.parse_call()
        elif tok_type == "IF":
            return self.parse_if()
        elif tok_type == "WHILE":
            return self.parse_while()
        else:
            raise SyntaxError(f"Unexpected token in block: {self.tokens[self.pos]}")

    def parse_call(self):
        # IDENT '(' [args] ')'
        name = self.tokens[self.pos][1]
        self.pos += 1
        if not self.match("LPAREN"):
            raise SyntaxError("Expected '(' after function name")
        args = []
        if not self.match("RPAREN"):
            args.append(self.bool_expr())
            while self.match("COMMA"):
                args.append(self.bool_expr())
            if not self.match("RPAREN"):
                raise SyntaxError("Expected ')' after function args")
        return ("CALL", name, args)

    def parse_if(self):
        self.match("IF")
        if not self.match("LPAREN"):
            raise SyntaxError("Expected '(' after 'if'")
        cond = self.bool_expr()
        if not self.match("RPAREN"):
            raise SyntaxError("Expected ')' after if condition")
        then_blk = self.parse_block()
        else_blk = None
        if self.match("ELSE"):
            else_blk = self.parse_block()
        return ("IF", cond, then_blk, else_blk)

    def parse_while(self):
        self.match("WHILE")
        if not self.match("LPAREN"):
            raise SyntaxError("Expected '(' after 'while'")
        cond = self.bool_expr()
        if not self.match("RPAREN"):
            raise SyntaxError("Expected ')' after while condition")
        body = self.parse_block()
        return ("WHILE", cond, body)

    def bool_expr(self):
        node = self.compare_expr()
        while (self.pos < len(self.tokens)
               and self.tokens[self.pos][0] in ("AND", "OR")):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.compare_expr()
            node = (op, node, right)
        return node

    def compare_expr(self):
        node = self.expr()
        comps = []
        while (self.pos < len(self.tokens)
               and self.tokens[self.pos][0] in ("EQ","NEQ","LT","GT","LE","GE")):
            op = self.tokens[self.pos][0]
            self.pos += 1
            rhs = self.expr()
            comps.append((op, rhs))
        return ("CHAIN", node, comps) if comps else node

    def expr(self):
        node = self.term()
        while (self.pos < len(self.tokens)
               and self.tokens[self.pos][0] in ("PLUS","MINUS")):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.term()
            node = (op, node, right)
        return node

    def term(self):
        node = self.factor()
        while (self.pos < len(self.tokens)
               and self.tokens[self.pos][0] in ("MUL","DIV","MOD")):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        tok_type, tok_val = self.tokens[self.pos]

        # unary minus
        if tok_type == "MINUS":
            self.pos += 1
            expr = self.factor()
            return ("NEG", expr)

        # input(...) builtin
        if tok_type == "INPUT":
            self.pos += 1
            if not self.match("LPAREN"):
                raise SyntaxError("Expected '(' after 'input'")
            prompt = self.bool_expr()
            if not self.match("RPAREN"):
                raise SyntaxError("Expected ')' after input call")
            return ("INPUT", prompt)

        # list literal
        if tok_type == "LBRACKET":
            self.pos += 1
            elems = []
            if not self.match("RBRACKET"):
                elems.append(self.bool_expr())
                while self.match("COMMA"):
                    elems.append(self.bool_expr())
                if not self.match("RBRACKET"):
                    raise SyntaxError("Expected ']' in list literal")
            return ("LIST", elems)

        # primary literals and variables
        if tok_type == "NUMBER":
            self.pos += 1
            return ("NUMBER", tok_val)
        if tok_type == "STRING":
            self.pos += 1
            return ("STRING", tok_val)
        if tok_type == "TRUE":
            self.pos += 1
            return ("BOOL", True)
        if tok_type == "FALSE":
            self.pos += 1
            return ("BOOL", False)
        if tok_type == "IDENT":
            self.pos += 1
            node = ("VAR", tok_val)
        elif tok_type == "NOT":
            self.pos += 1
            expr = self.factor()
            node = ("NOT", expr)
        elif tok_type == "LPAREN":
            self.pos += 1
            node = self.bool_expr()
            if not self.match("RPAREN"):
                raise SyntaxError("Missing closing parenthesis")
        else:
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

        # array indexing
        while self.match("LBRACKET"):
            idx = self.bool_expr()
            if not self.match("RBRACKET"):
                raise SyntaxError("Expected ']' after index")
            node = ("INDEX", node, idx)

        return node
