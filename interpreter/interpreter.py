def evaluate(node):
    if node[0] == "PRINT":
        value = evaluate(node[1])
        print(value)
        return None
    
    elif node[0] == "CHAIN":
        left = evaluate(node[1])
        for comp_op, right_expr in node[2]:
            right = evaluate(right_expr)

            if comp_op == "EQ":
                if not (left == right): return False
            elif comp_op == "NEQ":
                if not (left != right): return False
            elif comp_op == "LT":
                if not (left < right): return False
            elif comp_op == "GT":
                if not (left > right): return False
            elif comp_op == "LE":
                if not (left <= right): return False
            elif comp_op == "GE":
                if not (left >= right): return False

            # move to next comparison in chain
            left = right

        return True

    elif node[0] == "NUMBER":
        return node[1]

    elif node[0] == "BOOL":
        return node[1]
    
    elif node[0] == "STRING":
        return node[1]
    
    elif node[0] == "NEGATE":
        return -evaluate(node[1])

    elif node[0] == "NOT":
        return not evaluate(node[1])

    elif node[0] == "PLUS":
        return evaluate(node[1]) + evaluate(node[2])
    elif node[0] == "MINUS":
        return evaluate(node[1]) - evaluate(node[2])
    elif node[0] == "MUL":
        return evaluate(node[1]) * evaluate(node[2])
    elif node[0] == "DIV":
        return evaluate(node[1]) / evaluate(node[2])

    # Boolean logic
    elif node[0] == "AND":
        return evaluate(node[1]) and evaluate(node[2])
    elif node[0] == "OR":
        return evaluate(node[1]) or evaluate(node[2])

    # Comparisons
    elif node[0] == "EQ":
        return evaluate(node[1]) == evaluate(node[2])
    elif node[0] == "NEQ":
        return evaluate(node[1]) != evaluate(node[2])
    elif node[0] == "LT":
        return evaluate(node[1]) < evaluate(node[2])
    elif node[0] == "GT":
        return evaluate(node[1]) > evaluate(node[2])
    elif node[0] == "LE":
        return evaluate(node[1]) <= evaluate(node[2])
    elif node[0] == "GE":
        return evaluate(node[1]) >= evaluate(node[2])

    else:
        raise ValueError(f"Unknown node type: {node[0]}")
