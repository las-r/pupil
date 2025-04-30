import math
import os
import platform
import random
import sys
import time

# environment
variables = {}
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
        print("Operating system not supported.")

# evaluate func
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

        # comment and skip
        if line.startswith("~~") or line.strip() == "skip":
            pass
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
            variables[name.strip()] = evaluate(val)
            if debug:
                print(f"Set variable {name.strip()} to {val.strip()} ({filename}, {lineNum})")

        # output
        elif line.startswith("out "):
            output = line[4:]
            print(evaluate(output))

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
