
def valid_pairs(pw):
    matching_digits = []
    for i in range(1, len(pw)):
        if pw[i - 1] is pw[i]:
            matching_digits.append(pw[i])
        if pw[i - 1] > pw[i]:
            return []
    return matching_digits


def solve_part_1():
    nbr_valid = 0
    for i in range(388888, 799999 + 1):
        if len(valid_pairs(str(i))) >= 1:
            nbr_valid += 1
    return nbr_valid


def solve_part_2():
    nbr_valid = 0
    for i in range(388888, 799999 + 1):
        pairs = valid_pairs(str(i))
        if len([d for d in pairs if pairs.count(d) == 1]) >= 1:
            nbr_valid += 1
    return nbr_valid


def main():
    sol1 = solve_part_1()
    print('Part 1: {}'.format(sol1))
    sol2 = solve_part_2()
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
