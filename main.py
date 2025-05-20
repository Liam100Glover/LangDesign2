# Entry point for the language interpreter.
import sys
from interpreter.lexer import tokenize
from interpreter.parser import Parser
from interpreter.interpreter import evaluate

def run_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Ignore blank lines and comments
        try:
            tokens = tokenize(line)
            parser = Parser(tokens)
            ast = parser.parse()

            if ast[0] != "PRINT":
                print("Warning: non-print expression ignored")
            else:
                evaluate(ast)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
    else:
        run_file(sys.argv[1])
