from collections import defaultdict
import regex as re


def solve_part_1():
   pass


def solve_part_2():
   pass


def main():
    with open('input.txt') as f:
        in_data = list(map(int, re.findall(r'\d+', f)))
    sol1 =  solve_part_1()
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2()
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
