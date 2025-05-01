import math
import os
import platform
import random
import sys
import time

# environment
variables = {}
functions = {}
debug = False
lineNum = 1

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
    if x.startswith('"') and x.endswith('"'):
        return x[1:-1]
    if x == 'true':
        return True
    if x == 'false':
        return False
    if x == 'null':
        return None
    try:
        return int(x)
    except ValueError:
        pass
    try:
        return float(x)
    except ValueError:
        pass
    
    # inbuilt functions
    if x == "tunix":
        return time.time()

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
    reserved = "int,flt,bln,str,tunix,msqrt,mfloor,mceil,mfact,msin,mcos,mtan,masin,macos,matan,mcot,msec,mcsc,rint,rpick,sort,var,if,elseif,else,end,jump,jumpto,while,true,false,out,inp,func,get,wait,skip,stop".split(",")
    
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

        # comment and skip
        if line.startswith("~~") or line.strip() == "skip":
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
                print(f"Waited for {ms.strip()} ms ({filename}, {lineNum})")

        # variable
        elif line.startswith("var "):
            name, val = line[4:].split("=", 1)
            variables[varInter(name).strip()] = evaluate(val)
            if debug:
                print(f"Set variable {name.strip()} to {val.strip()} ({filename}, {lineNum})")

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

        # unknown
        else:
            print(f"Unable to parse '{line}' ({filename}, {lineNum})")
            sys.exit(0)

        # increment line
        lineNum += 1
