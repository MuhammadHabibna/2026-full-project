import pygame
import random
import sys

# Settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Pygame Init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Day 32: Maze Generator & Solver")
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        
    def draw(self, surface):
        x = self.x * CELL_SIZE
        y = self.y * CELL_SIZE
        
        if self.visited:
            pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
        else:
             pygame.draw.rect(surface, (50, 50, 50), (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls['top']:
            pygame.draw.line(surface, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls['right']:
            pygame.draw.line(surface, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls['bottom']:
            pygame.draw.line(surface, WHITE, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls['left']:
            pygame.draw.line(surface, WHITE, (x, y + CELL_SIZE), (x, y), 2)

    def check_neighbors(self, grid):
        neighbors = []
        top = grid[getIndex(self.x, self.y - 1)] if self.y > 0 else None
        right = grid[getIndex(self.x + 1, self.y)] if self.x < COLS - 1 else None
        bottom = grid[getIndex(self.x, self.y + 1)] if self.y < ROWS - 1 else None
        left = grid[getIndex(self.x - 1, self.y)] if self.x > 0 else None

        if top and not top.visited: neighbors.append(('top', top))
        if right and not right.visited: neighbors.append(('right', right))
        if bottom and not bottom.visited: neighbors.append(('bottom', bottom))
        if left and not left.visited: neighbors.append(('left', left))

        if neighbors:
            return random.choice(neighbors)
        return None

def getIndex(x, y):
    if x < 0 or y < 0 or x >= COLS or y >= ROWS:
        return -1
    return x + y * COLS

def remove_walls(a, b, direction):
    if direction == 'top':
        a.walls['top'] = False
        b.walls['bottom'] = False
    elif direction == 'right':
        a.walls['right'] = False
        b.walls['left'] = False
    elif direction == 'bottom':
        a.walls['bottom'] = False
        b.walls['top'] = False
    elif direction == 'left':
        a.walls['left'] = False
        b.walls['right'] = False

def draw_current(cell, color=RED):
    x = cell.x * CELL_SIZE
    y = cell.y * CELL_SIZE
    pygame.draw.rect(screen, color, (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10))

def solve_dfs(grid):
    start = grid[0]
    end = grid[-1]
    
    stack = [start]
    came_from = {start: None}
    visited = {start}
    
    while stack:
        current = stack[-1] # DFS - strict LIFO stack for recursion simulation
        
        # If we reached the end, highlight path
        if current == end:
             break

        # Get accessible neighbors
        neighbors = []
        # Check Top
        idx = getIndex(current.x, current.y - 1)
        if idx != -1 and not current.walls['top'] and grid[idx] not in visited:
            neighbors.append(grid[idx])
        # Check Right
        idx = getIndex(current.x + 1, current.y)
        if idx != -1 and not current.walls['right'] and grid[idx] not in visited:
            neighbors.append(grid[idx])
        # Check Bottom
        idx = getIndex(current.x, current.y + 1)
        if idx != -1 and not current.walls['bottom'] and grid[idx] not in visited:
            neighbors.append(grid[idx])
        # Check Left
        idx = getIndex(current.x - 1, current.y)
        if idx != -1 and not current.walls['left'] and grid[idx] not in visited:
            neighbors.append(grid[idx])

        if neighbors:
            next_cell = random.choice(neighbors) # Randomize slightly for interest
            visited.add(next_cell)
            came_from[next_cell] = current
            stack.append(next_cell)
        else:
            stack.pop() # Backtrack

        # Visualization
        screen.fill(BLACK)
        for c in grid: c.draw(screen)
        
        # Draw Solution Path so far
        temp = current
        while temp:
            draw_current(temp, PURPLE)
            temp = came_from.get(temp)
        draw_current(current, GREEN)
        
        pygame.display.update()
        # clock.tick(60) # Fast solve

    return came_from

def main():
    grid = [Cell(x, y) for y in range(ROWS) for x in range(COLS)]
    current_cell = grid[0]
    current_cell.visited = True
    stack = []

    # MAZE GENERATION
    generating = True
    while generating:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        for cell in grid:
            cell.draw(screen)
        
        draw_current(current_cell, ORANGE)

        # Logic
        next_step = current_cell.check_neighbors(grid)
        if next_step:
            direction, neighbor = next_step
            neighbor.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, neighbor, direction)
            current_cell = neighbor
        elif stack:
            current_cell = stack.pop()
        else:
            generating = False # Done

        pygame.display.update()
        # clock.tick(60) # Fast generation

    # SOLVING
    pygame.time.delay(1000)
    solve_dfs(grid)
    
    # Wait loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
