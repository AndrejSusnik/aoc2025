from functools import cache
file = 'input'
# file = 'example'

data = tuple(map(str.strip, open(file).readlines()))

activated = 0

beams = set([data[0].index('S')])

for i in range(len(data[1:])):
    for j in range(len(data[0])):
        if data[i][j] == '^':
            if j in beams:
                activated += 1
                beams.remove(j)
                if j - 1 >= 0:
                    beams.add(j-1)
                if j + 1 < len(data[0]):
                    beams.add(j+1)

print(f"Part 1: {activated}")

@cache
def beam(beam_pos, data):
    if len(data) == 0:
        return 1

    s = 0
    for j in range(len(data[0])):
        if beam_pos == j and data[0][j] == '^':
            s += beam(j-1, data[1:]) + beam(j+1, data[1:])
        
    if s == 0:
        s += beam(beam_pos, data[1:]) 

    return s

timelines = beam(data[0].index('S'), data[1:])
print(f"Part 2: {timelines}")
