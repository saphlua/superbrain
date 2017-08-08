#!/usr/bin/python3

import sys
import os
from clint.textui import colored, puts
import re
import math

version = "1.0"

helpstr = """This is my take on a brainf--- interpreter. It can use all eleven symbols
of pbrain (the procedural equivalent) as well as five symbols unique to this parser.
The eight extra symbols are called 'modern' or, more accurately, 'cheating'. The eight
primary symbols are called 'vanilla'.

--- COMMANDS ---

NOT IMPLEMENTED: These are the commands you can use with the interpreter program.

CURRENT: Use --help for help. Specify a filename to run it. That is all.

superbrain.py [--args] [filename|]

--help
	prints this messsage.
--repl
	runs a read-eval-print loop.
--check
	checks the file to see if it is valid BF.
--pack
	packs the file as tightly as possible (converts instruction pairs to bytes).
	If the number of instructions is uneven, the last instruction will be a `>`.
	The program can still be interpreted using this parser.
--unpack
	unpacks a byte-compressed file into instructions. Note that a packed .b file
	has a specific byte header and it will reject the file if you decide to choose,
	say, a GIF89a instead.
--clean
	optimizes the file. Uses the modern operators.
--clean-nm
	optimizes the file without modern operators.
--monkey
	runs the file in OOK mode. Only the vanilla symbols are permitted.
--tern
	runs the file in ternary mode. Only the vanilla symbols are permitted.
--vanilla
	runs the file in vanilla mode. Tape is 30000 cells long and only the vanilla
	symbols are permitted.
--step
	runs the file in debug mode. Step through the code instruction by instruction,
	jump through a loop, and view or modify values at various locations.
	You can also inject extra code into segments of the file and view a help
	index of snippets with various purposes.

--- ERRORS ---

The interpreter provides error messages on a crash. They are as helpful as possible,
which isn't much. There's only so much I can do.

They are also red. You can't miss 'em.

--- EXAMPLES ---

The included examples folder contains lots of snippets that accomplish various tasks.

--- CODE SYNTAX ---

SYMBOL	DESCRIPTION
>	increments the pointer location.
<	decrements the pointer location.
+	increments the value at the pointer.
-	decrements the value at the pointer.
.	output the value at the pointer.
,	get user input and assign it to the pointer.
[	opens a loop block if the value at the pointer is non-zero.
]	if the value at the pointer is non-zero, jump back
	to the instruction after the matching bracket.
(	opens a procedure with a name corresponding to
	the pointer's location index.
)	closes a procedure with a name corresponding to
	the pointer's location index. Jumps back to code.
:	runs the procedure corresponding to the location index.
	If the procedure is undefined, the program will crash.
&   Does an AND operation on the byte to the left and the byte to the right.
    The result is stored in the pointer's location.
|   Does an OR operation on the byte to the left and the byte to the right.
    The result is stored in the pointer's location.
~	flips the byte at the location.
*	left-shift the byte once.
/	right-shift the byte once.

--- TRANSLATION TABLE ---

For using the parser with Ook, Hex, Ternary, and Quad.

Quad is my own variant using the values 0, 1, 2, 3.

Values don't always correspond to the order in the table: I'm using the
standard order for those languages.

SYMBOL      HEX     OOK         TERNARY QUAD
>           0       Ook. Ook?   01      00
<           1       Ook? Ook.   00      01
+           2       Ook. Ook!   11      02
-           3       Ook! Ook!   10      03
.           4       Ook! Ook.   20      10
,           5       Ook. Ook!   21      11
[           6       Ook! Ook?   02      12
]           7       Ook? Ook!   12      13
(           8       --          --      20
)           9       --          --      21
:           A       --          --      22
&           B       --          --      23
|           C       --          --      30
~           D       --          --      31
*           E       --          --      32
/           F       --          --      33

--- COMING SOON ---

1. Tables and configurations. Define your own BF derivative and its rules.
2. Interpreter for Whitespace.
3. Interpreter for Brainbool.
4. 2D and 3D variants of BF.

--- COMING VERY SOON ---

1. Add interpreting for variants and implementation of all commands.
2. Example codes."""

def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch
    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch

getch = _find_getch()

def readFile(filename):
    f = open(filename, 'rt')
    data = f.read()
    f.close()
    return data

def findHeaders(data):
    return {}
    
def clean(data):
    # strip whitespace
    data = ''.join(data.split())
    # TODO: replace comments but preserve original code for debugging, add line markers for debugging
    # data = re.sub(r'["](.*)*["]', '', data)
    return data

def bfException(msg, codesnip):
    print()
    print(colored.red(msg), end="")
    print()
    print(codesnip)
    input()
    sys.exit(1)

def execute(data, options={}):
    # Probably not the most efficient code, but then again, how efficient can this be, really?
    code = clean(data)
    tapeLength = math.inf
    tape = [0]
    ptr = 0
    codeptr = 0
    depth = 0
    catchDepth = 0
    procedureStack = []
    procedure = {}
    errmsg = 'error @ [command `{0}`, code-point {1}] : {2}'
    while codeptr < len(code):
        if code[codeptr] == '>':
            ptr += 1
            if not ptr < tapeLength:
                bfException(errmsg.format(code[codeptr], codeptr, 'The pointer exceeded the boundaries of the tape.'), code[codeptr-50:codeptr] + colored.green(code[codeptr]) + code[codeptr+1:codeptr+50])
            try:
                tape[ptr]
            except IndexError:
                tape.append(0)
        elif code[codeptr] == '<':
            ptr -= 1
            if not ptr >= 0:
                bfException(errmsg.format(code[codeptr], codeptr, 'The pointer exceeded the boundaries of the tape.'), code[codeptr-50:codeptr] + colored.green(code[codeptr]) + code[codeptr+1:codeptr+50])
        elif code[codeptr] == '+':
            tape[ptr] += 1
            tape[ptr] %= 256
        elif code[codeptr] == '-':
            tape[ptr] -= 1
            tape[ptr] %= 256
        elif code[codeptr] == '.':
            if tape[ptr] in (10, 13):
                # find line break characters, please!
                print()
                print(chr(tape[ptr]), end="")
            print(chr(tape[ptr]), end="")
        elif code[codeptr] == ',':
            tape[ptr] = ord(getch())
        elif code[codeptr] == '[':
            if tape[ptr] != 0:
                # increase the depth and continue
                depth += 1
            else:
                # else skip the loop
                cdepth = 1
                # Preserve this in case we get a bfException.
                preserve_codeptr = codeptr
                while cdepth > 0:
                    # run forward until we exit the loop.
                    codeptr += 1
                    try:
                        code[codeptr]
                    except IndexError:
                        bfException(errmsg.format(code[codeptr], codeptr, 'The opening loop bracket at ' + str(preserve_codeptr) + ' does not have a sibling.'), code[codeptr-50:codeptr] + colored.green(code[codeptr]) + code[codeptr+1:codeptr+50])
                    if not code[codeptr] in ('[', ']'):
                        continue
                    elif code[codeptr] == '[':
                        cdepth += 1
                    elif code[codeptr] == ']':
                        cdepth -= 1
        elif code[codeptr] == ']':
            if depth == 0:
                bfException(errmsg.format(code[codeptr], codeptr, 'The closing loop bracket at ' + str(codeptr) + ' does not have a sibling.'), code[codeptr-50:codeptr] + colored.green(code[codeptr]) + code[codeptr+1:codeptr+50])
            else:
                if tape[ptr] != 0:
                    backdepth = 1
                    # run backward to just after the loop opening.
                    while backdepth > 0:
                        codeptr -= 1
                        # The exception has already been tested, we won't do that again. ^
                        if not code[codeptr] in ('[', ']'):
                            continue
                        elif code[codeptr] == '[':
                            backdepth -= 1
                        elif code[codeptr] == ']':
                            backdepth += 1
        elif code[codeptr] == '~':
            tape[ptr] = (tape[ptr] + 128) % 256
        elif code[codeptr] == '*':
            tape[ptr] = (tape[ptr] << 1) % 256
        elif code[codeptr] == '/':
            tape[ptr] = (tape[ptr] >> 1) % 256
        elif code[codeptr] == '(':
            pdepth = 1
            pcodeptr = codeptr
            procedure[ptr] = ''
            while pdepth > 0:
                pcodeptr += 1
                if code[pcodeptr] == '(':
                    pdepth += 1
                elif code[pcodeptr] == ')':
                    pdepth -= 1
                    if pdepth == 0:
                        continue
                procedure[ptr] += code[pcodeptr]
        elif code[codeptr] == ')':
            pass
        elif code[codeptr] == ':':
            # How do procedures work? They're injected directly into the code, replacing the symbol.
            try:
                procedure[ptr]
            except KeyError:
                bfException(errmsg.format(code[codeptr], codeptr, 'Attempted to call an undefined procedure at index ' + str(ptr) + '.'), code[codeptr-50:codeptr] + colored.green(code[codeptr]) + code[codeptr+1:codeptr+50])
            # Replace the symbol `:` with the code; an insert() for strings.
            code = code[:codeptr] + procedure[ptr] + code[codeptr+1:]
            # Problem: the first instruction of the procedure will be skipped over because the codeptr increments
            # at the end of the loop. The codeptr -= 1 fixes that, making sure every instruction runs.
            codeptr -= 1
        elif code[codeptr] == '&':
            try:
                tape[ptr-1]
                tape[ptr+1]
            except IndexError:
                bfException(errmsg.format(code[codeptr], codeptr, 'The operation exceeded the boundaries of the tape.'), code[codeptr-50:codeptr] + colored.green(code[codeptr]) + code[codeptr+1:codeptr+50])
            tape[ptr] = tape[ptr+1] & tape[ptr-1]
        elif code[codeptr] == '|':
            try:
                tape[ptr-1]
                tape[ptr+1]
            except IndexError:
                bfException(errmsg.format(code[codeptr], codeptr, 'The operation exceeded the boundaries of the tape.'), code[codeptr-50:codeptr] + colored.green(code[codeptr]) + code[codeptr+1:codeptr+50])
            tape[ptr] = tape[ptr+1] | tape[ptr-1]
        codeptr += 1

if __name__ == '__main__':
    if len(sys.argv) is 2 and sys.argv[1] == '--help':
        print(helpstr)
    elif len(sys.argv) is 2 and os.path.isfile(sys.argv[1]):
        data = readFile(sys.argv[1])
        execute(data)
