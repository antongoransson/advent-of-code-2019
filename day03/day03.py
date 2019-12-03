from collections import defaultdict

directions_x = {
    'U': -1,
    'D': 1,
    'R': 0,
    'L': 0
}
directions_y = {
    'U': 0,
    'D': 0,
    'R': 1,
    'L': -1
}


def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def solve(wires):
    start = (0, 0)
    grid = defaultdict(lambda: (0, -1))
    intersections = []
    for k, v in wires.items():
        steps = 0
        x, y = 0, 0
        for d, n_steps in v:
            for _ in range(n_steps):
                x += directions_x[d]
                y += directions_y[d]
                curr_cell = grid[x, y]
                if curr_cell[0] and curr_cell[1] != k:
                    intersections.append((x, y, curr_cell[2] + steps))
                else:
                    grid[x, y] = (1, k, steps)
                steps += 1
    intersections = [x for x in intersections if (x[0], x[1]) != start]
    return intersections, start


def solve_part_1(start, intersections):
    intersections.sort(key=lambda x: manhattan_dist(x, start))
    return manhattan_dist(intersections[0], start)


def solve_part_2(intersections):
    intersections.sort(key=lambda x: x[2])
    return intersections[0][2]


def main():
    l = defaultdict()
    wires = {}
    with open('input.txt') as f:
        for i, line in enumerate(f):
            wires[i] = [(x[0], int(x[1:])) for x in line.strip().split(',')]
    intersections, start = solve(wires)
    sol1 = solve_part_1(start, intersections)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(intersections)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
