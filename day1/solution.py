from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()
rotations = [int(l[1:]) * (-1 if l[0] == "L" else 1) for l in lines]
# print(rotations)


def part1():
    n = 50
    t = 0
    for r in rotations:
        n = (n + r) % 100
        t += n == 0
    return t


def part2():
    t = 0
    n = 50
    # I'm sure there's a fancy arithmetic way to do this but I'm too tired
    for r in rotations:
        extra_amt = abs(int(r / 100))
                   # take the remainder and keep the sign
        base_amt = n + (r - int(r / 100) * 100) not in range(1, 100) and n != 0
        t += base_amt + extra_amt
        n = (n + r) % 100
    return t


print(part1())
print(part2())
