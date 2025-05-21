
class Interpreter:
    def __init__(self):
        # Global environment for assignments
        self.env = {}

    def evaluate(self, node):
        node_type = node[0]

        # Literals
        if node_type == "NUMBER":
            return node[1]
        elif node_type == "STRING":
            return node[1]
        elif node_type == "BOOL":
            return node[1]
        elif node_type == "VAR":
            name = node[1]
            if name in self.env:
                return self.env[name]
            else:
                raise NameError(f"Undefined variable: {name}")

        # input(prompt)
        elif node_type == "INPUT":
            prompt = self.evaluate(node[1])
            if not isinstance(prompt, str):
                raise TypeError("Input prompt must be a string")
            return input(prompt)

        # Unary operators
        elif node_type == "NOT":
            return not self.evaluate(node[1])
        elif node_type == "NEG":
            val = self.evaluate(node[1])
            if not isinstance(val, (int, float)):
                raise TypeError("Unary minus applied to non-number")
            return -val

        # Binary arithmetic/logical operators
        elif node_type in ("PLUS", "MINUS", "MUL", "DIV", "MOD"):
            left  = self.evaluate(node[1])
            right = self.evaluate(node[2])

            if node_type == "PLUS":
                # Strict: cannot mix strings and numbers
                if isinstance(left, str) ^ isinstance(right, str):
                    raise TypeError(f"Cannot add {type(left).__name__} and {type(right).__name__}")
                return left + right
            elif node_type == "MINUS":
                return left - right
            elif node_type == "MUL":
                return left * right
            elif node_type == "DIV":
                return left / right
            elif node_type == "MOD":
                return left % right

        # Comparison operators
        elif node_type in ("EQ", "NEQ", "LT", "GT", "LE", "GE"):
            left  = self.evaluate(node[1])
            right = self.evaluate(node[2])
            if node_type == "EQ":
                return left == right
            elif node_type == "NEQ":
                return left != right
            elif node_type == "LT":
                return left < right
            elif node_type == "GT":
                return left > right
            elif node_type == "LE":
                return left <= right
            elif node_type == "GE":
                return left >= right

        # Chained comparisons (e.g. 1 < x < 3)
        elif node_type == "CHAIN":
            current = self.evaluate(node[1])
            for op, expr in node[2]:
                nxt = self.evaluate(expr)
                valid = {
                    "EQ":  current == nxt,
                    "NEQ": current != nxt,
                    "LT":  current < nxt,
                    "GT":  current > nxt,
                    "LE":  current <= nxt,
                    "GE":  current >= nxt,
                }[op]
                if not valid:
                    return False
                current = nxt
            return True

        # Boolean logic
        elif node_type == "AND":
            return self.evaluate(node[1]) and self.evaluate(node[2])
        elif node_type == "OR":
            return self.evaluate(node[1]) or self.evaluate(node[2])

        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def execute(self, stmt):
        try:
            kind = stmt[0]
            if kind == "PRINT":
                print(self.evaluate(stmt[1]))

            elif kind == "ASSIGN":
                name  = stmt[1]
                value = self.evaluate(stmt[2])
                self.env[name] = value

            elif kind == "IF":
                _, cond, then_block, else_block = stmt
                test = self.evaluate(cond)
                if not isinstance(test, bool):
                    raise TypeError("Condition must be a boolean")
                block = then_block if test else else_block
                if block:
                    for s in block:
                        self.execute(s)

            elif kind == "WHILE":
                _, cond, body = stmt
                while True:
                    test = self.evaluate(cond)
                    if not isinstance(test, bool):
                        raise TypeError("Condition must be a boolean")
                    if not test:
                        break
                    for s in body:
                        self.execute(s)

        except Exception as e:
            # Print errors but continue executing subsequent statements
            print(f"Error: {e}")