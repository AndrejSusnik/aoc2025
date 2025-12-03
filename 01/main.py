file = "input"
# file = "example"

data = list(map(lambda x: (x[0], int(x[1:])), open(file).readlines()))

pos = 50
cnt = 0

for rotation in data:
    pos += rotation[1] if rotation[0] == 'R' else -rotation[1]

    while pos < 0:
        pos += 100

    while pos > 99:
        pos -= 100

    if pos == 0:
        cnt += 1

print(f"Part 1: {cnt}")

pos = 50
cnt = 0

for rotation in data:
    rotations = rotation[1]

    while rotations > 0:
        if rotation[0] == 'L':
            pos -= 1
        else:
            pos += 1

        if pos < 0:
            pos = 99

        if pos > 99:
            pos = 0

        rotations -= 1 
        if pos == 0:
            cnt += 1

print(f"Part 2: {cnt}")