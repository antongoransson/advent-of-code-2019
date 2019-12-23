from collections import deque
import regex as re

def new_stack(deck, n):
    deck.reverse()


def cut(deck, n):
    deck.rotate(-n)


def increment(deck, n):
    copy = deque(deck)
    l = len(deck)
    i = 0
    while copy:
        deck[i] = copy.popleft()
        i = (i + n) % l

all_moves = {
    'cut' :cut,
    'increment': increment,
    'stack': new_stack
}

def get_card(offset, increment, n):
    return offset + increment * n

def mod_inv(n, deck_size):
    return pow(n, deck_size - 2, deck_size)

def shuffle(moves, deck_size):
    offset_diff, increment_mul = 0, 1
    for move, n in moves:
        if move == 'stack':
            increment_mul = (increment_mul * -1) % deck_size
            offset_diff = (offset_diff + increment_mul) % deck_size
        elif move == 'cut':
            offset_diff = (offset_diff + increment_mul * n) % deck_size
        elif move == 'increment':
            increment_mul = (increment_mul * mod_inv(n, deck_size)) % deck_size
    return offset_diff, increment_mul

def solve_part_1(moves):
    deck = deque([i for i in range(10007)])
    for move, n in moves:
        all_moves[move](deck, n)
    return deck.index(2019)

# Great explanation by 
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju?utm_source=share&utm_medium=web2x
def solve_part_2(moves):
    n = 2020
    deck_size = 119315717514047
    n_shuffles = 101741582076661
    offset_diff, increment_mul = shuffle(moves, deck_size)
    increment = pow(increment_mul, n_shuffles, deck_size)
    offset = offset_diff * (1 - pow(increment_mul, n_shuffles, deck_size)) * mod_inv(1 - increment_mul, deck_size)
    offset %= deck_size
    return get_card(offset, increment, n) % deck_size


def main():
    data = []
    with open('input.txt') as f:
        for line in f:
            if 'stack' in line:
                data.append(('stack', 0))
            elif 'cut' in line:
                d = int(re.findall(r'-?\d+', line)[0])
                data.append(('cut', d))
            elif 'increment' in line:
                d = int(re.findall(r'-?\d+', line)[0])
                data.append(('increment', d))
    sol1 =  solve_part_1(data)
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2(data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
