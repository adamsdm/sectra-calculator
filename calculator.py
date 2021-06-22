#!/usr/bin/python3

# Calculator.py
# 2021-06-21
# Adam Söderström

import sys

# 'registry' is a tree structure represented by a dictionary of lists.
# When an expression is evaluated, the tree is recursively traversed.
#         foo
#         / \ 
#       add sub
#       /     \
#     bar     10
#     / \
#   add mult
#   /     \
#  2       3
# 
registry = {}
operations = {
    "add"       : (lambda a, b : a + b),
    "subtract"  : (lambda a, b : a - b),
    "multiply"  : (lambda a, b : a * b),    
}

def print_help() :
    print("Invalid input!") 
    print("Enter input according to:")
    print(" - <register> <operation> <value>")
    print(" - print <register>")
    print(" - quit")

# Recursively evaluates expression and calculates result of all operations
# "expression" is an array of pairs, e.g ['add', 'foo'], [multiply, bar], [suctract, 2]
def evaluate_expression(expression, curr_depth) :
    curr_depth += 1 
    if(curr_depth >= sys.getrecursionlimit()) :
        raise RecursionError

    result = 0
    for op in expression :
        oper = op[0]
        rvalue = op[1]
        # If rvalue is an int, it should simply be added/subtracted/multiplied
        try :
            result = operations[oper](result, int(rvalue))
        except ValueError :
            if(rvalue in registry) :# If rvalue is a register, it has to be evaluated first.
                result = operations[oper](result, evaluate_expression(registry[rvalue], curr_depth))
            else : # If rvalue is not in registry, it is regarded to be zero.
                result = operations[oper](result, 0)
    return result

# Parses and validates input from an array of strings
# input_strings is an array consisting of [rvalue, operator, lvalue]
def parse_input(input_strings) :
    no_inputs = len(input_strings)
    # Validate inputs
    if(no_inputs == 1) :
        if(input_strings[0] == "quit") :
            print("Goodbye!")
            exit(0)
        else : 
            print_help()

    elif(no_inputs == 2) :
        if(input_strings[0] == "print") :
            reg = input_strings[1]
            if(reg in(registry)) : # Check if key exists in registry
                try :
                    print(evaluate_expression(registry[reg], 0))
                except RecursionError:
                    print("Recursion error!")
            else : 
                print("register '" + reg + "' is not defined!")
        else : 
            print_help()

    elif(no_inputs == 3) :
        lvalue = input_strings[0] # input_strings[0] should always be an register
        oper   = input_strings[1] # input_strings[1] should always be an operation
        rvalue = input_strings[2] # input_strings[2] could either be a register or an integer
        
        # Validate lvalue
        if(lvalue.isalnum() and lvalue not in operations) :
            if(lvalue not in registry) : # add lvalue to registry if not already present
                registry[lvalue] = []
        else :
            print("'" + lvalue + "' is not a valid registry name!")
            return

        # Validate oper
        if(oper not in operations) :
            print("'" + oper + "' is not a valid operation!")
            print_help()
            return

        # Validate rvalue
        try : 
            int(rvalue) # If rvalue is an int we dont need to add it to the registry
        except ValueError:
            if(rvalue.isalnum()  and rvalue not in operations) :
                if(rvalue not in registry) : # add rvalue to registry if not already present
                    registry[rvalue] = []
            else :
                print("'" + rvalue + "' is not a valid registry name!")
                return 

        # All inputs have been validated and we can safely append the operation to the node 'lvalue'
        registry[lvalue].append([oper, rvalue])

    else :
        print_help()
    
def run_calc_from_file(fpath) :
    # Try to read file
    try :
        f = open(fpath, "r")
        lines = f.readlines()
        for l in lines :
            parse_input(l.lower().split())
        f.close()
        exit(0)
    except FileNotFoundError :
        print("File not found: '" + fpath + "'")
        exit(1)

def run_calc_interactively() :
    # Main loop
    while True :
        parse_input(input(">> ").lower().split())
    
def run_calculator() :
    if(len(sys.argv) > 1) :
        fpath = sys.argv[1]
        run_calc_from_file(fpath)
    else :
        run_calc_interactively()
    

if __name__ == "__main__" :
    run_calculator()
