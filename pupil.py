import math
import os
import platform
import random
import sys
import time

# pupil, made by las-r on github
# version 0.7.0

# environment
debug = False
lineNum = 1
ignLines = False
inFunc = False
variables = {}
tempVars = {}
functions = {}
ifunctions = {"sqrt": math.sqrt, 
              "flr": int, 
              "ceil": math.ceil, 
              "sin": math.sin, 
              "cos": math.cos, 
              "tan": math.tan,
              "rnd": round,
              
              "rand": random.randint, 
              
              "unix": time.time,
              
              "str": str,
              "int": int,
              "flt": float,
              "bln": bool,
              "bin": bin,
              "hex": hex,
              "arr": list,
              
              "len": len,
              "range": range}
sys.set_int_max_str_digits(16384)
precedence = [
    ["++"],
    ["||"],
    ["&&"],
    ["==", "!=", "<", ">", "<=", ">="],
    ["|", "&", ":"],
    ["+", "-"],
    ["*", "/", "%"],
    ["^"]
]

# clear console func
def clearCmd():
    s = platform.system()
    if s == "Windows":
        os.system("cls")
    elif s in ("Linux", "Darwin"):
        os.system("clear")
    else:
        print(f"Operating system not supported for clear ({filename}, {lineNum})")
        sys.exit(1)

# tokenize func
def tokenize(x, spl):
    x = x.strip()
    if x == "":
        return []
    
    if debug:
        print(f"Tokenizing `{x}` by `{spl}` ({filename}, {lineNum})")

    tokenized = []
    token = ""
    in_string = False
    parens = 0
    brackets = 0
    infunc = False

    i = 0
    while i < len(x):
        c = x[i]

        # handle string
        if c == '"':
            in_string = not in_string
            token += c
            i += 1
            continue

        # handle function (starts with dot and ends with closing paren)
        if not in_string and not infunc and c == ".":
            if token:
                tokenized.append(token)
                token = ""
            infunc = True
            token += c
            i += 1
            continue
        if infunc:
            token += c
            if c == ")":
                infunc = False
                tokenized.append(token)
                token = ""
            i += 1
            continue

        # handle parentheses and brackets
        if not in_string:
            if c == "(":
                parens += 1
            elif c == ")":
                parens -= 1
            elif c == "[":
                brackets += 1
            elif c == "]":
                brackets -= 1

        # splitting logic
        if c == spl and not in_string and parens == 0 and brackets == 0:
            if token:
                tokenized.append(token)
                token = ""
        else:
            token += c

        i += 1

    if token:
        tokenized.append(token)
        
    if debug:
        print(f"Tokenized: `{tokenized}` ({filename}, {lineNum})")

    return tokenized

# blockify func
def blockify(it, lineNum):
    tags = ["end"]

    # if block
    if it:
        tags.append("else")
        tags.append("elif")

    # check for ending tag
    try:
        cur = lines[lineNum - 1].strip()
        while cur not in tags:
                lineNum += 1
                cur = lines[lineNum - 1].strip()
            
                # skip nested conditions
                if cur.startswith(("if ", "while ")):
                    lineNum = blockify(False, lineNum)
                
    except IndexError:
        print(f"Block doesn't have ending tag ({filename}, {lineNum})")
        sys.exit(1)

    # return end tag
    return lineNum

# Flattened set of all operators
all_ops = set(op for level in precedence for op in level)

def parseTokens(expr):
    tokens = []
    token = ""
    depth = 0
    for c in expr.strip():
        if c == " " and depth == 0:
            if token:
                tokens.append(token)
                token = ""
        else:
            if c in "([{" :
                depth += 1
            elif c in ")]}":
                depth -= 1
            token += c
    if token:
        tokens.append(token)
    return tokens

def findOp(tokens, ops):
    depth = 0
    for i in reversed(range(len(tokens))):
        tok = tokens[i]
        if tok == ")": depth += 1
        elif tok == "(": depth -= 1
        elif depth == 0 and tok in ops:
            return i
    return -1

def evaluateExpr(tokens):
    if len(tokens) == 1:
        return evaluate(tokens[0])

    for ops in precedence:
        i = findOp(tokens, ops)
        if i != -1:
            left = evaluateExpr(tokens[:i])
            right = evaluateExpr(tokens[i+1:])
            op = tokens[i]

            if op == "+": return left + right
            elif op == "-": return left - right
            elif op == "*": return left * right
            elif op == "/": return left / right
            elif op == "%": return left % right
            elif op == "^": return left ** right

            elif op == "&": return left & right
            elif op == "|": return left | right
            elif op == ":": return left ^ right

            elif op == "==": return left == right
            elif op == "!=": return left != right
            elif op == "<": return left < right
            elif op == ">": return left > right
            elif op in ["<=", "=<"]: return left <= right
            elif op in [">=", "=>"]: return left >= right
            elif op == "&&": return bool(left) and bool(right)
            elif op == "||": return bool(left) or bool(right)
            elif op == "::": return bool(left) ^ bool(right)

            elif op == "++": return str(left) + str(right)

            print(f"Unknown operator `{op}` ({filename}, {lineNum})")
            sys.exit(1)

    print(f"Invalid expression: {' '.join(tokens)} ({filename}, {lineNum})")
    sys.exit(1)

def evaluate(x):
    x = x.strip()
    if debug:
        print(f"Evaluating value `{x}` ({filename}, {lineNum})")
    
    # parenthesized expressions
    if x.startswith("(") and x.endswith(")"):
        return evaluate(x[1:-1])

    # split tokens with space logic
    tokens = tokenize(x, " ")
    if any(t in all_ops for t in tokens):
        return evaluateExpr(tokens)

    # primitives
    if x.startswith('"') and x.endswith('"'):
        return x[1:-1]
    if x.startswith("[") and x.endswith("]"):
        x = x[1:-1].split(",")
        return [evaluate(i.strip()) for i in x]
    if x.startswith("0b"):
        return int(x, 2)
    if x.startswith("0x"):
        return int(x, 16)
    if x == "true":
        return True
    if x == "false":
        return False
    if x == "null":
        return None
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            pass

    # array indexing
    if x.endswith("]") and "[" in x:
        name, idx = x[:-1].split("[", 1)
        return evaluate(name)[evaluate(idx)]

    # function
    if x.startswith("."):
        name, _, args = x[1:].partition("(")
        args = args[:-1] if args.endswith(")") else args
        arg_list = [evaluate(arg.strip()) for arg in tokenize(args, ",") if arg.strip()]
        if name in ifunctions:
            return ifunctions[name](*arg_list)
        elif name in functions:
            pass  # implement later
        else:
            print(f"Function `{name}` not found ({filename}, {lineNum})")
            sys.exit(1)

    # variable
    if x in variables:
        return variables[x]
    
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
    res = "int,flt,bln,str,unix,sqrt,flr,ceil,sin,cos,tan,rand,pick,sort,var,if,elif,else,end,jump,jumpto,while,true,false,out,inp,func,get,wait,skip,stop,ret,bin,hex,range".split(",")
    
    if any(c in x for c in invChars) or x in res:
        print(f"Bad variable name `{x}` ({filename}, {lineNum})")
        sys.exit(1)

# run line func
def runLine(line, inc):
    global lineNum, variables, functions
    
    if debug:
        print(f"Running line `{line}` ({filename}, {lineNum})")

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
        name, op, val = tokenize(line[4:], " ")
        varInter(name.strip())
        
        if op == "=":
            variables[name.strip()] = evaluate(val)
        else:
            if name in variables:
                if op == "+=":
                    variables[name.strip()] += evaluate(val)
                elif op == "-=":
                    variables[name.strip()] -= evaluate(val)
                elif op == "*=":
                    variables[name.strip()] *= evaluate(val)
                elif op == "/=":
                    variables[name.strip()] /= evaluate(val)
                elif op == "^=":
                    variables[name.strip()] **= evaluate(val)
                elif op == "%=":
                    variables[name.strip()] %= evaluate(val)
                    
                elif op == "&=":
                    variables[name.strip()] &= evaluate(val)
                elif op == "|=":
                    variables[name.strip()] |= evaluate(val)
                elif op == ":=":
                    variables[name.strip()] ^= evaluate(val)
                    
                elif op == "..=":
                    variables[name.strip()] = str(variables[name.strip()]) + str(evaluate(val))
                    
                else:
                    print(f"Assignment operator `{op}` not found ({filename}, {lineNum})")
                    sys.exit(1)
            else:
                print(f"Variable `{name}` not found ({filename}, {lineNum})")
                sys.exit(1)
        
        if debug:
            print(f"Set variable `{name.strip()}` to {variables[name.strip()]} ({filename}, {lineNum})")

    # output
    elif line.startswith("out "):
        output = line[4:]
        print(evaluate(output))

    # input
    elif line.startswith("inp "):
        var, typ, ph = tokenize(line[4:], " ")
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
        try:
            func, arg = line.split("(")
            args = [evaluate(a.strip()) for a in arg.split(",") if a.strip()]
        except ValueError:
            func = line

        if debug:
            print(f"Running function `{func[1:]}` ({filename}, {lineNum})")

        # run function
        if func[1:] in ifunctions:
            ifunctions[func[1:]](*args)
        if func[1:] in functions:
            for line in functions[func[1:]].split(";"):
                runLine(line.strip(), False)
        else:
            print(f"Function `{func[1:]}` not found ({filename}, {lineNum})")
            sys.exit(1)

    # if
    elif line.startswith("if "):
        arg = evaluate(line[3:])

        if debug:
            print(f"Checking if ({filename}, {lineNum})")

        # run block
        bNum = blockify(True, lineNum)
        if arg:
            if debug:
                print(f"Running if ({filename}, {lineNum})")

            lineNum += 1
            while lineNum < bNum:
                runLine(lines[lineNum - 1].strip(), True)
            lineNum = blockify(False, lineNum)
            
        # else & elif
        else:
            if debug:
                print(f"Skipping if ({filename}, {lineNum})")

            lineNum = bNum
            eLine = lines[lineNum - 1].strip()
            
            # else
            if eLine == "else":
                if debug:
                    print(f"Running else ({filename}, {lineNum})")
                
                # run b;pcl
                lineNum += 1
                while lineNum < blockify(True, lineNum):
                    runLine(lines[lineNum - 1].strip(), True)
                lineNum = blockify(False, lineNum)

    # while
    elif line.startswith("while "):
        args = line[6:]
        wNum = lineNum + 1

        if debug:
            print(f"Checking while ({filename}, {lineNum})")

        # run block
        bNum = blockify(False, lineNum)
        lineNum += 1

        if debug:
            print(f"Running while ({filename}, {lineNum})")

        while evaluate(args):
            while lineNum < bNum:
                runLine(lines[lineNum - 1].strip(), True)
            lineNum = wNum
        lineNum = bNum

        if debug:
            print(f"Finishing while ({filename}, {lineNum})")

    # for
    elif line.startswith("for "):
        i, array = tokenize(line[4:], " ")
        array = evaluate(array)

        wNum = lineNum + 1
        variables[i] = None
        
        bNum = blockify(False, lineNum)
        lineNum += 1

        if debug:
            print(f"Running for ({filename}, {lineNum})")

        for n in array:
            variables[i] = n
            while lineNum < bNum:
                runLine(lines[lineNum - 1].strip(), True)
            lineNum = wNum
        lineNum = bNum

        if debug:
            print(f"Finishing for ({filename}, {lineNum})")

    # function definition
    elif line.startswith("func "):
        name = line[5:]
        endLine = blockify(False, lineNum)
        function = ""

        # add lines to function
        lineNum += 1
        while lineNum < endLine:
            function += f"{lines[lineNum - 1].strip()};"
            lineNum += 1

        # debug
        if debug:
            print(f"Defined function `{name.strip()}` as `{function}` ({filename}, {lineNum})")
        
        # add function to list
        functions[name.strip()] = function

    # return
    elif line.startswith("ret "):
        if inFunc:
            pass # implement this later
        else:
            print(f"Return outside of function ({filename}, {lineNum})")
            sys.exit(1)

    # unknown
    else:
        print(f"Unable to parse line `{line}` ({filename}, {lineNum})")
        sys.exit(1)

    # increment line
    if inc:
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
    print("Pupil v0.5.1\nUsage: python pupil.py file.pil [--debug]")
    sys.exit(1)

# run file
try:
    with open(filename, "r") as file:
        lines = file.readlines()
        while lineNum <= len(lines):
            runLine(lines[lineNum - 1].strip(), True)
except FileNotFoundError:
    print(f"File `{filename}` not found")
    sys.exit(1)
except KeyboardInterrupt:
    print(f"Program interrupted by user ({filename}, {lineNum})")
    sys.exit(0)
