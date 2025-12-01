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
        if n == 0:
            t += 1
    return t

def part2():
    t = 0
    n = 50
    for r in rotations:
        n2 = (n + r) % 100
        extra = 0
        radj = r
        if abs(r) >= 100:
            extra = abs(r) // 100
            radj = abs(r) % 100 * (-1 if r < 0 else 1)

        s = n + radj
        amt = s not in range(1, 100) and n != 0
        t += abs(amt) + extra
        if amt:
            print(n, r, radj, amt, "ex", extra, t, "to", n2)
        
        n=n2

    return t

print(part1())
print(part2())