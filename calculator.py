#!/usr/bin/python3

operations = {
    "add"       : (lambda a, b : a + b),
    "subtract"  : (lambda a, b : a - b),
    "multiply"  : (lambda a, b : a * b),    
}
registry = {}

def print_help() :
    print("Invalid input!") 
    print("Enter input according to:")
    print(" - <register> <operation> <value>")
    print(" - print <register>")
    print(" - quit")

def evaluate_expression(expression) :
    result = 0
    for op in expression :
        oper = op[0]
        rvalue = op[1]

        # If rvalue is an int, it should simply be added/subtracted/multiplied
        try :
            result = operations[oper](result, int(rvalue))
        except ValueError :
            if(rvalue in registry) :# If rvalue is a register, it has to be evaluated first.
                result = operations[oper](result, evaluate_expression(registry[rvalue]))
            else : # If rvalue is not in registry, it is regarded to be zero.
                result = operations[oper](result, 0)
    return result



def parse_input(input_strings) :
    no_inputs = len(input_strings)
    # Validate inputs
    if(no_inputs == 1) :
        if(input_strings[0] == "quit") :
            print("Goodbye!")
            exit()
        elif(input_strings[0] == "dump") : #TODO REMOVE
            print(registry)
        else : 
            print_help()

    elif(no_inputs == 2) :
        if(input_strings[0] == "print") :
            reg = input_strings[1]
            if( reg in(registry) ) : # Check if key exists in registry
                result = evaluate_expression(registry[reg])
                print(result)
            else : 
                print("register '" + reg + "' is not defined!")
        else : 
            print_help()

    elif(no_inputs == 3) :
        lvalue = input_strings[0] # input_strings[0] should always be an register
        oper   = input_strings[1] # input_strings[1] should always be an operation
        rvalue = input_strings[2] # input_strings[2] could either be a register or an integer
        
        # Validate lvalue
        if(lvalue.isalnum()) :# Is lvalue alphanumerical?
            if(lvalue not in registry) : # add lvalue to registry if not already present
                registry[lvalue] = []
        else :
            print(lvalue + " is not an valid identifier!")
            return

        # Validate rvalue
        try : 
            int(rvalue) # If rvalue is an int we dont need to add it to the registry
        except ValueError:
            if(rvalue.isalnum()) : # Is lvalue alphanumerical?
                if(lvalue not in registry) : # add rvalue to registry if not already present
                    registry[rvalue] = []
            else :
                print(lvalue + " is not an valid identifier!")
                return 

        # Validate oper
        if(oper not in operations) :
            print("'" + oper + "' is not a valid operation!")
            print_help()
            return

        # All inputs have been validated
        registry[lvalue].append([oper, rvalue])

    else :
        print_help()
    

def run_calculator() :

    # TODO: Handle file input

    # Main loop
    while True :
        parse_input( input(">> ").lower().split() )

if __name__ == "__main__" :
    run_calculator()