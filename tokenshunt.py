import re
import math
from collections import namedtuple

# Function that returns true if there is a dot in a string
def is_dot(tok):
    for i in tok:
        if i == '.':
            return True
        
# A function that calculates sin, cos or tan
def trigon(function,input,deg_mode = 0):
    if deg_mode == 1: # Radians
        if function == "sin":
            return math.sin(input)
        elif function == "cos":
            return math.cos(input)
        elif function == "tan":
            return math.tan(input)
    else:
        if function == "sin":
            return math.sin(math.radians(input))
        elif function == "cos":
            return math.cos(math.radians(input))
        elif function == "tan":
            return math.tan(math.radians(input))



# Function that calculates 2 numbers with an operator
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
        
# Creates namedtuple opinfo that has operators, their precedence and whether they are left or right side associated, and then create a dict that has the operators as keys
opinfo = namedtuple('Operator', 'precedence associativity')
operator_info = {
    "+": opinfo(0, "L"),
    "-": opinfo(0, "L"),
    "*": opinfo(1, "L"),
    "/": opinfo(1, "L"),
    "!": opinfo(2, "L"),
    "^": opinfo(2, "R"),
}

functions = [
    "sin",
    "cos",
    "tan"
]

def tokenize(in_str):
    cleaned = re.sub(r"\s+", "", in_str)
    chars = list(cleaned)
    output = []
    buf = ""
    state = ""
    new_str = ""

    while len(chars) != 0:
        # Pop first string element from chars, while loop above ensures that chars is not empty
        char = chars.pop(0)

        # If the popped string is a number or a ".", it will check whether state is a number or not
        if char.isdigit() or char == ".":
            if state != "num":
                # Here it adds the complete string, either a number or an operator, to the list from buf if buf is not empty and resets buf
                output.append(buf) if buf != "" else False
                buf = ""
            # Sets state to "num" and adds char to buf
            state = "num"
            buf += char
        
        # If the popped string is an operator or parentheses, add buf to the output if it isn't already empty and reset it
        elif char in operator_info.keys() or char in ["(", ")"]:
            output.append(buf) if buf != "" else False
            buf = ""
            # Add char to output
            output.append(char)
        
        # Same as the others, but for functions and letters
        else:
            if state != "func":
                output.append(buf) if buf != "" else False
                buf = ""
            state = "func"
            new_str += char
            if new_str in functions:
                output.append(new_str)
                new_str = ""

    # Add buf to output if it isn't empty and then return output
    output.append(buf) if buf != "" else False
    return output
        
# This is the function that will shunt the tokenized string and return it as a list, that can be used when building the parsing tree
def shunt(tokens):
    tokens += ["end"]
    operators = []
    output = []
    tri_funcs = []

    while len(tokens) != 1:
        tok = tokens.pop(0)

        # If the popped token is a number or a dot, append it to the output list
        if tok.isdigit() or is_dot(tok):
            output.append(tok)

        # If the popped token is an operator present in the keys of the operator_info tuple, make sure that the operator list is not empty 
        elif tok in operator_info.keys():
            # Create a while loop that will check for precedence for the operators and pop the operator with higher precedence to the output list
            while len(operators) != 0:
                satisfied = False

                # Checks if the previous element in the list is a letter, sets the satisfied bool if true
                if operators[-1].isalpha():
                    satisfied = True
                
                # If the previous element in the list is not parentheses, then it checks the presedence of the operator against the presedence of the previous operator in the list
                if operators[-1] not in ["(", ")", functions]:
                    # Sets satisfied to True if toks precedence is lower than the presedence of the previous element
                    if operator_info[operators[-1]].precedence > operator_info[tok].precedence:
                        satisfied = True
                    # Sets satisfied to True if the precedence of tok and the previous element are the same AND if the previous element has left associativity
                    elif operator_info[operators[-1]].precedence == operator_info[tok].precedence and operator_info[operators[-1]].associativity == "left":
                        satisfied = True
                # Makes sure the previous element in the list is not a left parentheses and then breaks the while loop if satisfied is not True
                satisfied = satisfied and operators[-1] != "("

                if not satisfied:
                    break

                output.append(operators.pop())
            operators.append(tok)
        # Adds start parentheses to the operator list and if tok is an end parentheses, it will pop from the operators list until it encounters a start parentheses
        elif tok == "(" or tok in functions:
            operators.append(tok)
        elif tok == ")":
            while len(operators) != 0 and operators[-1] != "(":
                output.append(operators.pop())
            # Pop the operators list to get rid of the start parentheses and append the last element of operators to output if it's a trigonometric function
            operators.pop()
            if len(operators) != 0 and operators[-1] in functions:
                output.append(operators.pop())
        else:
            operators.append(tok)
    # Iterates through operators and adds them to the output
    output.extend(operators[::-1])

    return output

# Creates a class and creates the objects value, left and right
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# This function builds a parse tree from the postfix expression provided by shunt()
def parse_tree(postfix_expression):
    stack = []
    
    # Iterates through the shunted list and creates a node for all the numbers
    for token in postfix_expression:
        if token.isdigit() or is_dot(token):
            node = Node(token)
            stack.append(node)
        # If the token is a trigonometric function, it pops once from the stack to right_node and creates a node and a right node for the trigonometric function
        elif len(stack) > 0 and token in functions:
            right_node = stack.pop()
            node = Node(token)
            node.right = right_node
            stack.append(node)
        # If the stack has more than 2 elements and the input is not a number, it will pop the 2 most recent nodes as right and left
        elif len(stack) > 1:
            right_node = stack.pop()
            left_node = stack.pop()
            # Creates a node for the operator token and assigns the left and right nodes as it's respective nodes and then appends it to the stack
            node = Node(token)
            node.left = left_node 
            node.right = right_node
            stack.append(node)
    return stack[0]

# This function constructs the parse tree visually
def print_parse_tree(node, indent=''):
    if node is None:
        return
    
    print(indent + node.value)
    
    if node.left:
        print_parse_tree(node.left, indent + '  |__')
    
    if node.right:
        print_parse_tree(node.right, indent + '  |__')

# This function goes through the parse tree and calculates it with the calculator
def evaluate_parse_tree(node):
    if node is None:
        return 
    
    # Evaluates first the left then the right nodes of the tree through recursion. This type of evaluation is called depth first search
    left_node = evaluate_parse_tree(node.left)
    right_node = evaluate_parse_tree(node.right)
    
    # Returns the value of the node if it's a leaf node and returns the calculated result of the 2 child nodes if the node is an operator
    if (left_node is None or right_node is None) and node.value not in functions:
        return float(node.value)
    elif node.value in functions:
        return trigon(node.value, right_node,1) 
    else:
        return calculator(left_node, right_node, node.value)
    
def calout(usrin, deci = 2):
    tokens = tokenize(usrin)
    postfix = (shunt(tokens))
    print(postfix)
    tree = parse_tree(postfix)
    omnom = print_parse_tree(tree)
    value = evaluate_parse_tree(tree)
    value = round(value,deci)
    print(value)
    return value

def testing():
    tests = [
    ("5*sin(9/5)", 4.87),
    ("5*cos(9/5)", -1.14),
    ("5*tan(9/5)", -21.43),
    ("(6*cos(sin(9/5)/2))^3", 149.10),
    ("(6*cos(6*sin(9/5)/2))^3", -200.75),
    ("( 5 / 9 ) * 9 ^ 2", 45),
    ("( 5 ^ 2 / 9 ) * 3", 8.33),
    ("((5^3/9^2)^2)/10", 0.24)
    ]
    for enum, (test, expected_value) in enumerate(tests):
        print(test)
        tokens = tokenize(test)
        print(tokens)
        postfix = shunt(tokens)
        tree = parse_tree(postfix)
        print_parse_tree(tree)
        value = evaluate_parse_tree(tree)
        value = round(value,2)
        if (value != expected_value):
            print(f"Test {enum} failed")
            print(postfix)
            print(value)
        else:
            print("LESFUCKIGNGO")
            print(postfix)
            print(value)


if __name__ == "__main__":
    testing()