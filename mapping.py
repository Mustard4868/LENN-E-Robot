from collections import deque

default_grid = [
#0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
[1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], #0
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #1
[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], #2
[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], #3
[1, 0, 0, 0, 0, 0 ,0, 1, 0, 0, 0, 0, 0, 0, 1], #4
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #5
[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], #6
[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1], #7
[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], #8
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], #9
[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1] #10
]
grid = default_grid
rows = len(grid)
cols = len(grid[0])
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
direction_names = {
    "Up": "forward",
    "Down": "backward",
    "Left": "left",
    "Right": "right"
}
orientation = "Up"

def bfs_shortest_path(start, target):
    """
    Return the shortest path from start to target using the Breadth First Search algorithm.
    
    Args:
        start (tuple): (row, col) of the starting position.
        target (tuple): (row, col) of the target position.
    
    Returns:
        list: Shortest path from start to target as a list of coordinates.
    """
    if not isinstance(start, tuple) or not isinstance(target, tuple):
        raise ValueError("Start and target must be tuples representing coordinates (row, col)")
    
    queue = [(start, [start])]
    visited = set()
    visited.add(start)

    while queue:
        current_pos, path = queue.pop(0)  # Pop from the front of the list
        current_row, current_col = current_pos
        
        if current_pos == target:
            return path
        
        for dr, dc in directions:
            next_row, next_col = current_row + dr, current_col + dc
            next_pos = (next_row, next_col)
            
            if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] == 1 and next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return None

def is_junction(row, col):
    neighbor_count = 0
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if r >= 0 and r < rows and c >= 0 and c < cols:  # Combine boundary checks
            if grid[r][c] == 1:
                neighbor_count += 1
                if neighbor_count > 2:  # Early exit if more than 2 neighbors
                    return True
        
    return False


def update_orientation( new_direction):
    old_orientation = orientation

    if new_direction == (-1, 0):
        orientation = "Up"
    elif new_direction == (1, 0):
        orientation = "Down"
    elif new_direction == (0, -1):
        orientation = "Left"
    elif new_direction == (0, 1):
        orientation = "Right"

    if orientation != old_orientation:
        print(f"Robot turned to face {direction_names[orientation]}")

def getJunctions(path):
    junctions = []
    for position in path:
        row, col = position
        if is_junction(row, col):
            junctions.append(position)
    return junctions
