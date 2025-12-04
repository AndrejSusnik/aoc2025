file = "input"
# file = "example"

data = list(map(lambda x: list(map(int, list(x.strip()))), open(file).readlines()))
joltage = 0
for bank in data:
    max_item = max(bank)
    max_idx = bank.index(max_item)
    if max_idx == len(bank) - 1: 
        max_item = max(bank[:len(bank)-1])
        max_idx = bank.index(max(bank[:len(bank)-1]))
    max_item2 = max(bank[max_idx+1:])
    joltage += int(f"{max_item}{max_item2}")
print(f"Part 1: {joltage}")

data = list(map(lambda x: list(map(int, list(x.strip()))), open(file).readlines()))
joltage = 0
for bank in data:
    tmp_jolt_array = []
    length = 12
    prev_max_item_idx = -1
    while length > 0:
        sub_arr = bank[prev_max_item_idx + 1:len(bank) - length + 1]
        max_item = max(sub_arr)
        prev_max_item_idx = prev_max_item_idx + sub_arr.index(max_item) + 1
        tmp_jolt_array.append(max_item)
        length -= 1
    
    joltage += int("".join(map(str, tmp_jolt_array)))

print(f"Part 2: {joltage}")