import sys

def dfs(graph, start):
    visited = set()
    visit_order = []
    discovery_times = {}
    finish_times = {}
    time = [0]
    
    def dfs_visit(node):
        time[0] += 1
        discovery_times[node] = time[0]
        visited.add(node)
        visit_order.append(node)
        
        for neighbor in sorted(graph.get(node, [])):
            if neighbor not in visited:
                dfs_visit(neighbor)
        
        time[0] += 1
        finish_times[node] = time[0]
    
    dfs_visit(start)
    
    return visit_order, discovery_times, finish_times

lines = []
for line in sys.stdin:
    lines.append(line.strip())

v, e = map(int, lines[0].split())

graph = {}
for i in range(1, e + 1):
    u, v_node = map(int, lines[i].split())
    if u not in graph:
        graph[u] = []
    graph[u].append(v_node)

start_node = int(lines[e + 1])

visit_order, discovery_times, finish_times = dfs(graph, start_node)

print("Visit order:", " ".join(map(str, visit_order)))
first = True
for node in visit_order:
    if first:
        print(f"Discovery/finish: {node} d={discovery_times[node]} f={finish_times[node]}")
        first = False
    else:
        print(f"{node} d={discovery_times[node]} f={finish_times[node]}")