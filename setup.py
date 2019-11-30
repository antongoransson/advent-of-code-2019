import sys
import time
import subprocess


def run_day(d):
    starttime = time.time()
    p = subprocess.call(
        ['mkdir', f'day{d}'], cwd='./', stdout=subprocess.PIPE)
    s = subprocess.call(
        ['touch', f'day{d}.py'], cwd=f'./day{d}', stdout=subprocess.PIPE)
    a = subprocess.call(
        ['touch', 'input.txt'], cwd=f'./day{d}', stdout=subprocess.PIPE)
    endtime = time.time()
    t = endtime - starttime
    return t
def main():
    if len(sys.argv) == 2:
        d = sys.argv[1]
        t = run_day(d)
        return
    start_t = time.time()
    for i in range(1, 26):
        t = int(i < 10)
        d = ('0' * t) + str(i)
        t = run_day(d)
    end_t = time.time()
    tot = end_t - start_t
    print(f'Total execution time: {round(tot, 5)}s')


if __name__ == '__main__':
    main()
