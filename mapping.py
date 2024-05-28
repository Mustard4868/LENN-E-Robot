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

class floodFill:
    def __init__(self, grid = default_grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.direction_names = {
            "Up": "forward",
            "Down": "backward",
            "Left": "left",
            "Right": "right"
        }
        self.orientation = "Up"

    def bfs_shortest_path(self, start, target) -> list[tuple[int, int]]:
        """
        Return the shortest path from start to target using Breadth First Search algorithm\n
        Args:\n
            start (tuple): (row, col) of the starting position\n
            target (tuple): (row, col) of the target position\n
            """
        # Ensure start and target are tuples
        if not isinstance(start, tuple) or not isinstance(target, tuple):
            raise ValueError("Start and target must be tuples representing coordinates (row, col)")
        
        queue = deque([(start, [start])])  # (current position, path)
        visited = set()
        visited.add(start)

        while queue:
            current_pos, path = queue.popleft()
            current_row, current_col = current_pos  # Unpack current position
            if current_pos == target:
                return path
            
            for dr, dc in self.directions:
                next_row, next_col = current_row + dr, current_col + dc
                if 0 <= next_row < self.rows and 0 <= next_col < self.cols and self.grid[next_row][next_col] == 1 and (next_row, next_col) not in visited:
                    visited.add((next_row, next_col))
                    queue.append(((next_row, next_col), path + [(next_row, next_col)]))  # Add next position and path to queue
        
        return None
    
    def is_junction(self, row, col):
        neighbor_count = 0
        
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] == 1:
                neighbor_count += 1
            
        return neighbor_count > 2
    
    def update_orientation(self, new_direction):
        old_orientation = self.orientation

        if new_direction == (-1, 0):
            self.orientation = "Up"
        elif new_direction == (1, 0):
            self.orientation = "Down"
        elif new_direction == (0, -1):
            self.orientation = "Left"
        elif new_direction == (0, 1):
            self.orientation = "Right"

        if self.orientation != old_orientation:
            print(f"Robot turned to face {self.direction_names[self.orientation]}")
    
    def simulate_robot(self, path):
        current_position_index = 0
        while current_position_index < len(path) - 1:
            current = path[current_position_index]
            next_step = path[current_position_index + 1]
            direction = (next_step[0] - current[0], next_step[1] - current[1])
            
            print(f"Move {self.direction_names[self.orientation]} to {next_step}")
            
            if self.is_junction(next_step[0], next_step[1]):
                print(f"Junction detected at {next_step}")
                # Update current position to the junction
                current_position_index += 1
                # Recalculate shortest path from junction to target
                updated_path = self.bfs_shortest_path(next_step, path[-1])
                if updated_path:
                    path = path[:current_position_index] + updated_path
                else:
                    print("No path found from junction to target.")
                    break
            else:
                current_position_index += 1
            
            self.update_orientation(direction)

            
#floodfill = floodFill()
#path = floodfill.bfs_shortest_path((10, 14), (0, 0))
#floodfill.simulate_robot(path)