import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import defaultdict, deque
from intcode.IntcodeComputer import IntcodeComputer


def get_neighbours(grid, pos):
    adjacent = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
    return[p for p in adjacent if grid[p[0], p[1]] != 0]


def bfs(grid, start, end=-1):
    q = deque([[start]])
    explored = set()
    while q:
        path = q.popleft()
        node = path[-1]
        if node in explored:
            continue
        for neighbour in get_neighbours(grid, node):
            x, y = neighbour
            if neighbour in explored:
                continue
            new_path = list(path)
            new_path.append(neighbour)
            q.append(new_path)
            x, y = neighbour
            if grid[x, y] == end or (x, y) == end:
                return new_path[1:]
        explored.add(node)
    return None


dx = {
    1: -1,
    2: 1,
    3: 0,
    4: 0
}
dy = {
    1: 0,
    2: 0,
    3: -1,
    4: 1
}


def get_next_move(grid, x, y, path):
    if path:
        next_tile = path.pop(0)
    else:
        path = bfs(grid, (x, y))
        if path == None:
            return -1, []
        next_tile = path.pop(0)
    if x < next_tile[0]:
        d = 2
    elif x > next_tile[0]:
        d = 1
    elif y > next_tile[1]:
        d = 3
    elif y < next_tile[1]:
        d = 4
    return d, path


def run_program(instructions, grid):
    start, goal = (0, 0), (0, 0)
    x, y = start
    d = 1
    path = []

    def get_input():
        return d
    program = IntcodeComputer(instructions, get_input)
    while not program.done:
        out = program.run()
        grid[x + dx[d], y + dy[d]] = out
        if out == 0:
            d, path = get_next_move(grid, x, y, path, )
            if d == -1:
                return len(bfs(grid, start, goal)), goal
        else:
            x += dx[d]
            y += dy[d]
            d, path = get_next_move(grid, x, y, path)
        if out == 2:
            goal = (x, y)
    return


def solve_part_1(instructions, grid):
    n_steps, goal = run_program(instructions, grid)
    return n_steps, goal


def solve_part_2(grid, goal):
    t = 0
    q = [goal]
    seen = set()
    while True:
        next_t = []
        while q:
            node = q.pop()
            if node in seen:
                continue
            seen.add(node)
            for neighbour in get_neighbours(grid, node):
                if neighbour in seen:
                    continue
                next_t.append(neighbour)
        if not next_t:
            return t
        q = next_t
        t += 1


def main():
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        grid = defaultdict(lambda: -1)
        sol1, goal = solve_part_1(in_data, grid)
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(grid, goal)
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
