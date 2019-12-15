from collections import defaultdict
POS_MODE = 0
IMM_MODE = 1
REL_MODE = 2


class IntcodeComputer:
    def __init__(self, instructions, get_input):
        self.ip = 0
        self.rel_base = 0
        self.memory = defaultdict(
            int, {k: v for k, v in enumerate(instructions)})
        self.get_input = get_input
        self.done = False
        self.op_codes = {
            1: self.addr,
            2: self.mulr,
            3: self.write,
            4: self.output,
            5: self.jmpift,
            6: self.jmpiff,
            7: self.less,
            8: self.eq,
            9: self.adj_rel_base
        }

    def set_val(self, ip , val):
        self.memory [ip] = val

    def run(self):
        instruction = self.memory[self.ip]
        while instruction != 99:
            params = str(instruction)[:-2].zfill(3)
            op = int(str(instruction)[-2:])
            p_modes = list(map(int, params))[::-1]
            out = self.op_codes[op](p_modes)
            if op == 4:
                return out
            instruction = self.memory[self.ip]
        self.done = True

    def get_val(self, ip, p_mode):
        r = self.memory[ip]
        if p_mode == POS_MODE:
            r = self.memory[r]
        elif p_mode == REL_MODE:
            r = self.memory[self.rel_base + r]
        return r

    def addr(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        b = self.get_val(self.ip + 2, p_modes[1])
        c = self.memory[self.ip + 3]
        if p_modes[2] == REL_MODE:
            c = self.rel_base + c
        self.memory[c] = a + b
        self.ip += 4

    def mulr(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        b = self.get_val(self.ip + 2, p_modes[1])
        c = self.memory[self.ip + 3]
        if p_modes[2] == REL_MODE:
            c = self.rel_base + c
        self.memory[c] = a * b
        self.ip += 4

    def write(self, p_modes):
        val = self.get_input()
        a = self.memory[self.ip + 1]
        if p_modes[0] == REL_MODE:
            a = self.rel_base + a
        self.memory[a] = val
        self.ip += 2

    def output(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        self.ip += 2
        return a

    def jmpift(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        b = self.get_val(self.ip + 2, p_modes[1])
        self.ip = self.ip + 3 if a == 0 else b

    def jmpiff(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        b = self.get_val(self.ip + 2, p_modes[1])
        self.ip = self.ip + 3 if a != 0 else b

    def less(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        b = self.get_val(self.ip + 2, p_modes[1])
        c = self.memory[self.ip + 3]
        if p_modes[2] == REL_MODE:
            c = self.rel_base + c
        self.memory[c] = int(a < b)
        self.ip += 4

    def eq(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        b = self.get_val(self.ip + 2, p_modes[1])
        c = self.memory[self.ip + 3]
        if p_modes[2] == REL_MODE:
            c = self.rel_base + c
        self.memory[c] = int(a == b)
        self.ip += 4

    def adj_rel_base(self, p_modes):
        a = self.get_val(self.ip + 1, p_modes[0])
        self.rel_base += a
        self.ip += 2
