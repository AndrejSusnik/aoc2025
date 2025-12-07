file = 'input'
# file = 'example'

data = list(map(lambda x: list(filter(lambda y: y != '', x.strip().split(' '))), open(file).readlines()))

accum = 0
for j in range(len(data[0])):
    op = data[len(data) - 1][j]
    ident = 0 if op == '+' else 1
    for i in range(len(data) - 1):
        if op == '+':
            ident += int(data[i][j])
        else:
            ident *= int(data[i][j])

    accum += ident

print(f"Part 1: {accum}")
    

data = list(map(lambda x: x[:-1], open(file).readlines()))

total = 0
op = ""
nums = []
for j in range(len(data[0]) - 1, -1, -1):
    found = False
    t_num = ""
    for i in range(len(data) - 1):
        if data[i][j] != ' ':
            t_num += data[i][j]
            found = True
    if t_num != "":
        nums.append(int(t_num))

    if data[-1][j] != ' ':
        op = data[-1][j]

    if not found:
        if op == '+':
            t = 0
            for el in nums:
                t += el
            total += t
        else:
            t = 1
            for el in nums:
                t *= el
            total += t

        nums = []

if op == '+':
    t = 0
    for el in nums:
        t += el
    total += t
else:
    t = 1
    for el in nums:
        t *= el
    total += t

print(f"Part 2: {total}")