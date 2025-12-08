from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()
divs = [-1] + [i for i in range(len(lines[0])) if all(l[i] == " " for l in lines)] + [len(lines[0])]
ops = [[l[divs[i] + 1 : divs[i + 1]] for l in lines] for i in range(len(divs) - 1)]


def part1():
    return sum(eval(op[-1].join(op[:-1])) for op in ops)


def part2():
    return sum(eval(op[-1].join("".join(n).strip() for n in zip(*op[:-1]))) for op in ops)


print(part1())
print(part2())
