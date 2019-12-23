import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intcode.IntcodeComputer import IntcodeComputer
from collections import defaultdict

def solve_part_1(instructions):
    packages = {i: [i] for i in range(50)}

    def get_input(i):
        if packages[i]:
            return packages[i].pop(0)
        return -1
    network = []
    for i in range(50):
       network.append(IntcodeComputer(instructions, lambda: get_input(i)))
    i = 0
    while True:
       program = network[i]
       while not program.done:
            address = program.run()
            if address == -1:
                i = (i + 1) % 50      
                break   
            x = program.run()
            y = program.run()
            if address == 255:
                return y
            packages[address] += [x, y]

def solve_part_2(instructions):
   packages = {i: [i] for i in range(50)}
   def get_input(i):
        if packages[i]:
            return packages[i].pop(0)
        return -1
   network = []
   for i in range(50):
       network.append(IntcodeComputer(instructions, lambda: get_input(i)))
   i = 0
   seen = set()
   while True:
       program = network[i]
       while not program.done:
            address = program.run()
            if address == -1:
                i = (i + 1) % 50      
                break   
            x = program.run()
            y = program.run()
            if address == 255:
                if all([len(p) == 0 for p in packages.values()]):
                    packages[0] += [x, y]
                    if y in seen:
                        return y
                    seen.add(y)
            else:
                packages[address] += [x, y]


def main():
    with open('input.txt') as f:
        data = list(map(int, f.read().strip().split(",")))
    sol1 =  solve_part_1(data)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
