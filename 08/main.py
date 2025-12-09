from math import sqrt
from functools import reduce
file = 'input'
# file = 'example'

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def euclidian(a, b):
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

    @staticmethod
    def from_line(line: str):
        x, y, z = map(int, line.strip().split(','))
        return Point(x, y, z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __hash__(self):
        return hash(self.__str__())

data = list(map(lambda x: Point.from_line(x), open(file).readlines()))

distances = []
for p in data:
    for p2 in data:
        if p == p2:
            continue
        distances.append((p, p2, Point.euclidian(p, p2)))
distances = sorted(distances, key=lambda x: x[2])

circutis: list[set[Point]] = [set()]
circutis[0].add(distances[0][0])
circutis[0].add(distances[0][1])

already_connected = lambda p: any(map(lambda x: True if p in x else False, circutis))
index_of = lambda p: list(map(lambda x: True if p in x else False, circutis)).index(True)

couter = 1
for i in range(2, len(distances), 2):
    if couter == 1000:
        break
    couter += 1
    d = distances[i]
    if already_connected(d[0]) and already_connected(d[1]):
        if index_of(d[0]) == index_of(d[1]):
            continue
        else:
            s1 = circutis[index_of(d[0])]
            s2 = circutis[index_of(d[1])]
            s = s1.union(s2)
            circutis.remove(s1)
            circutis.remove(s2)
            circutis.append(s)
            
    if already_connected(d[0]):
        circutis[index_of(d[0])].add(d[1])
        continue
    if already_connected(d[1]):
        circutis[index_of(d[1])].add(d[0])
        continue

    circutis.append(set())
    circutis[-1].add(d[0])
    circutis[-1].add(d[1])

print(sorted(map(len, circutis), reverse=True))
product = reduce(lambda x, y: x * y, sorted(map(len, circutis), reverse=True)[:3], 1)
print(f"Part 1: {product}")

circutis: list[set[Point]] = [set()]
circutis[0].add(distances[0][0])
circutis[0].add(distances[0][1])

for i in range(2, len(distances), 2):
    d = distances[i]
    if already_connected(d[0]) and already_connected(d[1]):
        if index_of(d[0]) != index_of(d[1]):
            s1 = circutis[index_of(d[0])]
            s2 = circutis[index_of(d[1])]
            s = s1.union(s2)
            circutis.remove(s1)
            circutis.remove(s2)
            circutis.append(s)
            
    elif already_connected(d[0]):
        circutis[index_of(d[0])].add(d[1])
    elif already_connected(d[1]):
        circutis[index_of(d[1])].add(d[0])
    else:
        circutis.append(set())
        circutis[-1].add(d[0])
        circutis[-1].add(d[1])

    if max(map(len, circutis)) == len(data):
        print(f"Part 2: {d[0].x * d[1].x}")
        break
    