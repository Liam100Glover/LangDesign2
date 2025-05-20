import re

# Define all the possible token types and their regex patterns
TOKEN_SPEC = [
    ("PRINT",    r"\bprint\b"),        # Recognises the print statement
    ("STRING", r'"[^"]*"'),
    ("TRUE",     r"true\b"),
    ("FALSE",    r"false\b"),
    ("AND",      r"and\b"),
    ("OR",       r"or\b"),
    ("EQ", r"=="),      # Equal to
    ("NEQ", r"!="),     # Not equal to
    ("LE", r"<="),      # Less than or equal
    ("GE", r">="),      # Greater than or equal
    ("LT", r"<"),       # Less than
    ("GT", r">"),       # Greater than
    ("NOT",      r"!"),
    ("NUMBER",   r"\d+(\.\d+)?"),     # Integer or decimal numbers
    ("PLUS",     r"\+"),              # Addition
    ("MINUS",    r"-"),               # Subtraction or unary minus
    ("MUL",      r"\*"),              # Multiplication
    ("DIV",      r"/"),               # Division
    ("LPAREN",   r"\("),              # Left parenthesis
    ("RPAREN",   r"\)"),              # Right parenthesis
    ("SKIP",     r"[ \t]+"),          # Ignore spaces and tabs
    ("MISMATCH", r"."),               # Any other unexpected character
]

def tokenize(code):
    """Convert input string into a list of tokens."""
    tokens = []
    pattern = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)
    
    for match in re.finditer(pattern, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "NUMBER":
            tokens.append(("NUMBER", float(value)))
        elif kind in ("PRINT", "STRING", "TRUE", "FALSE", "AND", "OR", "EQ", "NEQ", "LE", "GE", "LT", "GT", "NOT", "NUMBER",
              "PLUS", "MINUS", "MUL", "DIV", "LPAREN", "RPAREN"):
            tokens.append((kind, value))
        elif kind == "SKIP":
            continue  # Ignore spaces
        else:
            raise SyntaxError(f"Unexpected character: {value}")   
        
    return tokens
