from collections import defaultdict, deque
import networkx as nx

def neigbours(grid, pos):
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [(pos[0] + dx, pos[1] + dy) for dx, dy in deltas if (pos[0]+ dx, pos[1] + dy) in grid]

def bfs(grid, portals):
    all_paths = defaultdict(list)
    for start, portal in portals.items():
        goals = [p for p, v in portals.items() if v != portal]
        q = deque([[start]])
        explored = set()
        while q:
            path = q.popleft()
            node = path[-1]
            if node in explored:
                continue
            for p in neigbours(grid, node):
                if p in explored:
                    continue
                new_path = list(path)
                new_path.append(p)
                q.append(new_path)
                if p in goals:
                    all_paths[start].append((p, len(path)))
            explored.add(node)
    return all_paths

def solve_part_1(grid, portals, portal_coords):
    all_paths = bfs(grid, portals)
    graph = create_graph(all_paths, portal_coords)
    start = portal_coords['AA'][0]
    goal = portal_coords['ZZ'][0]
    return nx.algorithms.shortest_path_length(graph, start, goal, weight='weight')


def solve_part_2(grid, portals, portal_coords):
    all_paths = bfs(grid, portals)
    graph = create_recursive_graph(all_paths, portal_coords)
    start = portal_coords['AA']
    goal = portal_coords['ZZ']
    return nx.algorithms.shortest_path_length(graph, start, goal, weight='weight')

def create_graph(all_paths, portal_coords):
    graph = nx.Graph()
    for p1 in all_paths:
        for p2, l in all_paths[p1]:
            graph.add_edge(p1, p2, weight=l)
    for point, v in portal_coords.items():
        if point == 'AA' or point == 'ZZ':
            continue
        p1, _ = v[0]
        p2, _ = v[1]
        graph.add_edge(p1, p2, weight=1)
    return graph

def create_recursive_graph(all_paths, portal_coords):
    graph = nx.DiGraph()
    # Assume that depth wont be higher than 50
    for level in range(50):
        for p1 in all_paths:
            for p2, l in all_paths[p1]:
                graph.add_edge((p1, level), (p2, level), weight=l)
        for point, v in portal_coords.items():
            if point == 'AA' or point == 'ZZ':
                continue
            (x1, y1), d1 = v[0]
            (x2, y2), d2 = v[1]
            if level + d1 >= 0:
                graph.add_edge(((x1, y1), level), ((x2, y2), level + d1), weight=1)
            if level + d2 >= 0:
                graph.add_edge(((x2, y2), level), ((x1, y1), level + d2), weight=1)
    return graph

def main():
    grid = {}
    max_x = 0
    max_y = 0
    with open('input.txt') as f:
        for x, line in enumerate(f):
            max_y = max(max_y, len(line))
            for y, c in enumerate(line.strip("\n")):
                if c not in " #":
                    grid[x, y] = c
            max_x += 1
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    portals = {}
    portal_coords = defaultdict(list)
    out = [0, max_x - 2, max_y - 3]
    for (row, col), c in grid.items():
        if c == '.':
            for dx, dy in deltas:
                x = dx + row
                y = dy + col
                if (x, y) in grid and grid[x, y] not in  '.#':
                    a = [(x, y), (x + dx, y + dy)]
                    a.sort()
                    portal = grid[a[0]] + grid[a[1]]
                    portals[(row, col)] = portal
                    d  = -1 if a[0][0] in out or a[0][1] in out else 1
                    if portal == 'AA' or portal == 'ZZ':
                        portal_coords[portal] = ((row, col), 0)
                    else:
                        portal_coords[portal].append(((row, col), d))
    sol1 =  solve_part_1(grid, portals, portal_coords)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(grid, portals, portal_coords)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
