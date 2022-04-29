import operator
from collections import deque


def manipulate_parentheses(old_expression):
    new_expression = []
    for ind, symbol in enumerate(old_expression):
        if symbol[0] == "(":
            new_expression.extend(["(", symbol[1:]])
        elif symbol[-1] == ")":
            new_expression.extend([symbol[:-1], ")"])
        else:
            new_expression.append(symbol)
    return new_expression


def infix_to_postfix(infix_expression):
    operator_stack = deque()
    postfix_expression = []
    operators = {"+", "-", "*", "/", "(", ")"}
    for symbol in infix_expression:
        if symbol not in operators:
            postfix_expression.append(symbol)
        elif not operator_stack or operator_stack[-1] == "(":
            operator_stack.append(symbol)
        elif symbol == "(":
            operator_stack.append(symbol)
        elif symbol == ")":
            while operator_stack[-1] != "(":
                postfix_expression.append(operator_stack.pop())
            operator_stack.pop()
        elif priority(symbol) > priority(operator_stack[-1]):
            operator_stack.append(symbol)
        elif priority(symbol) <= priority(operator_stack[-1]):
            while (
                len(operator_stack) != 0
                and operator_stack[-1] != "("
                and priority(symbol) <= priority(operator_stack[-1])
            ):
                postfix_expression.append(operator_stack.pop())
            operator_stack.append(symbol)
    for _ in range(len(operator_stack)):
        postfix_expression.append(operator_stack.pop())
    return postfix_expression


def priority(operator):
    if operator in {"+", "-"}:
        return 0
    elif operator in {"*", "/"}:
        return 1


def postfix_to_result(postfix_expression):
    result_stack = deque()
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }
    for symbol in postfix_expression:
        if symbol in operators:
            a = int(result_stack.pop())
            b = int(result_stack.pop())
            temp_out = operators[symbol](a, b)
            result_stack.append(str(temp_out))
        else:
            result_stack.append(symbol)
    return result_stack.pop()
