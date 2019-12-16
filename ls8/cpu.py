"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 6
        self.reg = [0] * 8

    def ram_read(self, pc):
        print(self.ram[pc])

    def ram_write(self, prog):
        self.ram.append(prog)

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

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
        running = True
        while running:
            if self.ram[self.pc] == HLT:
                running = False
            if self.ram[self.pc] == LDI:
                position = self.ram[self.pc + 1]
                print(position, "POSITION")
                self.reg[position] = self.ram[self.pc + 2]
            if self.ram[self.pc] == PRN:
                # print("Hi, here is self.pc+1", self.pc +
                #       1, "And the reg", self.reg)
                position = self.ram[self.pc + 1]
                print(self.reg[position])
            self.pc += 1
        pass
