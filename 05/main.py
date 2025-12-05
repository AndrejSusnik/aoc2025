file = 'input'
# file = 'example'

data = open(file).readlines()

ranges = [] 
products = set()

fill_ranges = True
for line in data:
    if line == '\n':
        fill_ranges = False
        continue

    if fill_ranges:
        start, stop = map(int, line.strip().split("-"))
        ranges.append((start, stop))
    else:
        products.add(int(line.strip()))

cnt = 0

for product in products:
    for range in ranges:
        if product >= range[0] and product <= range[1]:
            cnt += 1
            break
        else:
            continue

print(f"Part 1: {cnt}")

def includes(range1, range2):
    return range1[0] <= range2[0] and range1[1] >= range2[1]

def range_len(range):
    return range[1] - range[0] + 1

def overlaps(range1, range2):
    return (range2[0] <= range1[1] and range2[0] > range1[0]) or (range1[0] <= range2[1] and range1[0] > range2[0])

def join_overlaping(range1, range2):
    if includes(range1, range2):
        return range1
    if includes(range2, range1):
        return range2

    if overlaps(range1, range2): 
        if range1[0] > range2[0]:
            return (range2[0], range1[1])
        else:
            return (range1[0], range2[1])
    else:
        return None

def join_ranges(ranges):
    new_ranges = [ranges[0]]

    for range in ranges[1:]:
        for r in new_ranges:
            overlap = join_overlaping(range, r)
            if overlap:
                replace = r
                replace_with = overlap
                break
        else:
            new_ranges.append(range)
            continue

        new_ranges[new_ranges.index(replace)] = replace_with

    return new_ranges

new_ranges = ranges
while True:
    prev = new_ranges
    new_ranges = join_ranges(new_ranges)
    if len(prev) == len(new_ranges):
        break

print(new_ranges)

cnt = 0
for r in new_ranges:
    cnt += range_len(r)

print(f"Part 2: {cnt}")
    


