import re
import sys
import os
import math
import random
import time

# script vars
debug = False
lineN = 0

# environment
variables = {}

# clear console function
def clearconsole():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

# mathematical functions
def msqrt(x):
    return math.sqrt(x)
def msin(x):
    return math.sin(math.radians(x))
def mcos(x):
    return math.cos(math.radians(x))
def mtan(x):
    return math.tan(math.radians(x))
def masin(x):
    return math.degrees(math.asin(x))
def macos(x):
    return math.degrees(math.acos(x))
def matan(x):
    return math.degrees(math.atan(x))
def mcot(x):
    return 1 / math.tan(math.radians(x))
def msec(x):
    return 1 / math.cos(math.radians(x))
def mcsc(x):
    return 1 / math.sin(math.radians(x))
def sort(x):
    return sorted(x)

# random functions
def rint(minval, maxval):
    return random.randint(minval, maxval)
def rpick(array):
    return random.choice(array)

# time functions
def tunix():
    return int(time.time())

# evaluation function
def evaluate(expr):
    try:
        original = expr

        # replace variables
        for var in sorted(variables, key=len, reverse=True):
            value = variables[var]
            if isinstance(value, str):
                expr = re.sub(rf'\b{re.escape(var)}\b', f'"{value}"', expr)
            else:
                expr = re.sub(rf'\b{re.escape(var)}\b', str(value), expr)

        # convert concatenation expressions
        if '+' in expr:
            parts = [p.strip() for p in expr.split('+')]
            if any(p.startswith('"') and p.endswith('"') for p in parts):
                expr = ' + '.join(f'str({p})' if not (p.startswith('"') and p.endswith('"')) else p for p in parts)

        if debug:
            print(f"[eval] {original} → {expr} ({lineN})")

        return eval(expr)
    except Exception as e:
        if debug:
            print(f"[error] Failed to eval '{expr}': {e}")
        return f"Error: {e}"
        sys.exit(0)

# line runner
def runline(line):
    global lineN

    line = line.strip()
    if not line:
        return
    
    if debug:
        print(f"> {line}")

    # variables
    if line.startswith("str "):
        _, name, _, value = line.split(" ", 3)
        variables[name] = value.strip('"')
        if debug:
            print(f"[set] str {name} = \"{variables[name]}\"")
    elif line.startswith("int "):
        _, name, _, value = line.split(" ", 3)
        variables[name] = int(value)
        if debug:
            print(f"[set] int {name} = {variables[name]}")
    elif line.startswith("flt "):
        _, name, _, value = line.split(" ", 3)
        variables[name] = float(value)
        
        if debug:
            print(f"[set] flt {name} = {variables[name]} ({lineN})")
    
    # output 
    elif line.startswith("out "):
        expr = line[4:].strip()
        result = evaluate(expr)
        print(result)
    
    # clear console
    elif line == "wipe":
        clearconsole()
        
        if debug:
            print(f"[wipe] Console cleared. ({lineN + 1})")
    
    # input
    elif line.startswith("inp "):
        type_, var, placeholder = line[4:].strip().split(" ", 2)
        if type_ == "int":
            variables[var] = int(input(evaluate(placeholder)))
        elif type_ == "flt":
            variables[var] = float(input(evaluate(placeholder)))
        elif type_ == "str":
            variables[var] = str(input(evaluate(placeholder)))
        else:
            print(f"Error: 'inp' expects int, flt, or str. ({lineN + 1})")
            sys.exit(0)
            
        if debug:
            print(f"[inp] {type_} {var} has been set ({lineN + 1})")
            
    # wait
    elif line.startswith("wait "):
        ms = evaluate(line[5:].strip())
        time.sleep(ms / 1000)

    # jump
    elif line.startswith("jump "):
        l = int(evaluate(line[5:].strip()))
        lineN += l

    # jumpto
    elif line.startswith("jumpto "):
        l = int(evaluate(line[7:].strip()))
        lineN = l - 1

    # skip & comments
    elif line == "skip" or line.startswith("~~ "):
        pass

        if debug:
            print(f"[skip] line ({lineN + 1})")

    # stop
    elif line == "stop":
        if debug:
            print(f"[stop] program stopped ({lineN + 1})")

        sys.exit(0)

    # if
    elif line.startswith("if "):
        cond = line[3:].split(" ", 2)
        if len(cond) < 3:
            print(f"Syntax error in if condition ({lineN + 1})")
            sys.exit(0)

        conda = evaluate(cond[0])
        oper = cond[1]
        condb = evaluate(cond[2])

        # evaluate condition
        if oper == "==":
            condr = conda == condb
        elif oper == ">":
            condr = conda > condb
        elif oper == ">=":
            condr = conda >= condb
        elif oper == "<":
            condr = conda < condb
        elif oper == "<=":
            condr = conda <= condb
        elif oper == "!=":
            condr = conda != condb
        elif oper == "||":
            condr = bool(conda) or bool(condb)
        elif oper == "&&":
            condr = bool(conda) and bool(condb)
        elif oper == "::":
            condr = bool(conda) ^ bool(condb)
        else:
            print(f"Unknown operator '{oper}' ({lineN + 1})")
            sys.exit(0)

        # Decide where to go
        block_start = lineN + 1
        block_end = block_start
        found_else = False
        found_end = False

        # Locate block boundaries
        while block_end < len(lines):
            test_line = lines[block_end].strip()
            if test_line.startswith("else") or test_line.startswith("elseif"):
                if not found_else:
                    else_start = block_end
                    found_else = True
            if test_line == "end":
                found_end = True
                break
            block_end += 1

        if not found_end:
            print(f"Error: missing 'end' for if statement ({lineN + 1})")
            sys.exit(0)

        if condr:
            # Run the true block
            lineN = block_start
            while lineN < len(lines):
                check_line = lines[lineN].strip()
                if check_line in ["else", "elseif", "end"]:
                    break
                runline(lines[lineN])
                lineN += 1
        else:
            # Skip to 'else' or after 'end'
            if found_else:
                lineN = else_start + 1
                while lineN < block_end:
                    runline(lines[lineN])
                    lineN += 1
            else:
                lineN = block_end  # go to line after end
    
    # unknown
    else:
        if debug:
            print(f"Unknown command or function ({lineN + 1}")
        
        sys.exit(0)

# main
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python pupil.py file.pil [--debug]")
else:
    if len(sys.argv) == 3 and sys.argv[2] == "--debug":
        debug = True

    filename = sys.argv[1]

    with open(filename) as f:
        lines = f.readlines()
        while lineN < len(lines):
            current = lineN
            runline(lines[lineN])
            if lineN == current:
                lineN += 1