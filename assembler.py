import sys
import os

COMP_TABLE = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "M":   "1110000",
    "!D":  "0001101", "!A":  "0110001", "!M":  "1110001",
    "-D":  "0001111", "-A":  "0110011", "-M":  "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010111",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}

DEST_TABLE = {
    "":    "000", "M":   "001", "D":   "010", "MD":  "011",
    "A":   "100", "AM":  "101", "AD":  "110", "AMD": "111",
}

JUMP_TABLE = {
    "":    "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


def init_symbols():
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576,
    }
    for i in range(16):
        symbols[f"R{i}"] = i
    return symbols


def clean_line(raw_line):
    return raw_line.split("//")[0].strip()


def assemble(input_path):
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    symbols = init_symbols()
    declared_labels = set()
    cleaned_instructions = []
    rom_address = 0

    # Pass 1: Record labels and warn on duplicate labels (K = 05 -> K mod 3 == 2)
    for line_num, raw in enumerate(raw_lines, start=1):
        line = clean_line(raw)
        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            if label in declared_labels:
                print(f"Warning (Line {line_num}): Duplicate label '({label})' found.")
            else:
                declared_labels.add(label)
                symbols[label] = rom_address
        else:
            cleaned_instructions.append(line)
            rom_address += 1

    # Pass 2: Translate instructions to 16-bit binary
    next_ram_addr = 16
    machine_code = []

    for inst in cleaned_instructions:
        if inst.startswith("@"):
            symbol = inst[1:]
            if symbol.isdigit():
                addr = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram_addr
                    next_ram_addr += 1
                addr = symbols[symbol]
            machine_code.append(f"0{addr:015b}")
        else:
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            c_bits = COMP_TABLE[comp.strip()]
            d_bits = DEST_TABLE[dest.strip()]
            j_bits = JUMP_TABLE[jump.strip()]
            machine_code.append(f"111{c_bits}{d_bits}{j_bits}")

    output_path = os.path.splitext(input_path)[0] + ".hack"
    with open(output_path, "w", encoding="utf-8") as f:
        for code in machine_code:
            f.write(code + "\n")


    print(f"Wrote {len(machine_code)} instructions to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <Program.asm>")
        sys.exit(1)
    assemble(sys.argv[1])
