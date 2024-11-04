import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import heapq

MAX_CORD = 100
CONNECT = 0.8
SHOWLABELS = False
NO_CITIES = 10

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y



def generate_cities(num_cities):
    cities = []
    for i in range(num_cities):
        x, y = random.uniform(-MAX_CORD, MAX_CORD), random.uniform(-MAX_CORD, MAX_CORD)
        cities.append(City(f"C_{i}", x, y))
    return cities

def euclidean_distance(city1, city2):
    return ((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2) ** 0.5

def create_graph(cities, all_connections = True):
    G = nx.Graph()
    for city in cities:
        G.add_node(city.name, pos=(city.x, city.y))
    
    if all_connections:
        for i, j in itertools.combinations(cities, 2):
            dist = euclidean_distance(i, j)
            G.add_edge(i.name, j.name, distance = dist)
    else:
        num_possible_roads = len(cities) * (len(cities) - 1) // 2
        num_roads = int(num_possible_roads * CONNECT)
        all_pairs = list(itertools.combinations(cities, 2))
        selected_roads = random.sample(all_pairs, num_roads)
        
        for i, j in selected_roads:
            dist = euclidean_distance(i, j)
            G.add_edge(i.name, j.name, distance = dist)
    
    return G


def plot_graph(G, title):
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue")
    if SHOWLABELS == True:
        labels = {(u, v): round(d['distance']) for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)
    plt.title(title)
    plt.show()


def bfs(graph, start_city):
    num_cities = len(graph.nodes)
    queue = deque([(start_city, [start_city], 0)])
    min_cost = float('inf')
    best_path = None
    
    while queue:
        current_node, path_taken, cost_so_far = queue.popleft()
        
        if len(path_taken) == num_cities:
            if start_city in graph[path_taken[-1]]:
                cost_so_far += graph[path_taken[-1]][start_city]['distance']
                
                if cost_so_far < min_cost:
                    min_cost = cost_so_far
                    best_path = path_taken + [start_city]
        
        for neighbor in graph.neighbors(current_node):
            if neighbor not in path_taken:
                new_path = path_taken + [neighbor]
                new_cost = cost_so_far + graph[current_node][neighbor]['distance']
                
                if new_cost < min_cost:
                    queue.append((neighbor, new_path, new_cost))
    
    return best_path, min_cost


def dfs(graph, start_city):
    num_cities = len(graph.nodes)
    all_cities = list(graph.nodes)
    
    visited = {city: False for city in all_cities}
    min_cost = float('inf')
    best_path = None
    
    def dfs_recursive(current_node, current_cost, path_taken):
        nonlocal min_cost, best_path
        visited[current_node] = True
        if len(path_taken) == num_cities:
            if start_city in graph[path_taken[-1]]:
                total_cost = current_cost + graph[path_taken[-1]][start_city]['distance']
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_path = path_taken + [start_city]
        for neighbor in graph.neighbors(current_node):
            if not visited[neighbor]:
                new_cost = current_cost + graph[current_node][neighbor]['distance']
                dfs_recursive(neighbor, new_cost, path_taken + [neighbor])
        visited[current_node] = False
    dfs_recursive(start_city, 0, [start_city])
    return best_path, min_cost


def greedy(graph, start):
    path = [start]
    total_cost = 0
    while len(path) < len(graph.nodes()):
        last = path[-1]
        neighbors = [node for node in graph.neighbors(last) if node not in path]
        if not neighbors:
            raise ValueError(f"No valid path found from {last}.")
        
        next_city = min(neighbors, key=lambda node: graph[last][node]['distance'])
        path.append(next_city)
        total_cost += graph[last][next_city]['distance']
    if start in graph[path[-1]]:
        total_cost += graph[path[-1]][start]['distance']
        path.append(start)
    else:
        raise ValueError(f"No valid path found from {path[-1]} to {start}.")
    
    return path, total_cost



def mst(graph):
    def prims_algorithm(graph):
        start_node = list(graph.nodes)[0]
        visited = set([start_node])
        edges = [
            (graph[start_node][neighbor]['distance'], start_node, neighbor)
            for neighbor in graph.neighbors(start_node)
        ]
        heapq.heapify(edges)
        mst_edges = []

        while edges:
            cost, frm, to = heapq.heappop(edges)
            if to not in visited:
                visited.add(to)
                mst_edges.append((frm, to, cost))
                for next_node in graph.neighbors(to):
                    if next_node not in visited:
                        heapq.heappush(edges, (graph[to][next_node]['distance'], to, next_node))

        return mst_edges

    def dfs_path(graph, start_node):
        visited = set()
        path = []

        def dfs(node):
            visited.add(node)
            path.append(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor)
            return path

        return dfs(start_node)

    mst_edges = prims_algorithm(graph)
    mst_graph = nx.Graph()
    mst_graph.add_weighted_edges_from([(frm, to, cost) for frm, to, cost in mst_edges])

    start_node = list(graph.nodes)[0]
    path = dfs_path(mst_graph, start_node)
    path.append(start_node)

    total_cost = 0
    for i in range(len(path) - 1):
        if path[i + 1] in graph[path[i]]:
            total_cost += graph[path[i]][path[i + 1]]['distance']

    return path, total_cost


def bidirectional_search(G, start, goal):
    if start == goal:
        return [start]
    
    forward_queue = {start: [start]}
    backward_queue = {goal: [goal]}
    
    while forward_queue and backward_queue:
        if forward_queue:
            f_node, f_path = forward_queue.popitem()
            for neighbor in G.neighbors(f_node):
                if neighbor not in forward_queue and neighbor not in f_path:
                    new_path = f_path + [neighbor]
                    if neighbor in backward_queue:
                        return new_path + backward_queue[neighbor][::-1][1:]
                    forward_queue[neighbor] = new_path
        
        if backward_queue:
            b_node, b_path = backward_queue.popitem()
            for neighbor in G.neighbors(b_node):
                if neighbor not in backward_queue and neighbor not in b_path:
                    new_path = b_path + [neighbor]
                    if neighbor in forward_queue:
                        return forward_queue[neighbor] + new_path[::-1][1:]
                    backward_queue[neighbor] = new_path
    
    return None


cities = generate_cities(NO_CITIES)
G_all = create_graph(cities, all_connections=True)
G_partial = create_graph(cities, all_connections=False)

plt.figure(figsize=(14, 7))
plt.subplot(121)
plot_graph(G_all, "All Direct Connections")

plt.subplot(122)
plot_graph(G_partial, "80% Connections")
plt.show()

start_city = cities[0].name


print("\nmst:")
path, cost = mst(G_all)
print(f"Path: {path},\n Cost: {cost}")

print("\nGreedy:")
path, cost = greedy(G_all, start_city)
print(f"Path: {path},\n Cost: {cost}")

print("BFS ALL:")
path, cost = bfs(G_all, start_city)
print(f"Path: {path}\n Cost: {cost}")

print("DFS ALL:")
path, cost = dfs(G_all, start_city)
print(f"Path: {path}\n Cost: {cost}")

print("BFS 80:")
path, cost = bfs(G_partial, start_city)
print(f"Path: {path}\n Cost: {cost}")

print("DFS 80:")
path, cost = dfs(G_partial, start_city)
print(f"Path: {path}\n Cost: {cost}")


a = random.randint(0, NO_CITIES)
b = 0
while b == a:
    b = random.randint(0, NO_CITIES) 
city_a = cities[a].name
city_b = cities[b].name
print(f"\nShortest path between {city_a} and {city_b} using bidirectional search:")
path = bidirectional_search(G_partial, city_a, city_b)
print(f"Path: {path}")
