import re
from collections import namedtuple

opinfo = namedtuple('Operator', 'precedence associativity')
operator_info = {
    "+": opinfo(0, "L"),
    "-": opinfo(0, "L"),
    "*": opinfo(1, "L"),
    "/": opinfo(1, "L"),
    "!": opinfo(2, "L"),
    "^": opinfo(2, "R"),
}

def is_dot(tok):
    for i in tok:
        if i == '.':
            return True


def calculator(num1, num2, operator):
    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '^': lambda x, y: x ** y
    }
    operation_func = operations.get(operator)
    if operation_func:
        result = operation_func(num1, num2)
        return result
    else:
        print("Invalid operation")



def tokenize(input_string):
    cleaned = re.sub(r'\s+', "", input_string)
    chars = list(cleaned)

    output = []
    state = ""
    buf = ""

    while len(chars) != 0:
        char = chars.pop(0)

        if char.isdigit() or char == ".":
            if state != "num":
                output.append(buf) if buf != "" else False
                buf = ""

            state = "num"
            buf += char

        elif char in operator_info.keys() or char in ["(", ")"]:
            output.append(buf) if buf != "" else False
            buf = ""

            output.append(char)

        else:
            if state != "func":
                output.append(buf) if buf != "" else False
                buf = ""

            state = "func"
            buf += char

    output.append(buf) if buf != "" else False
    return output


def shunt(tokens):
    tokens += ['end']
    operators = []
    output = []

    while len(tokens) != 1:
        current_token = tokens.pop(0)

        if current_token.isdigit() or is_dot(current_token):
            # Is a number
            #print("number", current_token)
            output.append(current_token)

        elif current_token in operator_info.keys():
            # Is an operator
            #print("op", current_token)
            
            while True:
                if len(operators) == 0:
                    break

                satisfied = False

                if operators[-1].isalpha():
                    # is a function
                    satisfied = True

                if operators[-1] not in ["(", ")"]:
                    if operator_info[operators[-1]].precedence > operator_info[current_token].precedence:
                        # operator at top has greater precedence
                        satisfied = True

                    elif operator_info[operators[-1]].precedence == operator_info[current_token].precedence:
                        if operator_info[operators[-1]].associativity == "left":
                            # equal precedence and has left associativity
                            satisfied = True

                satisfied = satisfied and operators[-1] != "("

                if not satisfied:
                    break

                output.append(operators.pop())

            operators.append(current_token)

        elif current_token == "(":
            # Is left bracket
            #print("left", current_token)
            operators.append(current_token)

        elif current_token == ")":
            # Is right bracket
            #print("right", current_token)

            while True:
                if len(operators) == 0:
                    break

                if operators[-1] == "(":
                    break

                output.append(operators.pop())

            if len(operators) != 0 and operators[-1] == "(":
                operators.pop()

        else:
            # Is a function name
            #print("func", current_token)
            operators.append(current_token)

    output.extend(operators[::-1])

    return output

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_parse_tree(postfix_expression):
    stack = []
    
    for token in postfix_expression.split():
        if token.isdigit() or is_dot(token):
            node = Node(token)
            stack.append(node)
        else:
            right_node = stack.pop()
            left_node = stack.pop()
            node = Node(token)
            node.left = left_node
            node.right = right_node
            stack.append(node)
    
    return stack[0]


def print_parse_tree(node, indent=''):
    if node is None:
        return
    
    print(indent + node.value)
    
    if node.left:
        print_parse_tree(node.left, indent + '  |__')
    
    if node.right:
        print_parse_tree(node.right, indent + '  |__')

def evaluate_parse_tree(node):
    if node is None:
        return 
    
    left_operand = evaluate_parse_tree(node.left)
    right_operand = evaluate_parse_tree(node.right)
    
    if left_operand is None or right_operand is None:
        return float(node.value)
    else:
        return calculator(left_operand, right_operand, node.value)

#tokens = tokenize("350 / ( 4 + 2 ) ^ 3")
#postfix = " ".join(shunt(tokens))
#parse = build_parse_tree(postfix)
#print(postfix)
#print_parse_tree(parse)
#value = evaluate_parse_tree(parse)
def testing():
    tests = [
    ("1+2", 3),
    ("1+2*3", 7),
    ("1+2 * 3 + 4", 11),
    ("1 + 2 * 3 + 4 * 5", 27),
    ("5.9 * ( 4 + 3 ) / 35", 1.18),
    ("( 5 / 9 ) * 9 ^ 2", 45),
    ("( 5 ^ 2 / 9 ) * 3", 8.33),
    ("((5^3/9^2)^2)/10", 0.24)
    ]
    for enum, (test, expected_value) in enumerate(tests):
        tokens = tokenize(test)
        print(tokens)
        postfix = " ".join(shunt(tokens))
        parse_tree = build_parse_tree(postfix)
        omnom = print_parse_tree(parse_tree)
        value = evaluate_parse_tree(parse_tree)
        value = round(value,2)
        if (value != expected_value):
            print(f"Test {enum} failed")
            print(postfix)
        else:
            print("LESFUCKIGNGO")

def calout(usrin, deci = 2):
    tokens = tokenize(usrin)
    postfix = " ".join(shunt(tokens))
    parse_tree = build_parse_tree(postfix)
    omnom = print_parse_tree(parse_tree)
    value = evaluate_parse_tree(parse_tree)
    value = round(value,deci)
    return value
    

if __name__ == "__main__":
  testing()