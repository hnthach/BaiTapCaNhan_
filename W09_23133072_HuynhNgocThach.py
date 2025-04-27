import pygame
import sys
import heapq
from collections import deque
import time 
import random

# Kích thước giao diện
WIDTH, HEIGHT = 550, 750  
GRID_SIZE = 3
TILE_SIZE = WIDTH // GRID_SIZE
FONT_SIZE = 60  
STEP_DELAY = 300  
BUTTON_HEIGHT = 50
BUTTON_WIDTH = WIDTH // 4 - 15  
BUTTON_SPACING = 8
BUTTON_START_Y = HEIGHT - 170 
    
# Màu sắc cho từng ô
TILE_COLORS = {
    1: (255, 100, 100), 2: (100, 255, 100), 3: (100, 100, 255),
    4: (255, 255, 100), 5: (255, 100, 255), 6: (100, 255, 255),
    7: (200, 150, 100), 8: (150, 200, 150), 0: (50, 50, 50)
}

# Trạng thái đầu & trạng thái mục tiêu
start_state = ((2, 6, 5), (8, 0, 7), (4, 3, 1))
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def print_state(state):
    """In trạng thái ra console dưới dạng bảng 3x3"""
    for row in state:
        print(" | ".join(f"{cell:2}" for cell in row))
    print("-" * 10)

# Pygame khởi tạo
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle AI Solver")
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, 36)  # Giảm kích thước font
selected_algorithm = None
highlighted_tiles = []

def draw_grid(state):
    """Vẽ lưới ô số"""
    screen.fill((30, 30, 30))  
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = TILE_COLORS[value]
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            if value != 0:
                text = font.render(str(value), True, (255, 255, 255))
                screen.blit(text, (rect.x + TILE_SIZE // 3, rect.y + TILE_SIZE // 4))

def draw_buttons():
    """Vẽ nút chọn thuật toán"""
    global selected_algorithm
    button_texts = ["A*", "BFS", "DFS", "Greedy", 
                   "UCS", "IDA*", "IDDFS", 
                   "SimpleH", "SteepH", "QUIT"]  
    colors = [
        (255, 50, 50), (80, 80, 80), (255, 200, 50),
        (50, 200, 100), (220, 220, 220), (100, 50, 200), 
        (150, 100, 200), (200, 150, 100), (100, 200, 150), (200, 50, 50)
    ]
    buttons = []
    buttons_per_row = 4  # 4 nút mỗi hàng
    
    for i, text in enumerate(button_texts):
        row = i // buttons_per_row
        col = i % buttons_per_row
        rect = pygame.Rect(
            10 + col * (BUTTON_WIDTH + BUTTON_SPACING),
            BUTTON_START_Y + row * (BUTTON_HEIGHT + BUTTON_SPACING),
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        color = colors[i] if text != selected_algorithm else (0, 0, 0)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        
        # Xử lý văn bản dài
        display_text = text if len(text) <= 6 else text[:5] + ".."
        text_render = button_font.render(display_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=rect.center)
        screen.blit(text_render, text_rect)
        buttons.append((rect, text))
    return buttons

def find_blank(state):
    """Tìm vị trí ô trống"""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if state[i][j] == 0:
                return i, j

def swap_tiles(state, i1, j1, i2, j2):
    """Hoán đổi hai ô"""
    new_state = [list(row) for row in state]
    new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
    return tuple(tuple(row) for row in new_state)

def manhattan_distance(state):
    """Tính khoảng cách Manhattan"""
    total = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = (value - 1) // GRID_SIZE, (value - 1) % GRID_SIZE
                total += abs(i - goal_x) + abs(j - goal_y)
    return total

def ida_star_search(start, goal):
    """Giải bằng IDA*"""
    bound = manhattan_distance(start)
    path = [start]

    def search(g, bound):
        state = path[-1]
        f = g + manhattan_distance(state)
        if f > bound:
            return f
        if state == goal:
            return "FOUND"
        min_bound = float('inf')
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in path:
                    path.append(new_state)
                    result = search(g + 1, bound)
                    if result == "FOUND":
                        return "FOUND"
                    if result < min_bound:
                        min_bound = result
                    path.pop()
        return min_bound

    while True:
        result = search(0, bound)
        if result == "FOUND":
            return path
        if result == float('inf'):
            return None
        bound = result

def bfs(start, goal):
    """Giải bằng BFS"""
    queue = deque([(start, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [new_state]))
    return None

def dfs(start, goal, depth_limit=50):
    """Giải bằng DFS với giới hạn độ sâu"""
    stack = [(start, [], 0)]  # (state, path, current_depth)
    visited = set()
    while stack:
        state, path, depth = stack.pop()
        if state == goal:
            return path + [goal]
        if depth >= depth_limit:
            continue  # Bỏ qua nếu vượt quá độ sâu tối đa
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, path + [new_state], depth + 1))
    return None

def iddfs(start, goal):
    """Giải bằng IDDFS (Iterative Deepening DFS)"""
    depth_limit = 0
    while True:
        result = dfs(start, goal, depth_limit)
        if result is not None:
            return result
        depth_limit += 1

def greedy(start, goal):
    """Giải bằng Greedy"""
    priority_queue = [(manhattan_distance(start), start, [])]
    visited = set()
    while priority_queue:
        _, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    heapq.heappush(priority_queue, (manhattan_distance(new_state), new_state, path + [new_state]))
    return None

def ucs(start, goal):
    """Giải bằng UCS"""
    priority_queue = [(0, start, [])]
    visited = set()
    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    heapq.heappush(priority_queue, (cost + 1, new_state, path + [new_state]))
    return None

def a_star(start, goal):
    """Giải bằng A*"""
    priority_queue = [(manhattan_distance(start), 0, start, [])]
    visited = set()
    while priority_queue:
        _, cost, state, path = heapq.heappop(priority_queue)
        if state == goal:
            return path + [goal]
        blank_i, blank_j = find_blank(state)
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    heapq.heappush(priority_queue, (cost + 1 + manhattan_distance(new_state), cost + 1, new_state, path + [new_state]))
    return None

def simple_hill_climbing(start, goal, max_steps=1000):
    """Simple Hill Climbing với cải tiến"""
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
        
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                new_h = manhattan_distance(new_state)
                neighbors.append((new_h, new_state))
        
        if not neighbors:
            break
            
        # Chọn ngẫu nhiên một trạng thái tốt hơn
        random.shuffle(neighbors)
        improved = False
        for h, state in neighbors:
            if h < current_h:
                current_state = state
                current_h = h
                path.append(current_state)
                improved = True
                break
                
        if not improved:
            break
    
    return path

def steepest_hill_climbing(start, goal, max_steps=1000):
    """Steepest Hill Climbing với cải tiến"""
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
        
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                new_h = manhattan_distance(new_state)
                neighbors.append((new_h, new_state))
        
        if not neighbors:
            break
            
        neighbors.sort(key=lambda x: x[0])
        best_h, best_state = neighbors[0]
        
        if best_h >= current_h:
            break
            
        current_state = best_state
        current_h = best_h
        path.append(current_state)
    
    return path

def main():
    global selected_algorithm, highlighted_tiles
    running = True
    path = None
    step = 0
    
    while running:
        # Vẽ giao diện
        current_state = path[step] if path else start_state
        draw_grid(current_state)
        buttons = draw_buttons()
        
        # Hiển thị thông báo
        if selected_algorithm:
            if path is None:
                warning = button_font.render("No solution found!", True, (255, 50, 50))
                screen.blit(warning, (WIDTH//2 - warning.get_width()//2, BUTTON_START_Y - 40))
            else:
                info = button_font.render(f"Steps: {len(path)-1}", True, (200, 200, 200))
                screen.blit(info, (WIDTH//2 - info.get_width()//2, BUTTON_START_Y - 40))
        
        pygame.display.flip()
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for rect, algo in buttons:
                    if rect.collidepoint(x, y):
                        if algo == "QUIT":
                            running = False
                        else:
                            selected_algorithm = algo
                            start_time = time.time()
                            try:
                                if algo == "A*": path = a_star(start_state, goal_state)
                                elif algo == "BFS": path = bfs(start_state, goal_state)
                                elif algo == "DFS": path = dfs(start_state, goal_state)
                                elif algo == "Greedy": path = greedy(start_state, goal_state)
                                elif algo == "UCS": path = ucs(start_state, goal_state)
                                elif algo == "IDA*": path = ida_star_search(start_state, goal_state)
                                elif algo == "IDDFS": path = iddfs(start_state, goal_state)
                                elif algo == "Hill": path = simple_hill_climbing(start_state, goal_state)
                                elif algo == "Steep": path = steepest_hill_climbing(start_state, goal_state)
                                
                                end_time = time.time()
                                print(f"{algo} time: {end_time-start_time:.4f}s")
                                if path: 
                                    print(f"Solution found in {len(path)-1} steps")
                                    for state in path:
                                        print_state(state)
                                else:
                                    print("No solution found!")
                            except Exception as e:
                                print(f"Error: {str(e)}")
                                path = None
                            step = 0
        
        # Tự động chạy animation nếu có path
        if path and step < len(path) - 1:
            pygame.time.delay(STEP_DELAY)
            step += 1
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
