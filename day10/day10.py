from collections import defaultdict
from itertools import combinations
from math import atan2, degrees, sqrt


def get_angle(p1, p2):
    y1, x1 = p1
    y2, x2 = p2
    d = degrees(atan2(y1 - y2, x1 - x2)) - 90
    if d < 0:
        d += 360
    return d


def get_all_angels(asteroids):
    angels = defaultdict(lambda: defaultdict(list))
    for a1, a2 in combinations(asteroids, 2):
        angels[a1][get_angle(a1, a2)].append(a2)
        angels[a2][get_angle(a2, a1)].append(a1)
    return angels


def dist(p1, p2):
    y1, x1 = p1
    y2, x2 = p2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def solve_part_1(angels):
    return max([len(v.keys()) for v in angels.values()])


def solve_part_2(angels):
    p = max(angels, key=lambda x: len(angels[x].keys()))
    p_angels = sorted(angels[p].keys())
    y, x = [sorted(angels[p][p_angels[i % len(p_angels)]],
                   key=lambda x: dist(p, x), reverse=True).pop() for i in range(200)][-1]
    return y + x * 100


def main():
    with open('input.txt') as f:
        asteroids = [(y, x) for y, l in enumerate(f)
                     for x, c in enumerate(l) if c == "#"]
        angels = get_all_angels(asteroids)
        sol1 = solve_part_1(angels)
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(angels)
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
