import re

# Define all possible token types and their regex patterns
TOKEN_SPEC = [
    ("PRINT",    r"\bprint\b"),         # print keyword
    ("STRING",   r'"[^"]*"'),            # string literals
    ("TRUE",     r"\btrue\b"),          # boolean true
    ("FALSE",    r"\bfalse\b"),         # boolean false
    ("AND",      r"\band\b"),           # logical and
    ("OR",       r"\bor\b"),            # logical or
    ("EQ",       r"=="),                  # equal
    ("NEQ",      r"!="),                  # not equal
    ("LE",       r"<="),                  # less or equal
    ("GE",       r">="),                  # greater or equal
    ("LT",       r"<"),                   # less than
    ("GT",       r">"),                   # greater than
    ("ASSIGN",   r"="),                   # assignment
    ("NOT",      r"!"),                   # logical not
    ("NUMBER",   r"\d+(\.\d+)?"),      # integer or decimal
    ("PLUS",     r"\+"),                 # addition
    ("MINUS",    r"-"),                   # subtraction / unary minus
    ("MUL",      r"\*"),                 # multiplication
    ("DIV",      r"/"),                   # division
    ("LPAREN",   r"\("),                 # left parenthesis
    ("RPAREN",   r"\)"),                 # right parenthesis
    ("IDENT",    r"[a-zA-Z_][a-zA-Z0-9_]*"),  # identifiers
    ("COMMENT",  r"#.*"),                 # comments
    ("SKIP",     r"[ \t]+"),             # spaces and tabs
    ("MISMATCH", r".")                    # any other character
]

# Build master regex pattern
token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
master_pat = re.compile(token_regex)

def tokenize(code):

    tokens = []
    for mo in master_pat.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            tokens.append(("NUMBER", float(value)))
        elif kind == "STRING":
            tokens.append(("STRING", value[1:-1]))  # strip quotes
        elif kind in ("TRUE", "FALSE"):
            tokens.append((kind, value))
        elif kind in ("PRINT", "AND", "OR", "EQ", "NEQ", "LE", "GE", "LT", "GT",
                      "ASSIGN", "NOT", "PLUS", "MINUS", "MUL", "DIV", "LPAREN", "RPAREN"):
            tokens.append((kind, value))
        elif kind == "IDENT":
            tokens.append(("IDENT", value))
        elif kind in ("SKIP", "COMMENT"):
            continue
        else:
            raise SyntaxError(f"Unexpected character: {value}")
    return tokens
