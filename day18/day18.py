from collections import defaultdict, deque


def parse_input(f):
    data, keys, doors = {}, {}, {}
    starts = []
    for x, line in enumerate(f):
        for y, c in enumerate(line.strip()):
            data[x, y] = c
            if 'a' <= c <= 'z':
                keys[x, y] = c
            elif 'A' <= c <= 'Z':
                doors[x, y] = c
            elif c == '@':
                starts.append((x, y))
    return data, keys, doors, starts


def get_neighbours(grid):
    n = {}
    l_x, l_y = max(grid.keys())
    for i in range(l_x + 1):
        for j in range(l_y + 1):
            deltas = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
            pos = [p for p in deltas if p[0] >= 0 and p[1] >=
                   0 and p[0] <= l_x and p[1] <= l_y and grid[p[0], p[1]] != '#']
            n[i, j] = pos
    return n


def get_all_paths(grid, all_neighbours, keys, doors, starts):
    all_paths = defaultdict(dict)
    all_starts = {k: v for k, v in keys.items()}
    for i, start in enumerate(starts):
        all_starts[start] = f'@{i if len(starts) > 1 else ""}'
    for pos, key in all_starts.items():
        explored = set()
        q = deque([[(pos, set())]])
        while q:
            path = q.popleft()
            (node, d) = path[-1]
            if node in explored:
                continue
            if node in doors:
                d = d | set(doors[node])
            for neighbour in all_neighbours[node]:
                new_path = list(path) + [(neighbour, d)]
                q.append(new_path)
                if neighbour in keys and neighbour != pos:
                    doors_on_path = "".join(sorted(list(d)))
                    if keys[neighbour] in all_paths[key]:
                        curr = all_paths[key][keys[neighbour]]
                        if len(path) < curr[0]:
                            all_paths[key][keys[neighbour]] = (
                                len(path), doors_on_path)
                    else:
                        all_paths[key][keys[neighbour]] = (
                            len(path), doors_on_path)
            explored.add(node)
    return all_paths


def set_to_str(s):
    return "".join(sorted(list(s)))


def bfs(all_paths, all_keys):
    states = {("@", ""): 0}
    q = deque([("@", "", 0)])
    while q:
        pos, keys, base_steps = q.popleft()
        if states[pos, keys] < base_steps:
            continue
        possible_states = [(k, steps) for k, (steps, doors) in all_paths[pos].items(
        ) if all(d in keys for d in doors.lower()) and k not in keys]
        for key, steps_k in possible_states:
            new_keys = "".join(sorted(keys + key))
            acc_steps = base_steps + steps_k
            if (key, new_keys) in states:
                if states[key, new_keys] > acc_steps:
                    states[key, new_keys] = acc_steps
                    q.append((key, new_keys, acc_steps))
            else:
                states[key, new_keys] = acc_steps
                q.append((key, new_keys, acc_steps))
    return states


def bfs_4(all_paths, all_keys):
    states = {
        0: {("@0", ""): 0},
        1: {("@1", ""): 0},
        2: {("@2", ""): 0},
        3: {("@3", ""): 0}
    }
    for i in range(4):
        q = deque([(f"@{i}", "", 0)])
        while q:
            pos, keys, base_steps = q.popleft()
            reachable_keys = all_paths[f"@{i}"].keys()
            doors_in_quad = set(
                "".join([all_paths[f"@{i}"][k][1] for k in reachable_keys]))
            doors_in_quad = set(
                [d for d in doors_in_quad if d.lower() in reachable_keys])
            possible_states = [(k, steps, doors) for k, (steps, doors)
                               in all_paths[pos].items() if k not in keys]
            for key, steps_k, doors in possible_states:
                rel_doors = set(doors) & doors_in_quad
                if all([d.lower() in keys for d in rel_doors]):
                    new_keys = "".join(sorted(list(set((keys + key)))))
                    acc_steps = base_steps + steps_k
                    if (key, new_keys) in states[i]:
                        if states[i][key, new_keys] > acc_steps:
                            states[i][key, new_keys] = acc_steps
                            q.append((key, new_keys, acc_steps))
                    else:
                        states[i][key, new_keys] = acc_steps
                        q.append((key, new_keys, acc_steps))
    return states


def solve_part_1(grid, all_neighbours, keys, doors, starts):
    all_paths = get_all_paths(grid, all_neighbours, keys, doors, starts)
    all_keys = "".join(sorted([v for k, v in keys.items()]))
    states = bfs(all_paths, all_keys)
    return min([steps for (pos, keys), steps in states.items() if keys == all_keys])


def solve_part_2(grid, all_neighbours, keys, doors, starts):
    all_paths = get_all_paths(grid, all_neighbours, keys, doors, starts)
    all_keys = "".join(sorted([v for k, v in keys.items()]))
    states = bfs_4(all_paths, all_keys)
    s = 0
    for i in range(4):
        m = max([len(keys) for (pos, keys), steps in states[i].items()])
        s += min([steps for (pos, keys),
                  steps in states[i].items() if len(keys) == m])
    return s


def main():
    with open('input.txt') as f:
        data, keys, doors, starts = parse_input(f)
    all_neighbours = get_neighbours(data)
    sol1 = solve_part_1(data, all_neighbours, keys, doors, starts)
    print('Part 1: {}'.format(sol1))

    with open('input2.txt') as f:
        data, keys, doors, starts = parse_input(f)
    all_neighbours = get_neighbours(data)
    sol2 = solve_part_2(data, all_neighbours, keys, doors, starts)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
