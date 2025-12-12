import networkx as nx
file = 'input'
# file = 'example2'

data = map(lambda x: x.split(':'), open(file).readlines())

devices = {}

for d in data:
    devices[d[0]] = set(d[1].split())

# print(devices)


def get_num_paths(devices, current_device):
    if current_device == 'out':
        return 1
    s = 0
    for d in devices[current_device]:
        s += get_num_paths(devices, d)

    return s

# print(get_num_paths(devices, 'you'))

def parse_graph(file_path):
	nodes = set()
	edges = []

	for raw_line in open(file_path).readlines():
		line = raw_line.strip()
		if not line or line.startswith("#"):
			continue

		if ":" not in line:
			raise ValueError(f"Line is missing ':' separator: {raw_line}")

		src, targets_raw = line.split(":", 1)
		src = src.strip()
		targets = [t for t in targets_raw.strip().split() if t]

		nodes.add(src)
		if not targets:
			continue

		for dst in targets:
			nodes.add(dst)
			edges.append((src, dst))

	return nodes, edges

nodes, edges = parse_graph(file)
graph = nx.DiGraph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)
print("paths")
paths = list(nx.all_simple_paths(graph, 'svr', 'out'))
print("filtering")
print(len(list(filter(lambda x: 'fft' in x and 'dac' in x, paths))))