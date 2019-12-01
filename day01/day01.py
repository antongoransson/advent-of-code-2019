def solve_part_1(masses):
   return sum([mass // 3 - 2 for mass in masses]) 

def solve_part_2(masses):
   return sum([calc_fuel(mass) for mass in masses])

def calc_fuel(mass):
    fuel = mass // 3 - 2
    if fuel <= 0:
        return 0
    return fuel + calc_fuel(fuel)

def main():
    with open('input.txt') as f:
        in_data = list(map(int, [mass for mass in f]))
        sol1 =  solve_part_1(in_data)
        print(f'Part 1: {sol1}')
        sol2 = solve_part_2(in_data)
        print(f'Part 2: {sol2}')

if __name__ == "__main__":
    main()
