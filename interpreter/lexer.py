import re

# Define all possible token types and their regex patterns
TOKEN_SPEC = [
    # Keywords
    ("PRINT",    r"\bprint\b"),
    ("IF",       r"\bif\b"),
    ("ELSE",     r"\belse\b"),
    ("WHILE",    r"\bwhile\b"),
    ("INPUT",    r"\binput\b"),
    
    # Literals
    ("STRING",   r'"[^"\\]*"'),
    ("TRUE",     r"\btrue\b"),
    ("FALSE",    r"\bfalse\b"),
    ("NUMBER",   r"\d+(\.\d+)?"),

    # Operators
    ("AND",      r"\band\b"),
    ("OR",       r"\bor\b"),
    ("EQ",       r"=="),
    ("NEQ",      r"!="),
    ("LE",       r"<="),
    ("GE",       r">="),
    ("LT",       r"<"),
    ("GT",       r">"),
    ("ASSIGN",   r"="),
    ("NOT",      r"!"),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("MUL",      r"\*"),
    ("DIV",      r"/"),
    ("MOD",      r"%"),

    # Delimiters
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("COMMA",    r","),

    # Identifier (variables, function names)
    ("IDENT",    r"[a-zA-Z_][a-zA-Z0-9_]*"),

    # Comments and whitespace
    ("COMMENT",  r"#.*"),
    ("SKIP",     r"[ \t\r\n]+"),

    # Any other character
    ("MISMATCH", r".")
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
        elif kind in ("PRINT","IF","ELSE","WHILE","INPUT",
                      "AND","OR","EQ","NEQ","LE","GE","LT","GT",
                      "ASSIGN","NOT","PLUS","MINUS","MUL","DIV","MOD",
                      "LPAREN","RPAREN","LBRACE","RBRACE","LBRACKET","RBRACKET","COMMA"):
            tokens.append((kind, value))
        elif kind == "IDENT":
            tokens.append(("IDENT", value))
        elif kind in ("SKIP", "COMMENT"):
            continue
        else:
            raise SyntaxError(f"Unexpected character: {value}")
    return tokens