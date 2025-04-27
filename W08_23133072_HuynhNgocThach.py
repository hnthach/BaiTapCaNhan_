import pygame
import sys
import heapq
from collections import deque
import time 

# Kích thước giao diện
WIDTH, HEIGHT = 500, 700 
GRID_SIZE = 3
TILE_SIZE = WIDTH // GRID_SIZE
FONT_SIZE = 60  
STEP_DELAY = 300  
BUTTON_HEIGHT = 60 
BUTTON_WIDTH = WIDTH // 6 - 10
BUTTON_SPACING = 10
BUTTON_START_Y = HEIGHT - 150  

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
    print("-" * 10)  # Dòng phân cách giữa các trạng thái

# Pygame khởi tạo
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle AI Solver")
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, 40)
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
    button_texts = ["A*", "BFS", "DFS", "Greedy", "UCS", "IDA*", "IDDFS", "QUIT"]  
    colors = [
        (255, 50, 50), (80, 80, 80), (255, 200, 50),
        (50, 200, 100), (220, 220, 220), (100, 50, 200), (150, 100, 200), (200, 50, 50)
    ]
    buttons = []
    num_buttons = len(button_texts)
    buttons_per_row = 4  
    button_width = (WIDTH - 20 - (buttons_per_row - 1) * BUTTON_SPACING) // buttons_per_row  

    for i, text in enumerate(button_texts):
        row = i // buttons_per_row
        col = i % buttons_per_row
        rect = pygame.Rect(
            10 + col * (button_width + BUTTON_SPACING),
            BUTTON_START_Y + row * (BUTTON_HEIGHT + BUTTON_SPACING),
            button_width,
            BUTTON_HEIGHT
        )
        color = colors[i] if text != selected_algorithm else (0, 0, 0)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text_render = button_font.render(text, True, (255, 255, 255))
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

def main():
    global selected_algorithm, highlighted_tiles
    running = True
    path = None
    step = 0
    
    while running:
        if path and step < len(path) - 1:
            prev_state, current_state = path[step], path[step + 1]
            highlighted_tiles = [find_blank(prev_state), find_blank(current_state)]
        else:
            highlighted_tiles = []

        draw_grid(path[step] if path else start_state)
        buttons = draw_buttons()
        pygame.display.flip()
        
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
                            start_time = time.time()  # Bắt đầu đo thời gian
                            if algo == "BFS":
                                path = bfs(start_state, goal_state)
                            elif algo == "DFS":
                                path = dfs(start_state, goal_state)
                            elif algo == "Greedy":
                                path = greedy(start_state, goal_state)
                            elif algo == "UCS":
                                path = ucs(start_state, goal_state)
                            elif algo == "A*":
                                path = a_star(start_state, goal_state)
                            elif algo == "IDA*":
                                path = ida_star_search(start_state, goal_state)
                            elif algo == "IDDFS":  # Xử lý IDDFS
                                path = iddfs(start_state, goal_state)
                            end_time = time.time()  # Kết thúc đo thời gian
                            print(f"Thời gian chạy của {algo}: {end_time - start_time:.4f} giây")
                            state_space = path  # Lưu lại không gian trạng thái
                            # In ra không gian trạng thái
                            print("\nKhông gian trạng thái:")
                            for state in state_space:
                                print_state(state)
                        step = 0  # Reset bước về 0 sau khi tìm xong đường đi
        
        if path and step < len(path) - 1:
            pygame.time.delay(STEP_DELAY)
            step += 1
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
