def n_adjactent_bugs(grid, pos):
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    x, y = pos
    n_bugs = 0
    for dx, dy in deltas:
        x1, y1 = x + dx, y + dy
        if 0 <= x1 < len(grid) and 0 <= y1 < len(grid[0]):
            if grid[x + dx][y + dy] == '#':
                n_bugs += 1
    return n_bugs


def n_adjactent_bugs_rec(grid, pos, level, levels):
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    x, y = pos
    n_bugs = 0
    for dx, dy in deltas:
        x1, y1 = x + dx, y + dy
        if 0 <= x1 < len(grid) and 0 <= y1 < len(grid[0]):
            if grid[x + dx][y + dy] == '#':
                n_bugs += 1
            elif (x1, y1) == (2, 2):
                if level + 1 in levels:
                    if (x, y) == (1, 2):
                        n_bugs += sum([int(c == '#')
                                       for c in levels[level + 1][0]])
                    elif (x, y) == (3, 2):
                        n_bugs += sum([int(c == '#')
                                       for c in levels[level + 1][len(grid) - 1]])
                    elif (x, y) == (2, 1):
                        n_bugs += sum([int(levels[level + 1][i][0] == '#')
                                       for i in range(len(grid))])
                    elif (x, y) == (2, 3):
                        n_bugs += sum([int(levels[level + 1][i][4] == '#')
                                       for i in range(len(grid))])
        elif level - 1 in levels:
            if y1 < 0:
                n_bugs += int(levels[level - 1][2][1] == '#')
            elif x1 < 0:
                n_bugs += int(levels[level - 1][1][2] == '#')
            elif x1 == len(grid):
                n_bugs += int(levels[level - 1][3][2] == '#')
            elif y1 == len(grid[0]):
                n_bugs += int(levels[level - 1][2][3] == '#')
    return n_bugs


def grid_to_str(grid):
    return "".join(["".join(row) for row in grid])


def score(grid):
    l = len(grid)
    return sum([2 ** (x * l + y) for x in range(l) for y in range(l) if grid[x][y] == '#'])


def solve_part_1(grid):
    seen = set(grid_to_str(grid))
    while True:
        next_state = empty_grid()
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                n_bugs = n_adjactent_bugs(grid, (x, y))
                if n_bugs == 1 or grid[x][y] == '.' and n_bugs == 2:
                    next_state[x][y] = '#'
        grid = next_state
        s = grid_to_str(grid)
        if s in seen:
            return score(grid)
        seen.add(s)


def empty_grid():
    return[['.' for _ in range(5)] for _ in range(5)]


def solve_part_2(grid):
    levels = {0: grid}
    for t in range(200):
        for d in [-1 * (t + 1), t + 1]:
            levels[d] = empty_grid()
        next_levels = {}
        for level, grid in levels.items():
            next_state = empty_grid()
            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    n_bugs = n_adjactent_bugs_rec(grid, (x, y), level, levels)
                    if n_bugs == 1 or grid[x][y] == '.' and n_bugs == 2:
                        next_state[x][y] = '#'
            next_state[2][2] = "?"
            next_levels[level] = next_state
        levels = next_levels
    return sum([grid_to_str(grid).count('#') for grid in levels.values()])


def main():
    with open('input.txt') as f:
        grid = [list(line.strip()) for line in f]
    sol1 = solve_part_1(grid)
    print('Part 1: {}'.format(sol1))
    grid[2][2] = "?"
    sol2 = solve_part_2(grid)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
