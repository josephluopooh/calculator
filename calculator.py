import operator
import string
from collections import deque
from typing import Tuple


class MyException(Exception):
    def __str__(self):
        return "test"


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
            if "(" not in operator_stack:
                raise ValueError
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
        "/": operator.floordiv,
    }
    for symbol in postfix_expression:
        if symbol in operators:
            b = int(result_stack.pop())
            a = int(result_stack.pop())
            temp_out = operators[symbol](a, b)
            result_stack.append(str(temp_out))
        else:
            result_stack.append(symbol)
    return result_stack.pop()


def parse(chars: list) -> list:
    chars_new = chars.copy()
    chars_contain_equal, ind_equal = contain_equal(chars_new)
    if chars_contain_equal:
        if len(chars_new) == 2:
            if ind_equal == 0:
                chars_new.insert(1, "=")
                chars_new[0] = chars_new[0][:-1]
            else:
                chars_new.insert(1, "=")
                chars_new[2] = chars_new[2][1:]
        elif len(chars_new) == 1:
            chars_new = chars_new[0].split("=")
            chars_new.insert(1, "=")
    for ind, char in enumerate(chars_new):
        if not char.isnumeric():
            if char.startswith("+"):
                chars_new[ind] = "+"
            elif not char[-1].isnumeric() and char.startswith("-"):
                chars_new[ind] = minus_count(char)
            elif char.startswith("*") or char.startswith("/"):
                if char.count("*") > 1 or char.count("/") > 1:
                    raise ValueError
    return chars_new


def contain_equal(chars: list) -> Tuple[bool, int]:
    contain_equal = False
    ind_out = None
    for ind, symbol in enumerate(chars):
        if "=" in symbol:
            ind_out = ind
            contain_equal = True
            break
    return contain_equal, ind_out


def chars_to_numbers(chars_new: list) -> list:
    num_list = []
    if chars_new[0][-1].isnumeric():
        num_list.append(int(chars_new[0]))
        chars_new.pop(0)
    for ind, char in enumerate(chars_new[::2]):
        if char == "+":
            num_list.append(int(chars_new[2 * ind + 1]))
        else:
            num_list.append(-int(chars_new[2 * ind + 1]))
    return num_list


def minus_count(minus_string: str) -> str:
    minus = minus_string.count("-")
    if minus % 2 == 1:
        return "-"
    else:
        return "+"


def is_valid_identifier(variable: str) -> bool:
    latin_letters = set(string.ascii_letters)
    is_valid_identifier = True
    for char in variable:
        if char not in latin_letters:
            is_valid_identifier = False
            break
    return is_valid_identifier


def eval_variable_number(operand: str, variables: dict):
    if operand in variables:
        return variables[operand]
    elif operand[0] == "-":
        if operand[1:].isnumeric():
            return int(operand)
    elif operand.isnumeric():
        return int(operand)
    else:
        return None


def main():
    variables = {}
    while True:
        try:
            chars = input().split()
            chars_parsed = parse(chars)
            chars_parsed = manipulate_parentheses(chars_parsed)
            if len(chars_parsed) == 0:
                pass
            elif len(chars_parsed) == 1:
                if chars_parsed[0][0] == "/":
                    if chars_parsed[0] == "/exit":
                        print("Bye!")
                        break
                    elif chars_parsed[0] == "/help":
                        print(
                            "The program calculates the sum or subtraction of numbers"
                        )
                    else:
                        print("Unknown command")
                else:
                    if eval_variable_number(chars_parsed[0], variables) is None:
                        print("Unknown variable")
                    else:
                        print(eval_variable_number(chars_parsed[0], variables))
            else:
                # sums = 0
                if "=" in chars_parsed:
                    if not is_valid_identifier(chars_parsed[0]):
                        print("Invalid identifier")
                        continue
                    elif len(chars_parsed) > 3:
                        print("Invalid assignment")
                        continue
                    if not chars_parsed[2].isnumeric():
                        if not is_valid_identifier(chars_parsed[2]):
                            print("Invalid assignment")
                        elif chars_parsed[2] not in variables:
                            print("Unknown variable")
                        else:
                            variables[chars_parsed[0]] = variables[chars_parsed[2]]
                    else:
                        variables[chars_parsed[0]] = chars_parsed[2]
                else:
                    chars_evaluated = []
                    for ind, symbol in enumerate(chars_parsed):
                        eval_symbol = eval_variable_number(symbol, variables)
                        if eval_symbol is None:
                            chars_evaluated.append(symbol)
                        else:
                            chars_evaluated.append(eval_symbol)
                    print(postfix_to_result(infix_to_postfix(chars_evaluated)))
        except ValueError:
            print("Invalid expression")


if __name__ == "__main__":
    main()
