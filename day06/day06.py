from collections import defaultdict, deque


def get_all_orbits(orbits):
    objects = list(orbits.keys())
    for o in objects:
        orbiting = orbits[o]
        q = list(orbiting)
        while q:
            o1 = q.pop()
            for o2 in orbits[o1]:
                if o2 in orbits[o]:
                    continue
                q.append(o2)
                orbits[o].add(o2)
    return orbits


def bfs(graph, start, end):
    q = deque([[start]])
    explored = set()
    found = False
    while q:
        path = q.popleft()
        node = path[-1]
        if node in explored:
            continue
        for o in graph[node]:
            if o in explored or o is node:
                continue
            new_path = list(path)
            new_path.append(o)
            q.append(new_path)
            if o == end:
                return path
        explored.add(node)
    return path


def solve_part_1(in_data):
    start_orbits = defaultdict(set)
    for a, b in in_data:
        start_orbits[a].add(b)
    orbits = get_all_orbits(start_orbits)
    return sum(len(v)for v in orbits.values())


def solve_part_2(in_data):
    orbits = defaultdict(set)
    for a, b in in_data:
        orbits[a].add(b)
        orbits[b].add(a)
    path = bfs(orbits, 'YOU', 'SAN')
    return len(path) - 2


def main():
    with open('input.txt') as f:
        in_data = [line.strip().split(")")for line in f]
    sol1 = solve_part_1(in_data)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(in_data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
