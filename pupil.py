import math
import os
import sys

# environment
variables = {}
debug = True
lineNum = 1

def evaluate(x):
    x = x.strip()

    # type
    if x.startswith('"') and x.endswith('"'):
        return x[1:-1]
    if x.lower() == 'true':
        return True
    if x.lower() == 'false':
        return False
    if x.lower() == 'null':
        return None
    try:
        return int(x)
    except ValueError:
        pass
    try:
        return float(x)
    except ValueError:
        pass

    # variable
    if x in variables:
        return variables[x]
    else:
        print(f"Unable to evaluate {x} ({filename}, {lineNum})")
        sys.exit(0)

# arguments
if len(sys.argv) == 2:
    filename = os.path.join(sys.argv[1])
elif len(sys.argv) == 3:
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

        # comment and skip
        if line.startswith("~~") or line == "skip":
            pass

        # variable declaration
        elif line.startswith("int "):
            name, val = evaluate(line[4:].split(" ", 1))
            variables[name] = int(val)
        elif line.startswith("flt "):
            name, val = evaluate(line[4:].split(" ", 1))
            variables[name] = float(val)
        elif line.startswith("str "):
            name, val = evaluate(line[4:].split(" ", 1))
            variables[name] = str(val)
        elif line.startswith("bln "):
            name, val = evaluate(line[4:].split(" ", 1))
            variables[name] = bool(val)
        #elif line.startswith("arr "):
            #name, val = evaluate(line[4:].split(" ", 1))
            #variables[name] = list(val)

        # output
        elif line.startswith("out "):
            arg = evaluate(line[4:])
            print(arg)

        # increment line
        lineNum += 1
