import re

# Define all possible token types and their regex patterns
TOKEN_SPEC = [
    ("PRINT",    r"\bprint\b"),         # print keyword
    ("IF",       r"\bif\b"),            # if keyword
    ("ELSE",     r"\belse\b"),          # else keyword
    ("WHILE",    r"\bwhile\b"),         # while keyword
    ("INPUT",    r"\binput\b"),         # input builtin
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
    ("MOD",      r"%"),                   # mod
    ("LPAREN",   r"\("),                 # left parenthesis
    ("RPAREN",   r"\)"),                 # right parenthesis
    ("LBRACE",   r"\{"),                 # left brace
    ("RBRACE",   r"\}"),                 # right brace
    ("IDENT",    r"[a-zA-Z_][a-zA-Z0-9_]*"),  # identifiers
    ("COMMENT",  r"#.*"),                 # comments
    ("SKIP",     r"[ \t\r\n]+"),       # spaces, tabs, newlines
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
        elif kind in ("TRUE", "FALSE", "PRINT", "IF", "ELSE", "WHILE", "INPUT",
                      "AND", "OR", "EQ", "NEQ", "LE", "GE", "LT", "GT",
                      "ASSIGN", "NOT", "PLUS", "MINUS", "MUL", "DIV", "MOD",
                      "LPAREN", "RPAREN", "LBRACE", "RBRACE"):
            tokens.append((kind, value))
        elif kind == "IDENT":
            tokens.append(("IDENT", value))
        elif kind in ("SKIP", "COMMENT"):
            continue
        else:
            raise SyntaxError(f"Unexpected character: {value}")
    return tokens