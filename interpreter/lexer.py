import re  # Python’s regular‐expression library, used for pattern matching.

# TOKEN_SPEC lists all the token types our language recognizes,
# paired with the regex pattern to identify each one.
TOKEN_SPEC = [
    # --- Keywords: reserved words that perform special functions ---
    ("PRINT",    r"\bprint\b"),   # the keyword 'print'
    ("IF",       r"\bif\b"),      # the keyword 'if'
    ("ELSE",     r"\belse\b"),    # the keyword 'else'
    ("WHILE",    r"\bwhile\b"),   # the keyword 'while'
    ("INPUT",    r"\binput\b"),   # the keyword 'input'

    # --- Literals: fixed values written directly in the code ---
    ("STRING",   r'"[^"\\]*"'),   # text in double quotes (no unescaped quotes inside)
    ("TRUE",     r"\btrue\b"),    # boolean literal true
    ("FALSE",    r"\bfalse\b"),   # boolean literal false
    ("NUMBER",   r"\d+(\.\d+)?"), # integer or decimal, e.g. 123 or 45.67

    # --- Operators: symbols that glue or compare values together ---
    ("AND",      r"\band\b"),     # logical AND
    ("OR",       r"\bor\b"),      # logical OR
    ("EQ",       r"=="),          # equals comparison
    ("NEQ",      r"!="),          # not‐equals comparison
    ("LE",       r"<="),          # less‐than‐or‐equal comparison
    ("GE",       r">="),          # greater‐than‐or‐equal comparison
    ("LT",       r"<"),           # less‐than comparison
    ("GT",       r">"),           # greater‐than comparison
    ("ASSIGN",   r"="),           # assignment operator
    ("NOT",      r"!"),           # logical NOT or inequality prefix
    ("PLUS",     r"\+"),          # addition or string concatenation
    ("MINUS",    r"-"),           # subtraction or unary negative
    ("MUL",      r"\*"),          # multiplication
    ("DIV",      r"/"),           # division
    ("MOD",      r"%"),           # modulo (remainder)

    # --- Delimiters: punctuation that groups or separates code elements ---
    ("LPAREN",   r"\("),          # left parenthesis "("
    ("RPAREN",   r"\)"),          # right parenthesis ")"
    ("LBRACE",   r"\{"),          # left brace "{"
    ("RBRACE",   r"\}"),          # right brace "}"
    ("LBRACKET", r"\["),          # left bracket "["
    ("RBRACKET", r"\]"),          # right bracket "]"
    ("COMMA",    r","),           # comma "," to separate items

    # --- Identifiers: names for variables and functions ---
    ("IDENT",    r"[a-zA-Z_][a-zA-Z0-9_]*"),
    # must start with a letter or underscore, followed by letters, numbers, or underscores

    # --- Comments & Whitespace: ignore these ---
    ("COMMENT",  r"#.*"),          # from "#" to end of line
    ("SKIP",     r"[ \t\r\n]+"),   # spaces, tabs, or newlines

    # --- Mismatch: any other single character is an error ---
    ("MISMATCH", r"."),
]

# Build a single regex by combining all token patterns.
# (?P<NAME>pattern) names each subpattern for identification.
token_regex = "|".join(f"(?P<{name}>{pattern})"
                       for name, pattern in TOKEN_SPEC)
master_pat = re.compile(token_regex)

def tokenize(code):
    """
    Convert the input source code (a string) into a list of tokens.
    Each token is a pair: (TOKEN_TYPE, value).
    """
    tokens = []
    # Scan through the code, one match at a time
    for mo in master_pat.finditer(code):
        kind = mo.lastgroup    # which pattern matched
        value = mo.group()     # the exact text that was matched

        if kind == "NUMBER":
            # Convert numeric text into a Python float
            tokens.append(("NUMBER", float(value)))

        elif kind == "STRING":
            # Remove the surrounding quotes from string literals
            tokens.append(("STRING", value[1:-1]))

        elif kind in ("TRUE", "FALSE"):
            # Keep boolean literals as their text; parser will turn them into True/False
            tokens.append((kind, value))

        elif kind in ("PRINT","IF","ELSE","WHILE","INPUT",
                      "AND","OR","EQ","NEQ","LE","GE","LT","GT",
                      "ASSIGN","NOT","PLUS","MINUS","MUL","DIV","MOD",
                      "LPAREN","RPAREN","LBRACE","RBRACE",
                      "LBRACKET","RBRACKET","COMMA"):
            # All other keywords, operators, and punctuation
            tokens.append((kind, value))

        elif kind == "IDENT":
            # Variable and function names
            tokens.append(("IDENT", value))

        elif kind in ("SKIP", "COMMENT"):
            # Ignore whitespace and comments entirely
            continue

        else:
            # Any unmatched character is a syntax error
            raise SyntaxError(f"Unexpected character: {value}")

    return tokens