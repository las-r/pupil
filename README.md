# Pupil
Pupil (*.pil*) is an interpreted programming language made for making stuff and other stuff. It has a focus on graphics using SDL.

Things that are underlined are unfinished.

## Syntax

### Data types
`int`: Integer, `10`\
`flt`: Floating point decimal, `3.141`\
`str`: String, `"string"`\
`bln`: Boolean, `true`\
`arr`: Array, `[1, 2, "three", 4.5, true]`

### Comments
Explain code
```
~~ this is a comment or something idk
```

### Variables
Store data
```
var greeting = "Hello, world!"
```

### If
If condition do action
```
if value == 69  
    out "hehehe"  
elseif otherValue == value  
    out "whoa they're equal"  
else  
    out "sad"  
end
```

### Jump (Relative)
Jump amount of lines  
```
jump 7
```

### Jump (Absolute)
Jump to line
```
jumpto 3
```

### While
While condition do action  
```
while running == true
    out "im running"
end
```

### Output
Prints in console  
```
out "Hi!"
```

### Input
User input in console
```
inp num int "enter a number"
```

### Function
Stores code and context  
```
func add (x y)
    ret x + y
end
.add (1 2)  ~~ returns 3
```


### Import
Get functions from another file
```
get more-math.pil
```

### Wait
Pause execution  
```
wait 500 ~~ waits 0.5 secs
```

### Skip
Does nothing  
```
skip
```

### Stop
Finishes the program  
```
stop
```

### In-built functions
- **Mathematical**: `.msqrt (x)`, `.mfloor (x)`, `.mceil (x)`, `.msin (x)`, `.mcos (x)`, `.mtan (x)`, `.mround (x, d)`
- **Random**: `.rint (min, max)`
- **Time**: `.tunix ()`
