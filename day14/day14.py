from collections import defaultdict
import math


def calc_ore(c, reactions, acc, waste, res):
    r = reactions[c[1]]
    c_n = c[0]
    r_n = r['amount']
    inputs = r['inputs']
    m = math.ceil((c_n * acc - waste[c[1]]) / r_n)
    waste[c[1]] = m * r_n - (c_n * acc - waste[c[1]])
    if inputs[0][1] == 'ORE':
        res.append(m * inputs[0][0])
        return
    [calc_ore(x, reactions, m, waste, res) for x in inputs]


def solve_part_1(reactions, fuel_amount):
    tot = defaultdict(int)
    waste = defaultdict(int)
    res = []
    [calc_ore(c, reactions, fuel_amount, waste, res)
     for c in reactions['FUEL']['inputs']]
    return sum(res)


def solve_part_2(reactions):
    low = 0
    high = 10000000
    res = {}
    while True:
        m = (high + low) // 2
        t = solve_part_1(reactions, fuel_amount=m)
        res[m] = t
        if t > 1000000000000:
            high = m
        else:
            low = m
            if m + 1 in res and res[m + 1] > 1000000000000:
                return m


def main():
    with open('input.txt') as f:
        reactions = {}
        for line in f:
            i, o = line.split("=>")
            i = i.split(",")
            o = o.strip().split(" ")
            reactions[o[1]] = {'amount': int(o[0]), 'inputs': []}
            for reaction in i:
                r = reaction.strip().split(" ")
                reactions[o[1]]['inputs'].append([int(r[0]), r[1]])
    sol1 = solve_part_1(reactions, 1)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(reactions)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
