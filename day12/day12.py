from collections import defaultdict
from itertools import combinations
import regex as re
import math

AXES = 'xyz'


def calc_velocity(p1, p2, v1, v2):
    for axis in AXES:
        if p1[axis] < p2[axis]:
            v1[axis] += 1
            v2[axis] -= 1
        elif p1[axis] > p2[axis]:
            v2[axis] += 1
            v1[axis] -= 1


def sim_motion(moons):
    for m1, m2 in combinations(moons.values(), 2):
        calc_velocity(m1['p'], m2['p'], m1['v'], m2['v'])
    for m in moons.values():
        for axis in AXES:
            m['p'][axis] += m['v'][axis]


def solve_part_1(moons):
    for _ in range(1000):
        sim_motion(moons)
    t = 0
    for m in moons.values():
        pot_e = sum(abs(m['p'][axis]) for axis in AXES)
        kin_e = sum(abs(m['v'][axis]) for axis in AXES)
        t += pot_e * kin_e
    return t


def flatten_state(moon):
    return [str(moon['p'][axis]) + str(moon['v'][axis]) for axis in AXES]


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def solve_part_2(moons):
    periods = {axis: -1 for axis in AXES}
    s = list(zip(*[(flatten_state(m)) for m in moons.values()]))
    start_states = {axis: s[k] for k, axis in enumerate(AXES)}
    i = 0
    while True:
        sim_motion(moons)
        i += 1
        s = list(zip(*[(flatten_state(m)) for m in moons.values()]))
        for k, axis in enumerate(AXES):
            if periods[axis] == -1:
                if s[k] == start_states[axis]:
                    periods[axis] = i
        if all([periods[axis] != -1 for axis in AXES]):
            break
    return lcm(lcm(periods['x'], periods['y']), periods['z'])


def main():
    moons = {}
    with open('input.txt') as f:
        for i, l in enumerate(f):
            x, y, z = map(int, re.findall(r'-?\d+', l))
            moons[i] = {'p': {'x': x, 'y': y, 'z': z},
                        'v': {'x': 0, 'y': 0, 'z': 0}}
    sol1 = solve_part_1(dict(moons))
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(dict(moons))
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
