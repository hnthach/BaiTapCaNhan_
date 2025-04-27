import pygame
from collections import deque

WIDTH, HEIGHT = 300, 300
TILE_SIZE = WIDTH // 3

class Puzzle8:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.rows = 3
        self.cols = 3
        self.moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  
    
    def find_blank(self, state):
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] == 0:
                    return i, j
        return None
    
    def is_valid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols
    
    def swap(self, state, x1, y1, x2, y2):
        new_state = [row[:] for row in state]
        new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
        return new_state
    
    def bfs(self):
        queue = deque([(self.start, [])])
        visited = set()
        visited.add(tuple(map(tuple, self.start)))
        
        while queue:
            state, path = queue.popleft()
            if state == self.goal:
                return path
            
            x, y = self.find_blank(state)
            for dx, dy in self.moves:
                new_x, new_y = x + dx, y + dy
                if self.is_valid(new_x, new_y):
                    new_state = self.swap(state, x, y, new_x, new_y)
                    state_tuple = tuple(map(tuple, new_state))
                    if state_tuple not in visited:
                        visited.add(state_tuple)
                        queue.append((new_state, path + [new_state]))
        return None

def draw_grid(screen, state):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 50)
    
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                pygame.draw.rect(screen, (0, 150, 255), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                text = font.render(str(value), True, (255, 255, 255))
                screen.blit(text, (j * TILE_SIZE + TILE_SIZE // 3, i * TILE_SIZE + TILE_SIZE // 3))
    pygame.display.flip()

start_state = [
    [2, 6, 5],
    [8, 0, 7],
    [4, 3, 1]
]
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

solver = Puzzle8(start_state, goal_state)
solution = solver.bfs()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle BFS")

if solution:
    for step in solution:
        draw_grid(screen, step)
        pygame.time.delay(500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
