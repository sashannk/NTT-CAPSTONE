// Box.asm for K = 05
// Draws a 32x20 black box starting at Row 5 (address 16544) while a key is pressed.

(MAIN_LOOP)
    @KBD
    D=M             // Read keyboard state
    @SET_WHITE
    D;JEQ           // If no key pressed (D == 0), set color to white (0)

    @color
    M=-1            // Key pressed: black (-1)
    @DRAW_INIT
    0;JMP

(SET_WHITE)
    @color
    M=0             // No key pressed: white (0)

(DRAW_INIT)
    @16544          // SCREEN (16384) + 32 * 5 (160) = 16544
    D=A
    @addr
    M=D

    @20             // Height = 20 rows
    D=A
    @rows
    M=D

(ROW_LOOP)
    @rows
    D=M
    @MAIN_LOOP
    D;JEQ           // Finished all 20 rows -> check keyboard again

    // Word 0 (pixels 0..15)
    @color
    D=M
    @addr
    A=M
    M=D

    // Word 1 (pixels 16..31 -> total 32 pixels wide)
    @color
    D=M
    @addr
    A=M+1
    M=D

    // Next row is 32 words down
    @32
    D=A
    @addr
    M=D+M

    // Decrement row counter
    @rows
    M=M-1

    @ROW_LOOP
    0;JMP
