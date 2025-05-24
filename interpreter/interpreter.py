class Interpreter:
    def __init__(self):
        self.env = {}

    def evaluate(self, node):
        t = node[0]
        # Literals
        if t == "NUMBER":
            return node[1]
        if t == "STRING":
            return node[1]
        if t == "BOOL":
            return node[1]
        # Variables
        if t == "VAR":
            name = node[1]
            if name in self.env:
                return self.env[name]
            raise NameError(f"Undefined variable: {name}")
        # input(prompt)
        if t == "INPUT":
            prompt = self.evaluate(node[1])
            if not isinstance(prompt, str):
                raise TypeError("Input prompt must be a string")
            return input(prompt)
        # Lists
        if t == "LIST":
            return [self.evaluate(e) for e in node[1]]
        # Indexing
        if t == "INDEX":
            lst = self.evaluate(node[1])
            idx = self.evaluate(node[2])
            if not isinstance(lst, list):
                raise TypeError("Indexing non-list")
            if not isinstance(idx, (int, float)):
                raise TypeError("Index must be a number")
            return lst[int(idx)]
        # Function calls
        if t == "CALL":
            name, args = node[1], node[2]
            if name == "append":
                lst = self.evaluate(args[0])
                val = self.evaluate(args[1])
                if not isinstance(lst, list):
                    raise TypeError("append first arg must be list")
                lst.append(val)
                return None
            if name == "remove":
                lst = self.evaluate(args[0])
                idx = self.evaluate(args[1])
                if not isinstance(lst, list):
                    raise TypeError("remove first arg must be list")
                return lst.pop(int(idx))
            raise NameError(f"Unknown function: {name}")
        # Unary operators
        if t == "NOT":
            return not self.evaluate(node[1])
        if t == "NEG":
            val = self.evaluate(node[1])
            if not isinstance(val, (int, float)):
                raise TypeError("Unary minus applied to non-number")
            return -val
        # Binary arithmetic / modulo
        if t in ("PLUS", "MINUS", "MUL", "DIV", "MOD"):
            a = self.evaluate(node[1])
            b = self.evaluate(node[2])
            if t == "PLUS":
                # strict: no mixing str and number
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
        # Comparisons
        if t in ("EQ", "NEQ", "LT", "GT", "LE", "GE"):
            a = self.evaluate(node[1])
            b = self.evaluate(node[2])
            ops = {
                "EQ": lambda x,y: x==y,
                "NEQ":lambda x,y: x!=y,
                "LT": lambda x,y: x<y,
                "GT": lambda x,y: x>y,
                "LE": lambda x,y: x<=y,
                "GE": lambda x,y: x>=y,
            }
            return ops[t](a,b)
        # Chained comparisons
        if t == "CHAIN":
            current = self.evaluate(node[1])
            for op, expr in node[2]:
                nxt = self.evaluate(expr)
                valid = {
                    "EQ": current==nxt,
                    "NEQ": current!=nxt,
                    "LT": current<nxt,
                    "GT": current>nxt,
                    "LE": current<=nxt,
                    "GE": current>=nxt,
                }[op]
                if not valid:
                    return False
                current = nxt
            return True
        # Boolean logic
        if t == "AND":
            return self.evaluate(node[1]) and self.evaluate(node[2])
        if t == "OR":
            return self.evaluate(node[1]) or self.evaluate(node[2])
        raise ValueError(f"Unknown node type: {t}")

    def execute(self, stmt):
        kind = stmt[0]
        try:
            if kind == "PRINT":
                print(self.evaluate(stmt[1]))
            elif kind == "ASSIGN":
                self.env[stmt[1]] = self.evaluate(stmt[2])
            elif kind == "CALL":
                # calls like append() or remove()
                self.evaluate(stmt)
            elif kind == "IF":
                _, cond, then_blk, else_blk = stmt
                test = self.evaluate(cond)
                if not isinstance(test, bool):
                    raise TypeError("Condition must be boolean")
                blk = then_blk if test else else_blk
                if blk:
                    for s in blk:
                        self.execute(s)
            elif kind == "WHILE":
                _, cond, body = stmt
                while True:
                    test = self.evaluate(cond)
                    if not isinstance(test, bool):
                        raise TypeError("Condition must be boolean")
                    if not test:
                        break
                    for s in body:
                        self.execute(s)
        except Exception as e:
            print(f"Error: {e}")