from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()


def max_i(s, start, end):
    m = int(s[end-1])
    mi = end-1
    for i in range(end-1, start-1, -1):
        n = int(s[i])
        if n >= m:
            m, mi = n, i
    return mi


def solve(l):
    tot = 0
    for line in lines:
        n = ""
        last_max_i = -1
        for i in range(l):
            start, end = last_max_i + 1, len(line) - (l - i - 1)
            last_max_i = max_i(line, start, end)
            n += line[last_max_i]
        tot += int(n)
    return tot


def part1():
    return solve(2)


def part2():
    return solve(12)


print(part1())
print(part2())