
"""CPU functionality."""

import sys

# declare opcodes for clarity

LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
JMP = 0b01010100
FL = 0b00000000
CMP = 0b10100111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.usage = 0
        self.sp = 7

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        return self.ram[MAR]

    def load(self, file):
        """Load a program into memory."""
        file = file
        address = 0

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

        print(f"self.ram : {self.ram}")

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
        print(self.ram, "SELF.RAM")
        while running:
            ir = self.ram_read(self.pc)
            position_1 = self.ram_read(self.pc + 1)
            position_2 = self.ram_read(self.pc + 2)

            if ir == HLT:
                print("*****HLT*****")
                running = False

            if ir == LDI:
                print("*****LDI*****")
                self.reg[position_1] = position_2
                self.pc += 3

            elif ir == PRN:
                print("*****PRN*****")
                print(self.reg[position_1])
                self.pc += 2

            elif ir == MUL:
                print("*****MUL*****")
                print(self.reg[position_1]*self.reg[position_2])
                self.pc += 3

            elif ir == PUSH:
                print("*****PUSH*****")
                self.reg[self.sp] -= 1
                value = self.reg[position_1]
                self.ram[self.reg[self.sp]] = value
                self.pc += 2

            elif ir == POP:
                print("*****POP*****")
                value = self.ram[self.reg[self.sp]]
                self.reg[position_1] = value
                self.reg[self.sp] += 1
                self.pc += 2

            elif ir == CALL:
                print("*****CALL*****")
                return_address = self.pc + 2
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = return_address

                reg_num = self.ram[self.pc + 1]
                sub_address = self.reg[reg_num]
                self.pc = sub_address

            elif ir == RET:
                print("*****RET*****")
                return_address = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
                self.pc = return_address

            elif ir == ADD:
                print("*****ADD*****")
                value = self.reg[position_1] + self.reg[position_2]
                self.reg[position_1] = value
                self.pc += 3

            elif ir == JMP:
                print("*****JMP*****")
                jump = self.reg[self.ram[position_1]]
                self.pc = jump

            elif ir == CMP:
                print("*****CMP*****")
                if self.register[position_1] < self.register[position_2]:
                    FL = 0b00000100
                if self.register[position_1] > self.register[position_2]:
                    FL = 0b00000010
                if self.register[position_1] == self.register[position_2]:
                    FL = 0b00000001

            else:
                print(f"Unknown instruction in RAM at: {self.pc}")
