from collections import deque
MAXRANGE = 3

def create_keyboard_graph():
    keyboard_layout = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]
    
    graph = {}
    
    for row in range(len(keyboard_layout)):
        for col in range(len(keyboard_layout[row])):
            key = keyboard_layout[row][col]
            graph[key] = []

            if col > 0:
                graph[key].append(keyboard_layout[row][col - 1])
            if col < len(keyboard_layout[row]) - 1:
                graph[key].append(keyboard_layout[row][col + 1])
            if row > 0 and col < len(keyboard_layout[row - 1]):
                graph[key].append(keyboard_layout[row - 1][col])
            if row < len(keyboard_layout) - 1 and col < len(keyboard_layout[row + 1]):
                graph[key].append(keyboard_layout[row + 1][col])
                
    return graph


def bidirectional_search(graph, start, goal):
    if start == goal:
        return 0
    
    start_queue = deque([(start, 0)])
    goal_queue = deque([(goal, 0)])

    start_distances = {start: 0}
    goal_distances = {goal: 0}
    
    while start_queue and goal_queue:
        if start_queue:
            current_start, depth_start = start_queue.popleft()
            
            if depth_start > MAXRANGE:
                continue
            
            for neighbor in graph[current_start]:
                if neighbor not in start_distances:
                    start_distances[neighbor] = start_distances[current_start] + 1
                    start_queue.append((neighbor, depth_start + 1))
                    if neighbor in goal_distances:
                        return start_distances[neighbor] + goal_distances[neighbor]
        
        if goal_queue:
            current_goal, depth_goal = goal_queue.popleft()
            
            if depth_goal > MAXRANGE:
                continue
            
            for neighbor in graph[current_goal]:
                if neighbor not in goal_distances:
                    goal_distances[neighbor] = goal_distances[current_goal] + 1
                    goal_queue.append((neighbor, depth_goal + 1))
                    if neighbor in start_distances:
                        return goal_distances[neighbor] + start_distances[neighbor]
            
    
    return -1


def minimum_keyboard_distance(key1, key2):
    graph = create_keyboard_graph()
    return bidirectional_search(graph, key1, key2)