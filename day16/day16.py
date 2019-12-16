def pattern(n, l, start = 0):
    i, j = start, 0
    p = [0, 1, 0, -1]
    k = 0 if start == 0 else 1
    first = True if start == 0 else False
    while i < l:
        j = 0
        while j < n and i < l:
            if first:
                first = False
            else:
                yield p[k % len(p)]
                i += 1
            j += 1
        k += 1
        

def solve_part_1(in_data):
    signal = in_data
    l = len(signal)
    for phase in range(100):
        new_signal = ''
        for i in range(l):
            j = i
            s = 0
            for x in pattern(i + 1, l, j):
                s += int(signal[j]) * x
                j += 1
            new_signal += str(abs(s) % 10)
        signal = new_signal
    return signal[:8]


def solve_part_2(in_data):
    signal = in_data
    for phase in range(100):
        s = 0
        a = []
        for i in range(len(signal) - 1, -1, -1):
            s += int(signal[i]) 
            a.append(str(s % 10))
        signal = "".join(reversed(a))
    return signal[:8]


def main():
    in_data = "59731816011884092945351508129673371014862103878684944826017645844741545300230138932831133873839512146713127268759974246245502075014905070039532876129205215417851534077861438833829150700128859789264910166202535524896960863759734991379392200570075995540154404564759515739872348617947354357737896622983395480822393561314056840468397927687908512181180566958267371679145705350771757054349846320639601111983284494477902984330803048219450650034662420834263425046219982608792077128250835515865313986075722145069152768623913680721193045475863879571787112159970381407518157406924221437152946039000886837781446203456224983154446561285113664381711600293030463013"
    sol1 =  solve_part_1(in_data)
    print('Part 1: {}'.format(sol1))
    offset = int(in_data[:7])
    in_data *= 10000
    in_data = in_data[offset:]
    sol2 = solve_part_2(in_data)
    print('Part 2: {}'.format(sol2))


if __name__ == "__main__":
    main()
