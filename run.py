import sys
import time
import subprocess


def run_day(d):
    starttime = time.time()
    p = subprocess.Popen(
        ['python', f'day{d}.py'], cwd=f'./day{d}', stdout=subprocess.PIPE)
    result = p.stdout.read().decode('utf-8')
    endtime = time.time()
    t = endtime - starttime
    return result, t


def print_result(d, result, t):
    print(f'Day {int(d)}')
    print(result)
    print(f'Time: {round(t, 5)}s')
    print('---------------------------')


def main():
    if len(sys.argv) == 2:
        d = sys.argv[1]
        result, t = run_day(d)
        print_result(d, result, t)
        return
    start_t = time.time()
    for i in range(1, 26):
        t = int(i < 10)
        d = ('0' * t) + str(i)
        result, t = run_day(d)
        print_result(d, result, t)
    end_t = time.time()
    tot = end_t - start_t
    print(f'Total execution time: {round(tot, 5)}s')


if __name__ == '__main__':
    main()
