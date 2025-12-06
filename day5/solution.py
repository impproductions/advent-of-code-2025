from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()
nums_s = lines[:-1]
ops = lines[-1]

ops = []

st = 0
for i in range(len(lines[0]) + 1):
    if i == len(lines[0]) or all(l[i] in (" ") for l in lines):
        ops.append([l[st:i] for l in lines])
        st = i + 1

def trim_op(l: list[str]):
    return [el.strip() for el in l]
    
def part1():
    tot = 0
    for op in ops:
        operator = op[-1]
        nums = op[:-1]
        tot += eval(operator.join(nums))
    return tot

def part2():
    tot = 0
    for o in ops:
        operator = o[-1]
        nums = o[:-1]
        nums = list(reversed(["".join(n).strip() for n in zip(*nums)]))
        tot += eval(operator.join(nums))
    return tot


print(part1())
print(part2())
