import math
import os
import platform
import random
import sys
import time

# pupil, made by las-r on github
# version 0.3.0

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
def rint(n, x):
    return random.randint(n, x)
def tunix():
    return time.time()
def ystr(x):
    return str(x)
def yint(x):
    return int(x)
def yflt(x):
    return float(x)
def ybln(x):
    return bool(x)

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
              "tunix": tunix,
              "str": ystr,
              "int": yint,
              "flt": yflt,
              "bln": ybln}

# clear console func
def clearCmd():
    s = platform.system()
    if s == "Windows":
        os.system('cls')
    elif s in ("Linux", "Darwin"):
        os.system('clear')
    else:
        print(f"Operating system not supported for clear ({filename}, {lineNum})")
        sys.exit(1)

# tokenize func
def tokenize(x):
    x = x.strip()

    # tokenized output
    tokenized = []

    # empty string check
    if x == "":
        return tokenized

    # inter over chars
    igns = False
    token = ""
    for c in x:
        # ignore strings
        if c == '"':
            igns = not igns

        # split
        if not igns:
            if c == " ":
                if token:
                    tokenized.append(token)
                    token = ""
            else:
                token += c
        else:
            token += c
    
    # last token (if any)
    if token:
        tokenized.append(token)

    return tokenized

# blockify func
def blockify(it):
    global lineNum
    eNum = lineNum
    tags = ["end"]

    # if block
    if it:
        tags.append("else")
        tags.append("elif")

    # check for ending tag
    try:
        while lines[eNum - 1].strip() not in tags:
                eNum += 1
    except IndexError:
        print(f"Block doesn't have ending tag ({filename}, {lineNum})")
        sys.exit(1)

    # return end tag
    return eNum

# evaluate func
def evaluate(x):
    x = x.strip()
    if debug:
        print(f"Evaluating value `{x}` ({filename}, {lineNum})")

    # empty
    if x == "":
        return
    
    # operators
    tokens = tokenize(x)
    if len(tokens) >= 3 and len(tokens) % 2 == 1:
        total = evaluate(tokens[0])
        i = 1
        while i < len(tokens):
            op = tokens[i]
            val = evaluate(tokens[i + 1])

            # arithmetic
            if op == "+":
                total += val
            elif op == "-":
                total -= val
            elif op == "*":
                total *= val
            elif op == "/":
                total /= val
            elif op == "^":
                total **= val
            elif op == "%":
                total %= val

            # bitwise
            elif op == "&":
                total &= val
            elif op == "|":
                total |= val
            elif op == ":":
                total ^= val

            # boolean
            elif op == "==":
                total = total == val
            elif op == "!=":
                total = total != val
            elif op == ">":
                total = total > val
            elif op == "<":
                total = total < val
            elif op in [">=", "=>"]:
                total = total >= val
            elif op in ["<=", "=<"]:
                total = total <= val
            elif op == "&&":
                total = total and val
            elif op == "||":
                total = total or val
            elif op == "::":
                total = bool(total) ^ bool(val)

            # concatenate
            elif op == "..":
                total = str(total) + str(val)
            
            # unknown
            else:
                print(f"Unknown operator `{op}` ({filename}, {lineNum})")

            i += 2
        return total

    # type
    if (x.startswith('"') and x.endswith('"')):
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
    
    # function calls
    if x.startswith("."):
        fc = x.split("(")
        if debug:
            print(f"Running function `{fc[0][1:]}` ({filename}, {lineNum})")

        # parse arguments
        if len(fc) == 2:
            arg = fc[1][:-1]
            args = [evaluate(a.strip()) for a in arg.split(",") if a.strip()]
        else:
            args = []

        # run function
        fc = fc[0][1:]
        if fc in ifunctions:
            try:
                return ifunctions[fc](*args)
            except TypeError:
                print(f"Function `{fc}` missing one or more arguments ({filename}, {lineNum})")
                sys.exit(1)
        elif fc in functions:
            pass # implement this later
        else:
            print(f"Function `{fc[0][1:]}` not found ({filename}, {lineNum})")
            sys.exit(1)

    # variable
    if x in variables:
        return variables[x]
    else:
        print(f"Unable to evaluate value `{x}` ({filename}, {lineNum})")
        sys.exit(1)

# parse as type func
def typeParse(x, typ):
    if debug:
        print(f"Parsing `{x}` as `{typ}` ({filename}, {lineNum})")
    
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
            print(f"Unknown type `{typ}` ({filename}, {lineNum})")
            sys.exit(1)
    
    except ValueError:
        print(f"Unable to parse value `{x}` as type `{typ}` ({filename}, {lineNum})")
        sys.exit(1)
        
# check variable interference func
def varInter(x):
    invChars = "1234567890`~!@#$%^&*(){}[]-+/\\.<>,;:'=\""
    res = "int,flt,bln,str,tunix,msqrt,mfloor,mceil,mfact,msin,mcos,mtan,masin,rint,rpick,sort,var,if,elif,else,end,jump,jumpto,while,true,false,out,inp,func,get,wait,skip,stop".split(",")
    
    if any(c in x for c in invChars) or x in res:
        print(f"Bad variable name `{x}` ({filename}, {lineNum})")
        sys.exit(1)

# run line func
def runLine(line):
    global lineNum, variables, functions

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
                    print(f"Ignoring inline comment ({filename}, {lineNum})")
                break
        il += 1   

    # comment, skip, and empty
    if line.startswith("~~") or line.strip() in ["skip", ""]:
        if debug:
            print(f"Skipping ({filename}, {lineNum})")

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
            print(f"Waited for `{ms.strip()}` ms ({filename}, {lineNum})")

    # variable
    elif line.startswith("set "):
        name, val = line[4:].split("=", 1)
        varInter(name.strip())

        variables[name.strip()] = evaluate(val)
        if debug:
            print(f"Set variable `{name.strip()}` to `{val.strip()}` ({filename}, {lineNum})")

    # output
    elif line.startswith("out "):
        output = line[4:]
        print(evaluate(output))

    # input
    elif line.startswith("inp "):
        var, typ, ph = tokenize(line[4:])
        varInter(var)

        if debug:
            print(f"Inputting `{typ.strip()}`, an `{var.strip()}` ({filename}, {lineNum})")
        variables[var] = typeParse(input(evaluate(ph)), typ)
        if debug:
            print(f"Inputed `{variables[var]}` ({filename}, {lineNum})")

    # jump
    elif line.startswith("jump "):
        ln = line[5:]
        if debug:
            print(f"Jumping `{ln.strip()}` lines ({filename}, {lineNum})")

        lineNum += evaluate(ln)
        return

    # jumpto
    elif line.startswith("jumpto "):
        ln = line[7:]
        if debug:
            print(f"Jumping to line `{ln.strip()}` ({filename}, {lineNum})")

        lineNum = evaluate(ln)
        return

    # function call
    elif line.startswith("."):
        func, arg = line.split("(")
        if debug:
            print(f"Running function `{func[1:]}` ({filename}, {lineNum})")

        # parse arguments
        args = [evaluate(a.strip()) for a in arg.split(",") if a.strip()]

        # run function
        if func[1:] in ifunctions:
            ifunctions[func[1:]](*args)
        if func[1:] in functions:
            pass # implement this later
        else:
            print(f"Function `{func[1:]}` not found ({filename}, {lineNum})")
            sys.exit(1)

    # if
    elif line.startswith("if "):
        arg = evaluate(line[3:])

        if debug:
            print(f"Checking if ({filename}, {lineNum})")

        # run block
        bNum = blockify(True)
        if arg:
            if debug:
                print(f"Running if ({filename}, {lineNum})")

            lineNum += 1
            while lineNum < bNum:
                runLine(lines[lineNum - 1].strip())
        else:
            if debug:
                print(f"Skipping if ({filename}, {lineNum})")

            lineNum = bNum

    # while
    elif line.startswith("while "):
        arg = evaluate(line[6:])
        wNum = lineNum

        if debug:
            print(f"Checking while ({filename}, {lineNum})")

        # run block
        bNum = blockify(True)
        while arg:
            arg = evaluate(lines[wNum - 1].strip()[6:])
            lineNum += 1
            while lineNum < bNum:
                runLine(lines[lineNum - 1].strip())

        if debug:
            print(f"Finishing while ({filename}, {lineNum})")

    # unknown
    else:
        print(f"Unable to parse line `{line}` ({filename}, {lineNum})")
        sys.exit(1)

    lineNum += 1

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
    sys.exit(1)

# run file
try:
    with open(filename, "r") as file:
        lines = file.readlines()
        while lineNum <= len(lines):
            runLine(lines[lineNum - 1].strip())
except FileNotFoundError:
    print(f"File `{filename}` not found")
    sys.exit(1)
