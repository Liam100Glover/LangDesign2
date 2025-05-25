class Interpreter:
    """
    The Interpreter walks over the parsed code (the AST) and:
      1. Evaluates expressions to produce values (numbers, strings, lists, etc.)
      2. Executes statements (print, assignments, loops, branches, function calls)
    It keeps track of global variables in a simple dictionary (self.env).
    """
    def __init__(self):
        # env is the “environment” that maps variable names (strings)
        # to their current values (numbers, strings, lists, booleans).
        self.env = {}

    def evaluate(self, node):
        """
        Evaluate a single expression node from the AST.
        `node` is a tuple whose first element (node[0]) is the node type,
        and the remaining elements hold the necessary data.
        Returns a Python value: int, float, str, bool, or list.
        """
        t = node[0]  # the node type, e.g. "NUMBER", "PLUS", "VAR", etc.

        # --- Literal values: just return them directly ---
        if t == "NUMBER":
            # node = ("NUMBER", numeric_value)
            return node[1]
        if t == "STRING":
            # node = ("STRING", text_value)
            return node[1]
        if t == "BOOL":
            # node = ("BOOL", True or False)
            return node[1]

        # --- Variables: look up in the environment ---
        if t == "VAR":
            # node = ("VAR", variable_name)
            name = node[1]
            if name in self.env:
                return self.env[name]
            # If the variable was never assigned, that’s an error.
            raise NameError(f"Undefined variable: {name}")

        # --- input(prompt): ask the user for a line of text ---
        if t == "INPUT":
            # node = ("INPUT", prompt_expr)
            # First evaluate the prompt expression to get its text.
            prompt = self.evaluate(node[1])
            if not isinstance(prompt, str):
                # Only strings can be used as prompts
                raise TypeError("Input prompt must be a string")
            # Call Python’s built-in input() to get user input
            return input(prompt)

        # --- List literals: build a new list from element expressions ---
        if t == "LIST":
            # node = ("LIST", [expr1, expr2, ...])
            # Evaluate each element expression and collect results
            return [self.evaluate(elem) for elem in node[1]]

        # --- Indexing: retrieve one item from a list by index ---
        if t == "INDEX":
            # node = ("INDEX", list_expr, index_expr)
            lst = self.evaluate(node[1])
            idx = self.evaluate(node[2])
            # Ensure we are indexing an actual list
            if not isinstance(lst, list):
                raise TypeError("Indexing non-list")
            # Ensure the index is a number (we will convert to int)
            if not isinstance(idx, (int, float)):
                raise TypeError("Index must be a number")
            # Return the selected element (cast index to int to drop .0)
            return lst[int(idx)]

        # --- Function calls: currently only append() and remove() ---
        if t == "CALL":
            # node = ("CALL", function_name, [arg1_expr, arg2_expr, ...])
            name, args = node[1], node[2]

            # append(list, value) adds value to the end of the list
            if name == "append":
                lst = self.evaluate(args[0])
                val = self.evaluate(args[1])
                if not isinstance(lst, list):
                    raise TypeError("append first arg must be list")
                lst.append(val)
                return None  # append returns nothing

            # remove(list, index) removes and returns the item at that index
            if name == "remove":
                lst = self.evaluate(args[0])
                idx = self.evaluate(args[1])
                if not isinstance(lst, list):
                    raise TypeError("remove first arg must be list")
                # pop returns the removed element
                return lst.pop(int(idx))

            # If an unknown function name is used, that’s an error.
            raise NameError(f"Unknown function: {name}")

        # --- Unary operators ---
        if t == "NOT":
            # Logical NOT: node = ("NOT", expr)
            return not self.evaluate(node[1])

        if t == "NEG":
            # Unary minus: node = ("NEG", expr)
            val = self.evaluate(node[1])
            if not isinstance(val, (int, float)):
                raise TypeError("Unary minus applied to non-number")
            return -val

        # --- Binary arithmetic and modulo ---
        if t in ("PLUS", "MINUS", "MUL", "DIV", "MOD"):
            a = self.evaluate(node[1])
            b = self.evaluate(node[2])

            if t == "PLUS":
                # Strict rule: you cannot mix string + number
                if isinstance(a, str) ^ isinstance(b, str):
                    raise TypeError(f"Cannot add {type(a).__name__} and {type(b).__name__}")
                return a + b

            if t == "MINUS":
                return a - b

            if t == "MUL":
                return a * b

            if t == "DIV":
                return a / b

            if t == "MOD":
                return a % b

        # --- Comparison operators ---
        if t in ("EQ", "NEQ", "LT", "GT", "LE", "GE"):
            a = self.evaluate(node[1])
            b = self.evaluate(node[2])
            # A small lookup table to map node types to Python comparisons
            ops = {
                "EQ":  lambda x, y: x == y,
                "NEQ": lambda x, y: x != y,
                "LT":  lambda x, y: x <  y,
                "GT":  lambda x, y: x >  y,
                "LE":  lambda x, y: x <= y,
                "GE":  lambda x, y: x >= y,
            }
            return ops[t](a, b)

        # --- Chained comparisons (e.g., 1 < x < 5) ---
        if t == "CHAIN":
            # node = ("CHAIN", firstExpr, [(op1, expr1), (op2, expr2), ...])
            current = self.evaluate(node[1])
            for op, expr in node[2]:
                nxt = self.evaluate(expr)
                valid = {
                    "EQ":  current == nxt,
                    "NEQ": current != nxt,
                    "LT":  current <  nxt,
                    "GT":  current >  nxt,
                    "LE":  current <= nxt,
                    "GE":  current >= nxt,
                }[op]
                if not valid:
                    return False
                current = nxt
            return True

        # --- Boolean logic operators ---
        if t == "AND":
            # node = ("AND", expr1, expr2)
            return self.evaluate(node[1]) and self.evaluate(node[2])

        if t == "OR":
            # node = ("OR", expr1, expr2)
            return self.evaluate(node[1]) or self.evaluate(node[2])

        # If we get here, the node type was unrecognized
        raise ValueError(f"Unknown node type: {t}")

    def execute(self, stmt):
        """
        Execute a single statement node from the AST.
        Statements include PRINT, ASSIGN, CALL, IF, and WHILE.
        Any runtime errors are caught so execution can continue.
        """
        kind = stmt[0]  # the statement type
        try:
            if kind == "PRINT":
                # stmt = ("PRINT", expr)
                # Evaluate the expression, then print its value
                print(self.evaluate(stmt[1]))

            elif kind == "ASSIGN":
                # stmt = ("ASSIGN", varName, expr)
                # Evaluate the expression and store it in the environment
                self.env[stmt[1]] = self.evaluate(stmt[2])

            elif kind == "CALL":
                # stmt = ("CALL", name, args)
                # We evaluate the call for its side effects (append/remove)
                self.evaluate(stmt)

            elif kind == "IF":
                # stmt = ("IF", condExpr, thenList, elseListOrNone)
                _, cond, then_blk, else_blk = stmt
                test = self.evaluate(cond)
                if not isinstance(test, bool):
                    raise TypeError("Condition must be boolean")
                # Choose which block to run
                blk = then_blk if test else else_blk
                if blk:
                    for s in blk:
                        self.execute(s)

            elif kind == "WHILE":
                # stmt = ("WHILE", condExpr, bodyList)
                _, cond, body = stmt
                # Repeat until the condition becomes false
                while True:
                    test = self.evaluate(cond)
                    if not isinstance(test, bool):
                        raise TypeError("Condition must be boolean")
                    if not test:
                        break
                    for s in body:
                        self.execute(s)

        except Exception as e:
            # If anything goes wrong, print an error message
            # and continue with the next statement.
            print(f"Error: {e}")