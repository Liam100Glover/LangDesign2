import os
import sys

# Prepend the `interpreter/` directory (which contains lexer.py, parser.py, interpreter.py)
interp_dir = os.path.join(os.path.dirname(__file__), "interpreter")
sys.path.insert(0, interp_dir)

# Import modules from the interpreter/ folder directly
import lexer
import parser
import interpreter

# Use the classes/functions
def run_file(file_path):
    # Read source file as UTF-8 to avoid platform default encoding issues
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    tokens     = lexer.tokenize(code)
    statements = parser.Parser(tokens).parse()

    engine = interpreter.Interpreter()
    for stmt in statements:
        engine.execute(stmt)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
    else:
        run_file(sys.argv[1])