 # superbrain

Superbrain is a brainf*** interpreter with optional extras.

Brainf*** uses eight characters to write incredibly simple instructions. It is Turing-complete, meaning it can theoretically complete any task expressible by a computer (given unlimited memory.) It is also referred to as a 'Turing tarpit', or a language which fulfills Turing-completeness while being as esoteric, minimalist, and confusing as possible.

Information is stored on a 'tape' which is either finite (usually 30000 cells) or infinite. The tape consists of cells with indices starting at 0. Each cell contains eight bits of information. A pointer which starts at cell 0 is pushed back and forth along the tape, reading and writing values. A simple loop block can be used to repeat instructions based on a condition.

| Instruction | Action |
| :---: | --- |
| `>` | Pushes the pointer to the right. |
| `<` | Pushes the pointer to the left. |
| `+` | Increments the cell at the pointer by 1. |
| `-` | Decrements the cell at the pointer by 1. |
| `,` | Accepts one byte of user input. |
| `.` | Writes the value of the cell to standard output. |
| `[` | Opens a loop if the value at the pointer is non-zero. |
| `]` | Continues a loop if the value at the pointer is non-zero; otherwise, breaks out of the loop. |

The augmented version supplied here contains eight extra characters, including the three added by pbrain, a procedural variant.

| Instruction | Action |
| :---: | --- |
| `(` | Starts recording a procedure linked to the active cell. The procedure doesn't execute yet. |
| `)` | Ends recording a procedure linked to the active cell. |
| `:` | Runs the procedure linked to the active cell. If none is specified, BF will crash. |
| `*` | Left-shifts the active cell once. |
| `/` | Right-shifts the active cell once. |
| `~` | Inverts the value of the active cell. (NOT logic operation) |
| `&` | Takes the value of the cells immediately to the left and right, ANDs them, and puts the value in the active cell. |
| `\|` | Takes the value of the cells immediately to the left and right, ORs them, and puts the value in the active cell. |

## How to Use

Write a BF file in your friendly neighborhood text editor, open a shell, and use bfi.py as a command with the filename and path as the only argument. You will need Python 3.5 or later installed.

`bfi.py hell.bf`

This has only been tested on Windows.

## Why is this one better than the eight thousand other BF interpreters?

It's not. Sorry. It works and stuff (I think), so there.

## Removed Features

*Removed features are features that aren't considered ~valuable~ confusing enough to be standard in the interpreter. They still exist and will be accessible via the `--legacy:[version]` command.*

- Remove AND and OR operations from standard set (too intuitive); replace with ~multi-dimensional operators~ pointer lock and the debug instruction which is standard in most implementations.

| Replaced Instruction | New Instruction | Action |
| :---: | :---: | --- |
| `&` | `!` | Freezes the pointer. All requests to move it will be tallied. When this symbol is used again, the pointer will jump in one step. |
| `\|` | `#` | Debug symbol. Will immediately jump to a step-through mode where all states can be viewed. |
