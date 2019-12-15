from collections import defaultdict, deque

POS_MODE = 0
IMM_MODE = 1
REL_MODE = 2


def get_val(ip, registers, p_mode, rel_base):
    r = registers[ip]
    if p_mode == POS_MODE:
        r = registers[r]
    elif p_mode == REL_MODE:
        r = registers[rel_base + r]
    return r


def addr(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = a + b
    ip += 4
    return ip


def mulr(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = a * b
    ip += 4
    return ip


def write(registers, ip,  val1, p_modes, rel_base):
    a = registers[ip + 1]
    if p_modes[0] == REL_MODE:
        a = rel_base + a
    registers[a] = val1
    ip += 2
    return ip


def output(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    ip += 2
    return ip, a


def jmpift(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    ip = ip + 3 if a == 0 else b
    return ip


def jmpiff(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    ip = ip + 3 if a != 0 else b
    return ip


def less(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = int(a < b)
    ip += 4
    return ip


def eq(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    b = get_val(ip + 2, registers, p_modes[1], rel_base)
    c = registers[ip + 3]
    if p_modes[2] == REL_MODE:
        c = rel_base + c
    registers[c] = int(a == b)
    ip += 4
    return ip


def adj_rel_base(registers, ip, p_modes, rel_base):
    a = get_val(ip + 1, registers, p_modes[0], rel_base)
    rel_base += a
    return rel_base


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


op_codes = {
    1: addr,
    2: mulr,
    5: jmpift,
    6: jmpiff,
    7: less,
    8: eq
}

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


def run_program(program, grid):
    ip, rel_base = 0, 0
    start, goal = (0, 0), (0, 0)
    x, y = start
    d = 1
    path = []
    while program[ip] != 99:
        params = (str(program[ip])[:-2]).zfill(3)
        op = int(str(program[ip])[-2:])
        p_modes = list(map(int, params))[::-1]
        if op == 3:
            ip = write(program, ip, d, p_modes, rel_base)
        elif op == 4:
            ip, out = output(program, ip, p_modes, rel_base)
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
        elif op == 9:
            rel_base = adj_rel_base(program, ip, p_modes, rel_base)
            ip += 2
        else:
            ip = op_codes[op](program, ip, p_modes, rel_base)
    return


def solve_part_1(program, grid):
    memory = defaultdict(int, {k: v for k, v in enumerate(program)})
    n_steps, goal = run_program(memory, grid)
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
    moons = {}
    with open('input.txt') as f:
        in_data = list(map(int, f.read().strip().split(",")))
        grid = defaultdict(lambda: -1)
        sol1, goal = solve_part_1(in_data, grid)
        print('Part 1: {}'.format(sol1))
        sol2 = solve_part_2(grid, goal)
        print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
