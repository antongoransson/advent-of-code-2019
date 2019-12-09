from collections import defaultdict
import regex as re
BLACK = 0
WHITE = 1
TRANSPARENT = 2
W, H = 25, 6

code = {
    BLACK: ".",
    WHITE: "#",
    TRANSPARENT: " "
}


def solve_part_1(in_data):
    n_layers = len(in_data) // (W * H)
    img = [in_data[layer * H * W:layer * H * W + W * H]
           for layer in range(n_layers)]
    l = min(img, key=lambda x: x.count('0'))
    return l.count('1') * l.count('2')


def solve_part_2(in_data):
    n_layers = len(in_data) // (W * H)
    img = [[TRANSPARENT for _ in range(W)] for _ in range(H)]
    for layer in range(n_layers):
        for r in range(H):
            for c in range(W):
                p = int(in_data[layer * H * W + W*r + c])
                if img[r][c] == TRANSPARENT and p != TRANSPARENT:
                    img[r][c] = code[p]
    s = "\n"
    for r in img:
        s += "".join(r) + "\n"
    return s


def main():
    with open('input.txt') as f:
        in_data = f.read().strip()
    sol1 = solve_part_1(in_data)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(in_data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
