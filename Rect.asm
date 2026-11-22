// Draws a rectangle of width 16 pixels and height RAM[0] at the top-left of the screen.
@0
D=M
@n
M=D
@INFINITE_LOOP
D;JLE

@SCREEN
D=A
@addr
M=D

@0
D=M
@i
M=D

(LOOP)
    @addr
    A=M
    M=-1

    @32
    D=A
    @addr
    M=D+M

    @i
    MD=M-1
    @LOOP
    D;JGT

(INFINITE_LOOP)
    @INFINITE_LOOP
    0;JMP