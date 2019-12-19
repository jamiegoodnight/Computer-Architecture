
"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.usage = 0
        self.sp = 7

    def ram_read(self, pc):
        print(self.ram[pc])

    def ram_write(self, prog):
        self.ram.append(prog)

    def load(self, file):
        """Load a program into memory."""
        file = file
        address = 0

        # For now, we've just hardcoded a program:

        with open(file) as f:
            for line in f:
                n = line.split("#")
                n[0] = n[0].strip()
                if n[0] == "":
                    continue
                val = int(n[0], 2)
                self.ram[address] = val
                address += 1
                self.usage += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.reg[self.sp] = 244
        cur_pos = self.ram[self.pc]
        running = True
        # position_1 = self.ram[self.pc + 1]
        # position_2 = self.ram[self.pc + 2]
        print(self.ram, "SELF.RAM")
        while running:
            # print(self.usage, "USAGE", self.pc, "PC")
            if self.ram[self.pc] == HLT:
                if self.usage-1 == self.pc:
                    print("*****HLT*****")
                    running = False

            elif self.ram[self.pc] == LDI:
                position_1 = self.ram[self.pc + 1]
                position_2 = self.ram[self.pc + 2]
                print("*****LDI*****")
                self.reg[position_1] = position_2
                self.pc += 3

            elif self.ram[self.pc] == PRN:
                print("*****PRN*****")
                print(self.reg[position_1])
                self.pc += 2

            elif self.ram[self.pc] == MUL:
                position_1 = self.ram[self.pc + 1]
                position_2 = self.ram[self.pc + 2]
                print("*****MUL*****")
                print(self.reg[position_1]*self.reg[position_2])
                self.pc += 3

            elif self.ram[self.pc] == POP:
                value = self.ram[self.reg[self.sp]]
                self.reg[self.ram[self.pc + 1]] = value
                self.reg[self.sp] += 1

                self.pc += 2

            elif self.ram[self.pc] == PUSH:
                self.reg[self.sp] -= 1
                value = self.reg[self.ram[self.pc + 1]]
                self.ram[self.reg[self.sp]] = value

                self.pc += 2

            else:
                print(f"Unknown instruction in RAM at: {self.pc}")

            # self.pc += 1
        pass
