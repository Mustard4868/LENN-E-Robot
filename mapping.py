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

nodes = [
    (1, 0), (1, 2), (1, 4), (1, 6), (1, 7), (1, 14),
    (3, 7), (3, 14),
    (5, 0), (5, 7), (5, 14),
    (7, 0), (7, 7),
    (9, 0), (9, 7), (9, 14),
    (10, 8), (10, 10), (10, 12), (10, 14)
]

grid = default_grid
rows = len(grid)
cols = len(grid[0])
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
direction_names = {
    "Up": "north",
    "Down": "south",
    "Left": "west",
    "Right": "east"
}
orientation = "north"

def update_orientation(current_position, next_position, current_orientation):
    """
    Update the robot's orientation based on the movement from current_position to next_position.
    
    Args:
        current_position (tuple): (row, col) of the current position.
        next_position (tuple): (row, col) of the next position.
        current_orientation (str): The current orientation of the robot.
        
    Returns:
        str: The new orientation of the robot.
    """
    current_row, current_col = current_position
    next_row, next_col = next_position
    
    # Determine the movement direction
    if next_row == current_row and next_col == current_col + 1:
        direction = "Right"
    elif next_row == current_row and next_col == current_col - 1:
        direction = "Left"
    elif next_row == current_row + 1 and next_col == current_col:
        direction = "Down"
    elif next_row == current_row - 1 and next_col == current_col:
        direction = "Up"
    else:
        raise ValueError("Invalid movement from current_position to next_position")
    
    # Only update the orientation if the new direction is different from the current orientation
    if direction_names[direction] != current_orientation:
        new_orientation = direction_names[direction]
    else:
        new_orientation = current_orientation
    
    return new_orientation

def bfs_shortest_path(start, target):
    """
    Return the shortest path from start to target using the Breadth First Search algorithm.
    
    Args:
        start (tuple): (row, col) of the starting position.
        target (tuple): (row, col) of the target position.
    
    Returns:
        list: Shortest path from start to target as a list of coordinates and orientations.
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
            path_nodes = []
            current_orientation = orientation

            for i in range(len(path) - 1):
                if path[i] in nodes:
                    path_nodes.append((path[i], current_orientation))
                current_orientation = update_orientation(path[i], path[i+1], current_orientation)
                
            return path_nodes
        
        for dr, dc in directions:
            next_row, next_col = current_row + dr, current_col + dc
            next_pos = (next_row, next_col)
            
            if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] == 1 and next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return None
