import pygame
import sys
import heapq
from collections import deque
import time 
import random
import math

# ========== HẰNG SỐ ==========
WIDTH, HEIGHT = 600, 800  # Kích thước cửa sổ
GRID_SIZE = 3             # Kích thước bảng (3x3 cho puzzle 8)
TILE_SIZE = 150           # Kích thước mỗi ô
GRID_OFFSET_X = (WIDTH - GRID_SIZE * TILE_SIZE) // 2  # Căn giữa bảng theo chiều ngang
GRID_OFFSET_Y = 80        # Vị trí bảng theo chiều dọc
FONT_SIZE = 60            # Cỡ chữ trên các ô
STEP_DELAY = 300          # Thời gian delay giữa các bước giải (ms)
BUTTON_HEIGHT = 50        # Chiều cao nút
BUTTON_WIDTH = 130        # Chiều rộng nút
BUTTON_SPACING = 10       # Khoảng cách giữa các nút
BUTTON_START_Y = HEIGHT - 230  # Vị trí bắt đầu của các nút
INFO_PANEL_HEIGHT = 60    # Chiều cao panel thông tin

# Màu sắc
BACKGROUND_COLOR = (40, 40, 50)  # Màu nền
TILE_COLORS = {  # Màu cho từng ô
    1: (255, 100, 100), 2: (100, 255, 100), 3: (100, 100, 255),
    4: (255, 255, 100), 5: (255, 100, 255), 6: (100, 255, 255),
    7: (200, 150, 100), 8: (150, 200, 150), 0: (70, 70, 80)  # 0 là ô trống
}
BUTTON_COLORS = [  # Màu cho các nút
    (255, 50, 50), (80, 80, 80), (255, 200, 50), (50, 200, 100),
    (220, 220, 220), (100, 50, 200), (150, 100, 200), (200, 150, 100),
    (100, 200, 150), (150, 200, 200), (200, 100, 150), (150, 150, 200),
    (200, 50, 100), (200, 50, 50), (100, 150, 200), (200, 100, 100)
]
TEXT_COLOR = (255, 255, 255)  # Màu chữ
SHADOW_COLOR = (0, 0, 0)      # Màu bóng đổ
INFO_PANEL_COLOR = (60, 60, 70)  # Màu panel thông tin
INFO_BORDER_COLOR = (100, 100, 110)  # Màu viền panel

# Trạng thái game
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # Trạng thái đích
start_state = ((8, 6, 7), (2, 5, 4), (3, 0, 1))  # Trạng thái bắt đầu
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Các hướng di chuyển

# ========== KHỞI TẠO ==========
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle AI Solver")

# Font chữ
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, 32)
title_font = pygame.font.Font(None, 48)
info_font = pygame.font.Font(None, 34)

# Biến game
selected_algorithm = None  # Thuật toán được chọn
path = None               # Đường đi giải quyết
step = 0                  # Bước hiện tại
solving_time = 0          # Thời gian giải
dragging = None           # Ô đang được kéo
drag_start_pos = None     # Vị trí bắt đầu kéo

# ========== HÀM HỖ TRỢ ==========
def draw_grid(state):
    """Vẽ bảng puzzle với hiệu ứng hình ảnh"""
    screen.fill(BACKGROUND_COLOR)
    
    # Vẽ tiêu đề
    title = title_font.render("8-Puzzle AI Solver", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Vẽ các ô
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            rect = pygame.Rect(
                GRID_OFFSET_X + j * TILE_SIZE, 
                GRID_OFFSET_Y + i * TILE_SIZE, 
                TILE_SIZE, 
                TILE_SIZE
            )
            
            # Hiệu ứng bóng cho ô
            pygame.draw.rect(screen, SHADOW_COLOR, rect.inflate(6, 6), border_radius=10)
            pygame.draw.rect(screen, TILE_COLORS[value], rect, border_radius=8)
            
            if value != 0:
                # Chữ với hiệu ứng bóng
                text_shadow = font.render(str(value), True, SHADOW_COLOR)
                screen.blit(text_shadow, (rect.x + TILE_SIZE//3 + 2, rect.y + TILE_SIZE//4 + 2))
                text = font.render(str(value), True, TEXT_COLOR)
                screen.blit(text, (rect.x + TILE_SIZE//3, rect.y + TILE_SIZE//4))

def draw_buttons():
    """Vẽ các nút chọn thuật toán"""
    global selected_algorithm
    
    button_texts = ["A*", "BFS", "DFS", "Greedy", 
                   "UCS", "IDA*", "IDDFS", "SimpleH", 
                   "SteepH", "StochHC", "SA", "Beam",
                   "Genetic", "Nondet", "PartialObs"]
    
    buttons = []
    buttons_per_row = 4  # Số nút mỗi hàng
    
    # Tính toán vị trí các nút căn giữa
    total_width = buttons_per_row * BUTTON_WIDTH + (buttons_per_row - 1) * BUTTON_SPACING
    start_x = (WIDTH - total_width) // 2
    
    for i, text in enumerate(button_texts):
        row = i // buttons_per_row
        col = i % buttons_per_row
        
        rect = pygame.Rect(
            start_x + col * (BUTTON_WIDTH + BUTTON_SPACING),
            BUTTON_START_Y + row * (BUTTON_HEIGHT + BUTTON_SPACING),
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        
        # Màu nút (sáng hơn khi được chọn)
        color = BUTTON_COLORS[i]
        if text == selected_algorithm:
            color = tuple(min(c + 40, 255) for c in color)
        
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)
        
        # Chữ trên nút (rút gọn nếu cần)
        display_text = text if len(text) <= 7 else text[:6] + "."
        text_surf = button_font.render(display_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        
        buttons.append((rect, text))
    
    return buttons

def draw_info_panel(steps, time_elapsed):
    """Vẽ panel thông tin hiển thị số bước và thời gian"""
    panel_rect = pygame.Rect(20, BUTTON_START_Y - INFO_PANEL_HEIGHT - 10, 
                            WIDTH - 40, INFO_PANEL_HEIGHT)
    
    # Nền panel
    pygame.draw.rect(screen, INFO_PANEL_COLOR, panel_rect, border_radius=10)
    pygame.draw.rect(screen, INFO_BORDER_COLOR, panel_rect, 2, border_radius=10)
    
    # Thông tin số bước
    if steps is not None:
        steps_text = info_font.render(f"Steps: {steps}", True, (200, 230, 200))
        screen.blit(steps_text, (40, BUTTON_START_Y - INFO_PANEL_HEIGHT + 15))
    
    # Thông tin thời gian
    if time_elapsed is not None:
        time_text = info_font.render(f"Time: {time_elapsed:.3f}s", True, (200, 200, 230))
        screen.blit(time_text, (WIDTH - time_text.get_width() - 40, 
                              BUTTON_START_Y - INFO_PANEL_HEIGHT + 15))

def find_blank(state):
    """Tìm vị trí ô trống (0)"""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if state[i][j] == 0:
                return i, j
    return None

def swap_tiles(state, i1, j1, i2, j2):
    """Hoán đổi vị trí 2 ô trong puzzle"""
    state_list = [list(row) for row in state]
    state_list[i1][j1], state_list[i2][j2] = state_list[i2][j2], state_list[i1][j1]
    return tuple(tuple(row) for row in state_list)

def manhattan_distance(state):
    """Tính khoảng cách Manhattan heuristic"""
    distance = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            if value != 0:
                goal_row = (value - 1) // GRID_SIZE  # Hàng đích
                goal_col = (value - 1) % GRID_SIZE   # Cột đích
                distance += abs(i - goal_row) + abs(j - goal_col)  # Khoảng cách Manhattan
    return distance

def is_solvable(state):
    """Kiểm tra trạng thái puzzle hiện tại có giải được không"""
    flat_state = [num for row in state for num in row if num != 0]
    inversions = 0  # Số lần đảo ngược
    
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1
                
    return inversions % 2 == 0  # Puzzle giải được nếu số lần đảo ngược chẵn

# ========== CÁC THUẬT TOÁN TÌM KIẾM ==========
def a_star(start, goal):
    """Thuật toán A* sử dụng heuristic khoảng cách Manhattan"""
    priority_queue = [(manhattan_distance(start), 0, start, [start])]
    visited = set()
    
    while priority_queue:
        _, cost, state, path = heapq.heappop(priority_queue)
        
        if state == goal:
            return path
        
        if state in visited:
            continue
            
        visited.add(state)
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    new_cost = cost + 1
                    heapq.heappush(
                        priority_queue,
                        (new_cost + manhattan_distance(new_state), new_cost, new_state, path + [new_state])
                    )
    return None

def bfs(start, goal):
    """Tìm kiếm theo chiều rộng (Breadth-First Search)"""
    queue = deque([(start, [start])])
    visited = set()
    
    while queue:
        state, path = queue.popleft()
        
        if state == goal:
            return path
        
        if state in visited:
            continue
            
        visited.add(state)
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    queue.append((new_state, path + [new_state]))
    return None

def dfs(start, goal, max_depth=50):
    """Tìm kiếm theo chiều sâu với giới hạn độ sâu"""
    stack = [(start, [start], 0)]
    visited = set()
    
    while stack:
        state, path, depth = stack.pop()
        
        if state == goal:
            return path
        
        if depth >= max_depth or state in visited:
            continue
            
        visited.add(state)
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    stack.append((new_state, path + [new_state], depth + 1))
    return None

def iddfs(start, goal):
    """Tìm kiếm theo chiều sâu lặp (Iterative Deepening DFS)"""
    depth = 0
    while True:
        result = dfs(start, goal, depth)
        if result is not None:
            return result
        depth += 1
        if depth > 100:  # Ngăn vòng lặp vô hạn
            return None

def greedy(start, goal):
    """Tìm kiếm tham lam (Greedy Best-First Search)"""
    priority_queue = [(manhattan_distance(start), start, [start])]
    visited = set()
    
    while priority_queue:
        _, state, path = heapq.heappop(priority_queue)
        
        if state == goal:
            return path
        
        if state in visited:
            continue
            
        visited.add(state)
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    heapq.heappush(
                        priority_queue,
                        (manhattan_distance(new_state), new_state, path + [new_state])
                    )
    return None

def ucs(start, goal):
    """Tìm kiếm chi phí đồng nhất (Uniform Cost Search)"""
    priority_queue = [(0, start, [start])]
    visited = set()
    
    while priority_queue:
        cost, state, path = heapq.heappop(priority_queue)
        
        if state == goal:
            return path
        
        if state in visited:
            continue
            
        visited.add(state)
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    heapq.heappush(
                        priority_queue,
                        (cost + 1, new_state, path + [new_state])
                    )
    return None

def ida_star_search(start, goal):
    """Tìm kiếm A* lặp sâu (Iterative Deepening A*)"""
    threshold = manhattan_distance(start)
    path = [start]
    
    def search(path, g, threshold):
        state = path[-1]
        f = g + manhattan_distance(state)
        
        if f > threshold:
            return f
        if state == goal:
            return "FOUND"
            
        min_cost = float('inf')
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in path:
                    new_path = path + [new_state]
                    result = search(new_path, g + 1, threshold)
                    
                    if result == "FOUND":
                        return "FOUND"
                    if result < min_cost:
                        min_cost = result
                        
        return min_cost
    
    while True:
        result = search(path, 0, threshold)
        if result == "FOUND":
            return path
        if result == float('inf'):
            return None
        threshold = result

def simple_hill_climbing(start, goal, max_steps=1000):
    """Leo đồi đơn giản (Simple Hill Climbing)"""
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
            
        # Tìm trạng thái lân cận tốt nhất
        neighbors.sort()
        best_h, best_state = neighbors[0]
        
        if best_h >= current_h:  # Không cải thiện
            break
            
        current_state = best_state
        current_h = best_h
        path.append(current_state)
    
    return path

def steepest_hill_climbing(start, goal, max_steps=1000):
    """Leo đồi dốc đứng (Steepest-Ascent Hill Climbing)"""
    return simple_hill_climbing(start, goal, max_steps)  # Giống với leo đồi đơn giản trong trường hợp này

def stochastic_hill_climbing(start, goal, max_steps=1000):
    """Leo đồi ngẫu nhiên (Stochastic Hill Climbing)"""
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
        better_neighbors = [state for h, state in neighbors if h < current_h]
        if better_neighbors:
            current_state = random.choice(better_neighbors)
            current_h = manhattan_distance(current_state)
            path.append(current_state)
        else:
            break
    
    return path

def simulated_annealing(start, goal, max_steps=1000, initial_temp=1000, cooling_rate=0.99):
    """Mô phỏng luyện kim (Simulated Annealing)"""
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    temp = initial_temp  # Nhiệt độ ban đầu
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        temp *= cooling_rate  # Giảm nhiệt độ
        if temp < 0.1:
            break
            
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
            
        # Chọn ngẫu nhiên một trạng thái lân cận
        new_h, new_state = random.choice(neighbors)
        delta_e = current_h - new_h  # Độ chênh lệch
        
        # Chấp nhận trạng thái tốt hơn hoặc đôi khi trạng thái xấu hơn
        if delta_e > 0 or math.exp(delta_e / temp) > random.random():
            current_state = new_state
            current_h = new_h
            path.append(current_state)
    
    return path

def beam_search(start, goal, beam_width=2, max_steps=1000):
    """Tìm kiếm chùm (Beam Search)"""
    current_states = [(manhattan_distance(start), start, [start])]
    visited = set()
    
    for _ in range(max_steps):
        next_states = []
        
        for h, state, path in current_states:
            if state == goal:
                return path
                
            if state in visited:
                continue
                
            visited.add(state)
            blank_i, blank_j = find_blank(state)
            
            for di, dj in directions:
                ni, nj = blank_i + di, blank_j + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                    new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                    if new_state not in visited:
                        next_states.append((
                            manhattan_distance(new_state),
                            new_state,
                            path + [new_state]
                        ))
        
        if not next_states:
            break
            
        # Chỉ giữ lại beam_width trạng thái tốt nhất
        next_states.sort()
        current_states = next_states[:beam_width]
    
    # Trả về đường đi tốt nhất tìm được
    if current_states:
        return current_states[0][2]
    return None

def genetic_algorithm(start, goal, population_size=20, max_generations=100, mutation_rate=0.2):
    """Giải thuật di truyền cho bài toán 8-puzzle"""
    def generate_individual():
        """Tạo một cá thể bằng cách di chuyển ngẫu nhiên từ trạng thái bắt đầu"""
        individual = start
        path = [individual]
        steps = random.randint(5, 30)  # Số bước di chuyển ngẫu nhiên
        
        for _ in range(steps):
            blank_i, blank_j = find_blank(individual)
            possible_moves = []
            
            for di, dj in directions:
                ni, nj = blank_i + di, blank_j + dj
                if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                    new_state = swap_tiles(individual, blank_i, blank_j, ni, nj)
                    possible_moves.append(new_state)
            
            if possible_moves:
                individual = random.choice(possible_moves)
                path.append(individual)
            else:
                break
                
        return path
    
    def fitness(path):
        """Đánh giá độ thích nghi của một cá thể (khoảng cách nhỏ hơn thì tốt hơn)"""
        return -manhattan_distance(path[-1])  # Âm vì chúng ta muốn tối đa hóa
    
    # Khởi tạo quần thể
    population = [generate_individual() for _ in range(population_size)]
    
    for generation in range(max_generations):
        # Đánh giá độ thích nghi
        scored_pop = [(fitness(ind), ind) for ind in population]
        scored_pop.sort(reverse=True)
        
        # Kiểm tra giải pháp
        best_individual = scored_pop[0][1]
        if best_individual[-1] == goal:
            return best_individual
        
        # Chọn lọc - giữ lại nửa tốt nhất
        selected = [ind for score, ind in scored_pop[:population_size//2]]
        
        # Sinh sản
        new_population = selected.copy()
        
        while len(new_population) < population_size:
            # Chọn cha mẹ
            parent1, parent2 = random.choices(selected, k=2)
            
            # Lai ghép - kết hợp các phần của đường đi cha mẹ
            crossover_point = min(len(parent1), len(parent2)) // 2
            child = parent1[:crossover_point] + parent2[crossover_point:]
            
            # Đột biến - thỉnh thoảng thêm bước di chuyển ngẫu nhiên
            if random.random() < mutation_rate:
                last_state = child[-1]
                blank_i, blank_j = find_blank(last_state)
                possible_moves = []
                
                for di, dj in directions:
                    ni, nj = blank_i + di, blank_j + dj
                    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                        new_state = swap_tiles(last_state, blank_i, blank_j, ni, nj)
                        possible_moves.append(new_state)
                
                if possible_moves:
                    child.append(random.choice(possible_moves))
            
            new_population.append(child)
        
        population = new_population
    
    # Trả về cá thể tốt nhất tìm được
    best_individual = max([(fitness(ind), ind) for ind in population], key=lambda x: x[0])[1]
    return best_individual

def nondeterministic_search(start, goal, max_steps=1000):
    """Tìm kiếm với hành động không xác định (có thể thất bại với xác suất nào đó)"""
    current_state = start
    path = [current_state]
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        possible_moves = []
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                possible_moves.append((di, dj))
        
        if not possible_moves:
            break
            
        # Chọn một bước di chuyển ngẫu nhiên
        di, dj = random.choice(possible_moves)
        ni, nj = blank_i + di, blank_j + dj
        
        # Hành động thành công với xác suất 80%
        if random.random() < 0.8:
            current_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
            path.append(current_state)
        else:
            # Hành động thất bại - giữ nguyên trạng thái
            path.append(current_state)
    
    return path

def partial_observation_search(start, goal, max_steps=1000):
    """Tìm kiếm với quan sát một phần (chỉ nhìn thấy một phần trạng thái)"""
    # Agent chỉ nhìn thấy cửa sổ 2x2 xung quanh ô trống
    current_state = start
    path = [current_state]
    visited = set()
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        possible_moves = []
        
        # Xác định vùng nhìn thấy (2x2 quanh ô trống)
        visible_tiles = []
        for i in range(max(0, blank_i-1), min(GRID_SIZE, blank_i+2)):
            for j in range(max(0, blank_j-1), min(GRID_SIZE, blank_j+2)):
                visible_tiles.append((i, j, current_state[i][j]))
        
        # Agent chỉ nhìn thấy các ô trong vùng nhìn thấy
        # Nên phải đưa ra quyết định dựa trên thông tin hạn chế này
        
        # Chiến lược đơn giản: cố gắng di chuyển các ô về vị trí đích trong vùng nhìn thấy
        best_move = None
        best_score = float('-inf')
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                # Đánh giá chất lượng bước di chuyển dựa trên các ô nhìn thấy
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                
                # Tính điểm dựa trên số ô nhìn thấy đúng vị trí
                score = 0
                for i, j, value in visible_tiles:
                    if value != 0:
                        goal_row = (value - 1) // GRID_SIZE
                        goal_col = (value - 1) % GRID_SIZE
                        if (i, j) == (goal_row, goal_col):
                            score += 1
                
                if score > best_score:
                    best_score = score
                    best_move = (di, dj)
        
        if best_move:
            di, dj = best_move
            ni, nj = blank_i + di, blank_j + dj
            current_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
            path.append(current_state)
        else:
            break
    
    return path

# ========== VÒNG LẶP CHÍNH CỦA GAME ==========
def main():
    global selected_algorithm, path, step, solving_time, dragging, drag_start_pos, start_state
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Giới hạn FPS và xử lý sự kiện
        clock.tick(60)
        
        # Lấy trạng thái hiện tại để hiển thị
        current_state = path[step] if path and step < len(path) else start_state
        
        # Vẽ tất cả các thành phần UI
        draw_grid(current_state)
        buttons = draw_buttons()
        draw_info_panel(len(path)-1 if path else None, solving_time if selected_algorithm else None)
        
        # Vẽ nút đóng
        close_button = pygame.Rect(WIDTH - 50, 20, 30, 30)
        pygame.draw.rect(screen, (220, 70, 70), close_button, border_radius=5)
        close_text = button_font.render("×", True, TEXT_COLOR)
        screen.blit(close_text, (WIDTH - 42, 20))
        
        pygame.display.flip()
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Kiểm tra nút đóng
                if close_button.collidepoint(mouse_pos):
                    running = False
                    continue
                
                # Kiểm tra các nút thuật toán
                button_clicked = False
                for rect, algo in buttons:
                    if rect.collidepoint(mouse_pos):
                        button_clicked = True
                        if algo == "QUIT":
                            running = False
                        else:
                            selected_algorithm = algo
                            start_time = time.time()
                            
                            # Chạy thuật toán được chọn
                            try:
                                algorithm_map = {
                                    "A*": a_star,
                                    "BFS": bfs,
                                    "DFS": dfs,
                                    "Greedy": greedy,
                                    "UCS": ucs,
                                    "IDA*": ida_star_search,
                                    "IDDFS": iddfs,
                                    "SimpleH": simple_hill_climbing,
                                    "SteepH": steepest_hill_climbing,
                                    "StochHC": stochastic_hill_climbing,
                                    "SA": simulated_annealing,
                                    "Beam": beam_search,
                                    "Genetic": genetic_algorithm,
                                    "Nondet": nondeterministic_search,
                                    "PartialObs": partial_observation_search
                                }
                                path = algorithm_map[algo](start_state, goal_state)
                                solving_time = time.time() - start_time
                                
                                if path:
                                    print(f"{algo} found solution in {len(path)-1} steps ({solving_time:.3f}s)")
                                else:
                                    print(f"{algo} found no solution")
                                
                            except Exception as e:
                                print(f"Error with {algo}: {str(e)}")
                                path = None
                            
                            step = 0
                        break
                
                # Xử lý kéo ô nếu không có nút nào được nhấn
                if not button_clicked and not path:
                    grid_x = (mouse_pos[0] - GRID_OFFSET_X) // TILE_SIZE
                    grid_y = (mouse_pos[1] - GRID_OFFSET_Y) // TILE_SIZE
                    
                    if (0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE and 
                        current_state[grid_y][grid_x] != 0):
                        dragging = (grid_y, grid_x)
                        drag_start_pos = mouse_pos
            
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                mouse_pos = pygame.mouse.get_pos()
                blank_pos = find_blank(current_state)
                
                # Kiểm tra nếu ô được kéo đến vị trí trống liền kề
                if blank_pos and (
                    (abs(dragging[0] - blank_pos[0]) == 1 and dragging[1] == blank_pos[1]) or 
                    (abs(dragging[1] - blank_pos[1]) == 1 and dragging[0] == blank_pos[0])):
                    
                    start_state = swap_tiles(start_state, dragging[0], dragging[1], blank_pos[0], blank_pos[1])
                
                # Đặt lại trạng thái kéo và giải pháp
                dragging = None
                path = None
                step = 0
                solving_time = 0
                selected_algorithm = None
            
            elif event.type == pygame.MOUSEMOTION and dragging:
                # Có thể thêm hiệu ứng hình ảnh khi kéo ở đây
                pass
        
        # Tự động chuyển tiếp hoạt ảnh giải pháp
        if path and step < len(path) - 1:
            pygame.time.delay(STEP_DELAY)
            step += 1
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()