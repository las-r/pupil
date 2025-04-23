# Pupil

Pupil *(.pil)* is an interpreted programming language made for making stuff and other stuff. It has a focus on graphics using SDL.

Things that are underlined are unfinished.

## Syntax

### Operators

**Arithmetic**  
`{val} + {val}`: Add, Concatenate  
`{val} - {val}`: Subtract  
`{val} * {val}`: Multiply  
`{val} / {val}`: Divide  
`{val} ^ {val}`: Exponent

**Boolean**  
`{val} && {val}`: AND  
`{val} || {val}`: OR  
`{val} :: {val}`: XOR  
`! {val}`: NOT  
`true`: True  
`false`: False

**Comparison**  
`{val} == {val}`: Equal to  
`{val} > {val}`: Greater than  
`{val} >= {val}`: Greater than or equal to  
`{val} < {val}`: Less than  
`{val} <= {val}`: Less than or equal to

### Data types

`int`: Integer, `10`  
`flt`: Floating point decimal, `3.141`  
`str`: String, `"string"`  
`bln`: Boolean, `true`  
`arr`: Array, `[int 1, int 2, str "three", flt 4.5, bln true]`

### Comments

Explain code  
`~~ this is a comment or something idk`

### Variables

Store data  
`str greeting = "Hello, world!"`

### If

If condition do action  
`if value == 69`  
	`out "hehehe"`  
`elseif otherValue == value`  
	`out "whoa they're equal"`  
`else`  
	`out "sad"`  
`end`

### Jump (Relative)

Jump amount of lines  
`jump 7`

### Jump (Absolute)

Jump to line  
`jumpto 3`

### While

While condition do action  
`while running == true`  
	`out "im running"`  
`end`

### Output

Prints in console  
`out "Hi!"`

### Input

User input in console  
`inp int number "enter a number"`

### Function

Stores code and context  
`func add(x, y)`  
	`ret x + y`  
`end`  
`add(1, 2) ~~ returns 3`

### Import

Get functions from another file  
`get more-math.pil`

### Wait

Pause execution  
`wait 500 ~~ waits 0.5 secs`

### Skip

Does nothing  
`skip`

### Stop

Finishes the program  
`stop`

## In-built functions

- *Mathematical*: msqrt(x), mfloor(x), mceil(x), mfact(x), msin(x), mcos(x), mtan(x), masin(x), macos(x), matan(x), mcot(x), msec(x), mcsc(x)  
- *Random*: rint(min, max), rpick(array)  
- *Time*: unix()  
- Array: sort(array)

## Examples

### Simple Calculator

`~~ simple calculator`

`~~ user inputs numbers`  
`inp flt x "Enter your first number (x): "`  
`inp flt y "Enter your second number (y): "`

`~~ calculate and output answers`  
`out "x + y = " + (x + y)`  
`out "x - y = " + (x - y)`  
`out "x * y = " + (x * y)`  
`out "x / y = " + (x / y)`  
`out "x ^ y = " + (x ^ y)`  
`out "sqrt x = " + msqrt(x)`  
`out "sqrt y = " + msqrt(y)`

### To-Do List Maker

`~~ to-do list creator`

`~~ list`  
`arr tdlist = []`

`~~ main loop`  
`while true`  
	`out "Actions"`  
	`out "0: View"`  
`out "1: Add item"`  
`out "2: Remove item"`  
	`inp int choice "Enter your choice from those above: "`

	`if choice == 0`  
		`~~ loop through list alphabetically`  
		`index = 0`  
		`while index < tdlist.len`  
			`out "- " + sort(tdlist)[index]`  
			`index = index + 1`  
		`end`

	`elseif choice == 1`  
		`~~ item to add to list`  
		`inp str item "Enter what you would like to add: "`

		`~~ append item to list`  
		`tdlist.add(item)`

	`elseif choice == 2`  
		`~~ item to remove from list`  
		`inp str item "Enter what you would like to remove: "`  
		  
		`if tdlist.has(item)`  
			`tdlist.rem(item)`  
		`else:`  
			`out "This isn’t in the list."`  
		`end`  
	`end`  
`end`

### String E Checker

`~~ check if strings have the letter e in them`

`~~ check function`  
`func check(string)`  
	`~~ loop through string and check if the index is e or E`  
	`index = 0`  
	`while index < string.len`  
		`if string[index] == "e" || string[index] == "E"`  
			`ret true`  
		`end`  
`index = index + 1`  
	`end`

	`~~ no e`  
	`ret false`  
`end`

`~~ user inputs string`  
`inp str string "Enter anything: "`

`~~ output`  
`if check(string)`  
	`out "THE STRING HAS AN E OH MY GOD"`  
`else`  
	`out "THE STRING DOESN’T HAVE AN E OH MY GOD"`  
`end`
