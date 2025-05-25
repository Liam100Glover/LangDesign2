# Language Design & Implementation ― README - 100617493

A small, Turing-complete language interpreter written in Python.  You can evaluate arithmetic, Boolean logic, strings, global variables, control-flow, I/O, and lists—all in plain `.txt` source files.


# Prerequisites

- **Python 3.8+** (no external libraries required)
- Works out-of-the-box on any system with Python 3.8 or later (e.g. Azure Labs VM)



# Project Structure

main.py
interpreter/
├── __init__.py
├── lexer.py
├── parser.py
└── interpreter.py
examples/
├── stage1.txt # arithmetic tests
├── stage2.txt # Boolean tests
├── stage3.txt # string tests
├── stage4.txt # variables tests
├── stage5.txt # control-flow & input tests
└── stage6.txt # list tests

You can create your own .txt files and run them through the interpreter. The language currently supports:

Stage 1 – Arithmetic
+, -, *, /, %, parentheses, unary minus.

Stage 2 – Boolean & Comparison
true/false, ==, !=, <, >, <=, >=, !, and, or.

Stage 3 – Strings
Double-quoted literals, + for concatenation, string comparisons.

Stage 4 – Global Variables
IDENT = expr, reading and writing named globals.

Stage 5 – Control Flow & I/O
if (cond) { … } [else { … }], while (cond) { … }, input("prompt").

Stage 6 – Lists
Literals [a, b, c], indexing list[index], append(list, value), remove(list, index).

Just follow the syntax shown in the examples/ folder. Save your code in a .txt file and point main.py at it everything else is automatic!

REFER TO BUILD.txt TO SEE HOW TO RUN THE PROJECT :)