// Computes max(R0, R1) and stores the result in R2.
@0
D=M
@1
D=D-M
@R0_GREATER
D;JGT
@1
D=M
@STORE
0;JMP
(R0_GREATER)
@0
D=M
(STORE)
@2
M=D