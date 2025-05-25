class Parser:
    def __init__(self, tokens):
        # Start with the list of tokens from the lexer,
        # and a pointer (pos) at the first token.
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        """
        Top‐level loop: read one statement after another
        until we run out of tokens, and return the list of
        parsed statements.
        """
        statements = []
        while self.pos < len(self.tokens):
            tok_type, _ = self.tokens[self.pos]

            if tok_type == "PRINT":
                # Found a 'print' keyword—consume it and parse
                # the expression that follows, then record a PRINT node.
                self.pos += 1
                expr = self.bool_expr()
                statements.append(("PRINT", expr))

            elif tok_type == "IDENT" and self.peek("ASSIGN"):
                # Found something like 'x = ...' — an assignment.
                name = self.tokens[self.pos][1]
                # Skip over IDENT and '='
                self.pos += 2
                expr = self.bool_expr()
                statements.append(("ASSIGN", name, expr))

            elif tok_type == "IDENT" and self.peek("LPAREN"):
                # Found a standalone function call, e.g. append(list, value)
                statements.append(self.parse_call())

            elif tok_type == "IF":
                # Found an if statement
                statements.append(self.parse_if())

            elif tok_type == "WHILE":
                # Found a while loop
                statements.append(self.parse_while())

            else:
                # Anything else is invalid here
                raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

        return statements

    def peek(self, kind):
        """
        Look ahead one token (without consuming anything)
        and check if its type matches `kind`.
        Useful for disambiguating IDENT vs IDENT '(' vs IDENT '='.
        """
        return (
            self.pos + 1 < len(self.tokens)
            and self.tokens[self.pos + 1][0] == kind
        )

    def match(self, kind):
        """
        If the current token is of type `kind`, consume it
        (advance pos) and return True. Otherwise, do nothing
        and return False.
        Used to optionally consume punctuation like commas or braces.
        """
        if (
            self.pos < len(self.tokens)
            and self.tokens[self.pos][0] == kind
        ):
            self.pos += 1
            return True
        return False

    def parse_block(self):
        """
        Parse a sequence of statements wrapped in { ... }.
        - Expect the opening '{'
        - Parse statements one by one until we see the closing '}'
        Returns the list of inner statements.
        """
        if not self.match("LBRACE"):
            raise SyntaxError("Expected '{' at start of block")

        stmts = []
        # Keep calling parse_stmt until the '}' arrives
        while not self.match("RBRACE"):
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        """
        Parse exactly one statement inside a block.
        This shares logic with top‐level parse(), but never
        loops—just handles a single PRINT, ASSIGN, CALL, IF, or WHILE.
        """
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
            # e.g. append(nums, 4)
            return self.parse_call()

        elif tok_type == "IF":
            return self.parse_if()

        elif tok_type == "WHILE":
            return self.parse_while()

        else:
            raise SyntaxError(f"Unexpected token in block: {self.tokens[self.pos]}")

    def parse_call(self):
        """
        Parse a function‐call statement or expression:
            IDENT '(' [arg1, arg2, ...] ')'
        Returns an AST node: ("CALL", functionName, [argASTs...])
        """
        name = self.tokens[self.pos][1]  # the function name
        self.pos += 1

        if not self.match("LPAREN"):
            raise SyntaxError("Expected '(' after function name")

        args = []
        # If the next token isn't ')', parse the first argument
        if not self.match("RPAREN"):
            args.append(self.bool_expr())
            # Then any further comma-separated args
            while self.match("COMMA"):
                args.append(self.bool_expr())
            if not self.match("RPAREN"):
                raise SyntaxError("Expected ')' after function arguments")

        return ("CALL", name, args)

    def parse_if(self):
        """
        Parse an if‐statement with optional else:
            'if' '(' condition ')' thenBlock ['else' elseBlock]
        Returns: ("IF", conditionAST, thenList, elseListOrNone)
        """
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
        """
        Parse a while‐loop:
            'while' '(' condition ')' bodyBlock
        Returns: ("WHILE", conditionAST, bodyList)
        """
        self.match("WHILE")
        if not self.match("LPAREN"):
            raise SyntaxError("Expected '(' after 'while'")
        cond = self.bool_expr()
        if not self.match("RPAREN"):
            raise SyntaxError("Expected ')' after while condition")

        body = self.parse_block()
        return ("WHILE", cond, body)

    def bool_expr(self):
        """
        Parse logical combinations of comparisons using AND/OR.
        Calls compare_expr() to handle the next level (==, <, >, etc.).
        """
        node = self.compare_expr()

        while (
            self.pos < len(self.tokens)
            and self.tokens[self.pos][0] in ("AND", "OR")
        ):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.compare_expr()
            node = (op, node, right)

        return node

    def compare_expr(self):
        """
        Parse chained comparisons like 'a < b < c' or single ones like 'x == y'.
        Returns either a single expression AST or a CHAIN node listing all comparisons.
        """
        node = self.expr()
        comps = []

        while (
            self.pos < len(self.tokens)
            and self.tokens[self.pos][0] in ("EQ","NEQ","LT","GT","LE","GE")
        ):
            op = self.tokens[self.pos][0]
            self.pos += 1
            rhs = self.expr()
            comps.append((op, rhs))

        if comps:
            # e.g. ("CHAIN", baseExpr, [(op1,expr1),(op2,expr2),...])
            return ("CHAIN", node, comps)
        else:
            return node

    def expr(self):
        """
        Parse addition and subtraction at this precedence level.
        Calls term() to handle the next level (multiplication, etc.).
        """
        node = self.term()

        while (
            self.pos < len(self.tokens)
            and self.tokens[self.pos][0] in ("PLUS","MINUS")
        ):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.term()
            node = (op, node, right)

        return node

    def term(self):
        """
        Parse multiplication, division, and modulo.
        Calls factor() for the most basic pieces.
        """
        node = self.factor()

        while (
            self.pos < len(self.tokens)
            and self.tokens[self.pos][0] in ("MUL","DIV","MOD")
        ):
            op = self.tokens[self.pos][0]
            self.pos += 1
            right = self.factor()
            node = (op, node, right)

        return node

    def factor(self):
        """
        Parse the smallest building blocks:
          - Unary minus ('-x')
          - input("prompt")
          - List literals [a, b, c]
          - Numbers, strings, booleans (true/false)
          - Variable names
          - Logical not (!x)
          - Parenthesized sub‐expressions ( ... )
          - Indexing (list[index])
        Each returns a simple tuple describing the node type and its children.
        """
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")

        tok_type, tok_val = self.tokens[self.pos]

        # Unary minus: consume '-' and parse the next factor
        if tok_type == "MINUS":
            self.pos += 1
            expr = self.factor()
            return ("NEG", expr)

        # input("prompt")
        if tok_type == "INPUT":
            self.pos += 1
            if not self.match("LPAREN"):
                raise SyntaxError("Expected '(' after 'input'")
            prompt = self.bool_expr()
            if not self.match("RPAREN"):
                raise SyntaxError("Expected ')' after input call")
            return ("INPUT", prompt)

        # List literal: [ item, item, ... ]
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

        # Numbers
        if tok_type == "NUMBER":
            self.pos += 1
            return ("NUMBER", tok_val)

        # String literals
        if tok_type == "STRING":
            self.pos += 1
            return ("STRING", tok_val)

        # Boolean true/false
        if tok_type == "TRUE":
            self.pos += 1
            return ("BOOL", True)
        if tok_type == "FALSE":
            self.pos += 1
            return ("BOOL", False)

        # Variable reference: store the name for later lookup
        if tok_type == "IDENT":
            self.pos += 1
            node = ("VAR", tok_val)

        # Logical not: !expr
        elif tok_type == "NOT":
            self.pos += 1
            expr = self.factor()
            node = ("NOT", expr)

        # Parentheses: ( expr )
        elif tok_type == "LPAREN":
            self.pos += 1
            node = self.bool_expr()
            if not self.match("RPAREN"):
                raise SyntaxError("Missing closing parenthesis")

        else:
            # If none of the above matched, it really is an error
            raise SyntaxError(f"Unexpected token: {self.tokens[self.pos]}")

        # Handle indexing syntax after any primary expression:
        # allow myList[2][1] etc.
        while self.match("LBRACKET"):
            idx = self.bool_expr()
            if not self.match("RBRACKET"):
                raise SyntaxError("Expected ']' after index")
            node = ("INDEX", node, idx)

        return node