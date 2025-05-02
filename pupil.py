import math
import os
import platform
import random
import sys
import time

# inbuilt funcs
def msqrt(x):
    return math.sqrt(x)
def mfloor(x):
    return int(x)
def mceil(x):
    return math.ceil(x)
def msin(x):
    return math.sin(x)
def mcos(x):
    return math.cos(x)
def mtan(x):
    return math.tan(x)
def mround(x, d):
    return round(x, d)
def rint(min_, max_):
    return random.randint(min_, max_)
def tunix():
    return time.time()

# environment
debug = False
lineNum = 1
variables = {}
functions = {}
ifunctions = {"msqrt": msqrt, 
              "mfloor": mfloor, 
              "mceil": mceil, 
              "msin": msin, 
              "mcos": mcos, 
              "mtan": mtan, 
              "rint": rint, 
              "mround": mround,
              "tunix": tunix}

# clear console func
def clearCmd():
    s = platform.system()
    if s == "Windows":
        os.system('cls')
    elif s in ("Linux", "Darwin"):
        os.system('clear')
    else:
        print(f"Operating system not supported for clear ({filename}, {lineNum})")
        sys.exit(0)

# evaluate func
def evaluate(x):
    x = x.strip()

    # type
    if (x.startswith('"') and x.endswith('"')) or (x.startswith("'") and x.endswith("'")):
        return x[1:-1]
    if x == "true":
        return True
    if x == "false":
        return False
    if x == "null":
        return None
    try:
        return int(x)
    except ValueError:
        pass
    try:
        return float(x)
    except ValueError:
        pass

    # operators
    # will implement later
    
    # function calls
    if x.startswith("."):
        x, arg = x.split(" ", 1)
        if debug:
            print(f"Running function '{x[1:]}' ({filename}, {lineNum})")

        # parse arguments
        args = arg[1:-1].split(" ")
        for i, a in enumerate(args):
            args[i] = evaluate(a)

        # run function
        if x[1:] in ifunctions:
            return ifunctions[x[1:]](*args)
        if x[1:] in functions:
            pass # implement this later
        else:
            print(f"Function '{x[1:]}' not found ({filename}, {lineNum})")
            sys.exit(0)

    # variable
    if x in variables:
        return variables[x]
    else:
        print(f"Unable to evaluate {x} ({filename}, {lineNum})")
        sys.exit(0)

# parse as type func
def typeParse(x, typ):
    if debug:
        print(f"Parsing {x} as {typ} ({filename}, {lineNum})")
    
    try:
        # type
        if typ == "int":
            return int(x)
        elif typ == "flt":
            return float(x)
        elif typ == "str":
            return x
        elif typ == "bln":
            return bool(x)
        else:
            print(f"Unknown type '{typ}' ({filename}, {lineNum})")
            sys.exit(0)
    
    except ValueError:
        print(f"Unable to parse '{x}' as '{typ}' ({filename}, {lineNum})")
        sys.exit(0)
        
# check variable interference func
def varInter(x):
    invalid_chars = "1234567890`~!@#$%^&*(){}[]-+/\\.<>,;:'=\""
    reserved = "int,flt,bln,str,tunix,msqrt,mfloor,mceil,mfact,msin,mcos,mtan,masin,rint,rpick,sort,var,if,elseif,else,end,jump,jumpto,while,true,false,out,inp,func,get,wait,skip,stop".split(",")
    
    if any(c in x for c in invalid_chars) or x in reserved:
        print(f"Bad variable name '{x}' ({filename}, {lineNum})")
    else:
        return x

# arguments
if len(sys.argv) == 2:
    filename = os.path.join(sys.argv[1])
elif len(sys.argv) == 3:
    filename = os.path.join(sys.argv[1])
    if sys.argv[2] == "--debug":
        debug = True
        print("DEBUG MODE")
else:
    print("Usage: python pupil.py file.pil [--debug]")
    sys.exit(0)

# run file
with open(filename, "r") as file:
    lines = file.readlines()
    while lineNum <= len(lines):
        # line
        line = lines[lineNum - 1]

        # check for inline comments
        ign = False
        il = 0
        for l in line:
            if l == '"':
                ign = not ign
            if not ign:
                if l == "~" and line[il + 1] == "~":
                    line = line[:il]
                    if debug:
                        print(f"Inline comment found, ignoring ({filename}, {lineNum})")
                    break
            il += 1   

        # comment, skip, and empty
        if line.startswith("~~") or line.strip() in ["skip", ""]:
            if debug:
                print(f"Skipped line ({filename}, {lineNum})")

        # clear console
        elif line.strip() == "clear":
            if debug:
                print(f"Cleared console ({filename}, {lineNum})")
            else:
                clearCmd()

        # stop program
        elif line.strip() == "stop":
            if debug:
                print(f"Stopping program ({filename}, {lineNum})")
            sys.exit(0)

        # wait
        elif line.startswith("wait "):
            ms = line[5:]
            time.sleep(evaluate(ms) / 1000)
            if debug:
                print(f"Waited for '{ms.strip()}' ms ({filename}, {lineNum})")

        # variable
        elif line.startswith("var "):
            name, val = line[4:].split("=", 1)
            variables[varInter(name).strip()] = evaluate(val)
            if debug:
                print(f"Set variable '{name.strip()}' to '{val.strip()}' ({filename}, {lineNum})")

        # output
        elif line.startswith("out "):
            output = line[4:]
            print(evaluate(output))
            
        # input
        elif line.startswith("inp "):
            var, typ, ph = line[4:].split(" ", 2)
            if debug:
                print(f"Inputting {typ.strip()} {var.strip()} ({filename}, {lineNum})")
            variables[varInter(var)] = typeParse(input(evaluate(ph)), typ)
            if debug:
                print(f"Inputed {variables[var]} ({filename}, {lineNum})")

        # jump
        elif line.startswith("jump "):
            ln = line[5:]
            if debug:
                print(f"Jumping {ln.strip()} lines ({filename}, {lineNum})")
            lineNum += evaluate(ln)
            continue

        # jumpto
        elif line.startswith("jumpto "):
            ln = line[7:]
            if debug:
                print(f"Jumping to line {ln.strip()} ({filename}, {lineNum})")
            lineNum = evaluate(ln)
            continue

        # function call
        elif line.startswith("."):
            func, arg = line.split(" ", 1)
            if debug:
                print(f"Running function '{func[1:]}' ({filename}, {lineNum})")
            
            # parse arguments
            args = arg[1:-1].split(" ")
            for i, a in enumerate(args):
                args[i] = evaluate(a)

            # run function
            if func[1:] in ifunctions:
                ifunctions[func[1:]](*args)
            if func[1:] in functions:
                pass # implement this later
            else:
                print(f"Function '{func[1:]}' not found ({filename}, {lineNum})")
                sys.exit(0)

        # unknown
        else:
            print(f"Unable to parse '{line}' ({filename}, {lineNum})")
            sys.exit(0)

        # increment line
        lineNum += 1
