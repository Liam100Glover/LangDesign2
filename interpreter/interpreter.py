class Interpreter:
    def __init__(self):
        self.env = {}

    def evaluate(self, node):
        node_type = node[0]
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
        elif node_type == "NOT":
            return not self.evaluate(node[1])
        elif node_type == "NEG":
            val = self.evaluate(node[1])
            if not isinstance(val, (int, float)):
                raise TypeError("Unary minus applied to non-number")
            return -val
        elif node_type in ("PLUS", "MINUS", "MUL", "DIV"):
            left = self.evaluate(node[1])
            right = self.evaluate(node[2])
            if node_type == "PLUS":
                # dynamic type check: str+number not allowed
                if isinstance(left, str) ^ isinstance(right, str):
                    raise TypeError(f"Cannot add {type(left).__name__} and {type(right).__name__}")
                return left + right
            elif node_type == "MINUS":
                return left - right
            elif node_type == "MUL":
                return left * right
            elif node_type == "DIV":
                return left / right
        elif node_type in ("EQ", "NEQ", "LT", "GT", "LE", "GE"):
            left = self.evaluate(node[1])
            right = self.evaluate(node[2])
            ops = {
                "EQ": lambda a,b: a==b,
                "NEQ": lambda a,b: a!=b,
                "LT": lambda a,b: a< b,
                "GT": lambda a,b: a> b,
                "LE": lambda a,b: a<=b,
                "GE": lambda a,b: a>=b
            }
            return ops[node_type](left, right)
        elif node_type == "CHAIN":
            left = self.evaluate(node[1])
            for op, expr in node[2]:
                right = self.evaluate(expr)
                if not {
                    "EQ": left==right,
                    "NEQ": left!=right,
                    "LT": left< right,
                    "GT": left> right,
                    "LE": left<=right,
                    "GE": left>=right
                }[op]:
                    return False
                left = right
            return True
        elif node_type == "AND":
            return self.evaluate(node[1]) and self.evaluate(node[2])
        elif node_type == "OR":
            return self.evaluate(node[1]) or self.evaluate(node[2])
        else:
            raise ValueError(f"Unknown node: {node_type}")

    def execute(self, stmt):
        try:
            if stmt[0] == "PRINT":
                result = self.evaluate(stmt[1])
                print(result)
            elif stmt[0] == "ASSIGN":
                name = stmt[1]
                value = self.evaluate(stmt[2])
                self.env[name] = value
        except Exception as e:
            print(f"Error: {e}")