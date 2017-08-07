# superbrain

Superbrain is a brainf*** interpreter with optional extras.

Brainf*** uses eight characters to write incredibly simple instructions. It is Turing-complete.

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
