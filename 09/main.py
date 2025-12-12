file = 'input'
file = 'example'

data = list(map(lambda x: tuple(map(int, x.strip().split(','))), open(file).readlines()))

def area(point1, point2):
    a = abs(point1[0] - point2[0] + 1)
    b = abs(point1[1] - point2[1] + 1)

    return a * b

max_area = 0
for c in data:
    for c2 in data:
        if c == c2:
            continue
        max_area = max(max_area, area(c, c2))

print(f"Part 1: {max_area}")
