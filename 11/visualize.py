"""Render a directed graph from the simple adjacency-list text format.

Supports static PNG/SVG/PDF output and interactive HTML (pan/zoom + hover).
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

try:
	import plotly.graph_objects as go
except Exception:  # Plotly is optional; interactive mode will check explicitly.
	go = None


def parse_graph(file_path: Path):
	"""Parse lines like `src: a b c` into nodes and edges."""
	nodes = set()
	edges = []

	for raw_line in file_path.read_text().splitlines():
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


def compute_layout(graph: nx.DiGraph, rankdir: str):
	try:
		# Prefer a tidy DOT layout if graphviz is available.
		return nx.nx_pydot.graphviz_layout(graph, prog="dot", args=f"-Grankdir={rankdir}")
	except Exception:
		# Fall back to a deterministic spring layout.
		return nx.spring_layout(graph, seed=42)


def draw_static(nodes, edges, output_path: Path, rankdir: str):
	graph = nx.DiGraph()
	graph.add_nodes_from(nodes)
	graph.add_edges_from(edges)

	pos = compute_layout(graph, rankdir)

	plt.figure(figsize=(12, 8))
	nx.draw_networkx(
		graph,
		pos,
		node_color="#f5f5f5",
		edgecolors="#333333",
		node_size=900,
		font_size=8,
		arrowsize=12,
		width=1.2,
	)
	plt.axis("off")
	plt.tight_layout()

	output_path.parent.mkdir(parents=True, exist_ok=True)
	plt.savefig(output_path)
	plt.close()


def draw_interactive(nodes, edges, output_path: Path, rankdir: str):
	if go is None:
		raise ImportError("plotly is required for interactive output. Install with `pip install plotly`." )

	graph = nx.DiGraph()
	graph.add_nodes_from(nodes)
	graph.add_edges_from(edges)

	pos = compute_layout(graph, rankdir)

	edge_x, edge_y = [], []
	for src, dst in graph.edges():
		x0, y0 = pos[src]
		x1, y1 = pos[dst]
		edge_x += [x0, x1, None]
		edge_y += [y0, y1, None]

	edge_trace = go.Scatter(
		x=edge_x,
		y=edge_y,
		line=dict(width=1.2, color="#444"),
		hoverinfo="none",
		mode="lines",
	)

	node_x, node_y, labels = [], [], []
	for node in graph.nodes():
		x, y = pos[node]
		node_x.append(x)
		node_y.append(y)
		labels.append(node)

	node_trace = go.Scatter(
		x=node_x,
		y=node_y,
		mode="markers+text",
		text=labels,
		textposition="middle right",
		hovertext=labels,
		hoverinfo="text",
		marker=dict(
			showscale=False,
			color="#f5f5f5",
			line=dict(color="#333", width=1.2),
			size=18,
		),
	)

	fig = go.Figure(data=[edge_trace, node_trace])
	fig.update_layout(
		showlegend=False,
		margin=dict(l=10, r=10, t=10, b=10),
		plot_bgcolor="white",
		xaxis=dict(showgrid=False, zeroline=False, visible=False),
		yaxis=dict(showgrid=False, zeroline=False, visible=False),
	)
	fig.update_yaxes(scaleanchor="x", scaleratio=1)

	output_path.parent.mkdir(parents=True, exist_ok=True)
	fig.write_html(output_path)


def main():
	parser = argparse.ArgumentParser(description="Draw a directed graph from text format")
	parser.add_argument("--file", default="example2", help="Input file with adjacency list (default: example2)")
	parser.add_argument(
		"--out",
		default="graph.html",
		help="Output path. Use .html for interactive or .png/.svg/.pdf for static",
	)
	parser.add_argument(
		"--rankdir",
		default="LR",
		choices=["LR", "RL", "TB", "BT"],
		help="Graphviz rankdir when dot is available",
	)
	parser.add_argument(
		"--mode",
		choices=["interactive", "static"],
		default="interactive",
		help="interactive=HTML (plotly), static=PNG/SVG/PDF (matplotlib)",
	)
	args = parser.parse_args()

	input_path = Path(args.file)
	if not input_path.exists():
		raise FileNotFoundError(f"Input file not found: {input_path}")

	nodes, edges = parse_graph(input_path)
	if not edges:
		raise ValueError("No edges parsed from input; ensure lines use 'src: dst1 dst2'")

	output_path = Path(args.out)

	if args.mode == "interactive" or output_path.suffix.lower() == ".html":
		draw_interactive(nodes, edges, output_path, args.rankdir)
		mode_used = "interactive"
	else:
		draw_static(nodes, edges, output_path, args.rankdir)
		mode_used = "static"

	print(
		f"Wrote {mode_used} graph with {len(nodes)} nodes and {len(edges)} edges to {output_path}"
	)


if __name__ == "__main__":
	main()
