from functools import cache
from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
fw_graph = {line[:3]: tuple(line.split(" ")[1:]) for line in lines}

@cache
def go_to(cur, target):
    if cur == target:
        return 1
    if cur == "out":
        return 0
    nbs = fw_graph[cur]
    return sum(go_to(n, target) for n in nbs)

def part1():
    return go_to('you', 'out')

def part2():
    return go_to('svr', 'fft') * go_to('fft', 'dac') * go_to('dac', 'out')

print(part1())
print(part2())