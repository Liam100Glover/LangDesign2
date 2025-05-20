# main.py
import sys

# if you need it, add the current directory to the path (usually not needed if you run from here)
# import os
# sys.path.insert(0, os.path.dirname(__file__))

from interpreter.lexer         import tokenize
from interpreter.parser        import Parser
from interpreter.interpreter   import Interpreter

def run_file(path):
    with open(path) as f:
        code = f.read()
    tokens     = tokenize(code)
    parser     = Parser(tokens)
    stmts      = parser.parse()
    engine     = Interpreter()
    for s in stmts:
        engine.execute(s)

if __name__ == "__main__":
    import sys as _sys
    if len(_sys.argv) != 2:
        print("Usage: python main.py <source_file>")
    else:
        run_file(_sys.argv[1])
