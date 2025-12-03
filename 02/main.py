file = "input"
# file = "example"

data =  list(map(lambda y: list(map(lambda x: x.split('-'), y.split(','))), open(file).readlines()))[0]
invalid_sum = 0
for r in data:
    start = int(r[0])
    stop = int(r[1])

    for i in range(start, stop+1):
        l = str(i)
        if l[:len(l) // 2] == l[len(l) // 2:]:
            invalid_sum += i

print(f"Part 1: {invalid_sum}")

invalid_sum = 0
for r in data:
    start = int(r[0])
    stop = int(r[1])

    for i in range(start, stop+1):
        l = str(i)
        for k in range(1, len(l) // 2 + 1):
            if len(l) % k != 0:
                continue
            count = len(l) // k
            found = False
            for j in range(count):
                if l[:k] != l[j * k: j * k + k]:
                    break
            else:
                found = True
            if found:
                invalid_sum += i
                # print(i)
                break


print(f"Part 2: {invalid_sum}")