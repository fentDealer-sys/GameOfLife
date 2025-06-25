import random

class GameOfLife:
    def __init__(self, input_file):
        self.grid = self.load_grid_from_file(input_file)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    @staticmethod
    def load_grid_from_file(file_path):
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return [[int(char) for char in line] for line in lines]

    def save_grid_to_file(self, file_path):
        with open(file_path, 'w') as f:
            for row in self.grid:
                line = ''.join(['1' if cell else '0' for cell in row])
                f.write(line + '\n')

    def get_neighbors(self, x, y):
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                count += self.grid[nx][ny]
        return count

    def update(self):
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors = self.get_neighbors(i, j)
                if self.grid[i][j] == 1 and neighbors in (2, 3):
                    new_grid[i][j] = 1
                elif self.grid[i][j] == 0 and neighbors == 3:
                    new_grid[i][j] = 1
        self.grid = new_grid

    def clear(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def randomize(self):
        self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]

    def toggle_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 - self.grid[row][col]