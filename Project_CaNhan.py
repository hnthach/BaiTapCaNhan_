import pygame
import sys
import heapq
from collections import deque
import time 
import random
random.seed(42)

import math

# ========== HẰNG SỐ ==========
WIDTH, HEIGHT = 1200, 800  
GRID_SIZE = 3              
TILE_SIZE = 150            
GRID_OFFSET_X = 150        
GRID_OFFSET_Y = 150        
FONT_SIZE = 50             
STEP_DELAY = 300           
BUTTON_HEIGHT = 40         
BUTTON_WIDTH = 200         
GROUP_BUTTON_WIDTH = 300
BUTTON_SPACING = 5         
BUTTON_START_X = 700       
BUTTON_START_Y = 150       
GROUP_SPACING = 18         
INFO_PANEL_HEIGHT = 60     
GROUP_BUTTON_HEIGHT = 55   

BACKGROUND_COLOR = (40, 40, 50)
TILE_COLORS = {
    1: (255, 100, 100), 2: (100, 255, 100), 3: (100, 100, 255),
    4: (255, 255, 100), 5: (255, 100, 255), 6: (100, 255, 255),
    7: (200, 150, 100), 8: (150, 200, 150), 0: (70, 70, 80)
}

GROUP_COLORS = {
    1: (80, 120, 200),    
    2: (80, 200, 120),    
    3: (200, 120, 80),    
    4: (200, 80, 200),   
    5: (200, 200, 80),    
    6: (120, 200, 200)    
}
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
INFO_PANEL_COLOR = (60, 60, 70)
INFO_BORDER_COLOR = (100, 100, 110)

# Trạng thái trò chơi
# (2, 6, 5), (8, 0, 7), (4, 3, 1)
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
start_state = ((2, 6, 5), (8, 0, 7), (4, 3, 1))
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#(2, 8, 3), (1, 6, 4), (7, 0, 5)

# ========== KHỞI TẠO ==========
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle AI Solver")

font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 72)
info_font = pygame.font.Font(None, 34)
group_font = pygame.font.Font(None, 36)

selected_algorithm = None  
path = None               
step = 0                  
solving_time = 0         
dragging = None           
drag_start_pos = None      
expanded_group = None     

# ========== HÀM TIỆN ÍCH ==========
def draw_grid(state):
    """Vẽ lưới puzzle với hiệu ứng hình ảnh"""
    screen.fill(BACKGROUND_COLOR)
    
    title = title_font.render("8-Puzzle AI Solver", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            rect = pygame.Rect(
                GRID_OFFSET_X + j * TILE_SIZE, 
                GRID_OFFSET_Y + i * TILE_SIZE, 
                TILE_SIZE, 
                TILE_SIZE
            )
            
            pygame.draw.rect(screen, SHADOW_COLOR, rect.inflate(6, 6), border_radius=10)
            pygame.draw.rect(screen, TILE_COLORS[value], rect, border_radius=8)
            
            if value != 0:
                text_shadow = font.render(str(value), True, SHADOW_COLOR)
                screen.blit(text_shadow, (rect.x + TILE_SIZE//3 + 2, rect.y + TILE_SIZE//4 + 2))
                text = font.render(str(value), True, TEXT_COLOR)
                screen.blit(text, (rect.x + TILE_SIZE//3, rect.y + TILE_SIZE//4))

def draw_buttons():
    """Vẽ các nút chọn thuật toán được tổ chức theo nhóm"""
    global selected_algorithm, expanded_group
    
    # Định nghĩa các nhóm thuật toán
    algorithm_groups = [
        {
            "id": 1,
            "name": "1. Uninformed Search",
            "algorithms": ["BFS", "DFS", "UCS", "IDDFS"],
            "expanded": expanded_group == 1
        },
        {
            "id": 2,
            "name": "2. Informed Search",
            "algorithms": ["A*", "IDA*", "Greedy"],
            "expanded": expanded_group == 2
        },
        {
            "id": 3,
            "name": "3. Local Search",
            "algorithms": ["SimpleH", "SteepH", "StochHC", "SA", "Beam", "Genetic"],
            "expanded": expanded_group == 3
        },
        {
            "id": 4,
            "name": "4. Complex Environments",
            "algorithms": ["Nondet", "PartialObs", "No_observation"],
            "expanded": expanded_group == 4
        },
        {
            "id": 5,
            "name": "5. CSPs",
            "algorithms": ["Backtracking", "ForwardCheck", "MinConflicts"],
            "expanded": expanded_group == 5
        },
        {
            "id": 6,
            "name": "6. Reinforcement Learning",
            "algorithms": ["Q-Learning"],
            "expanded": expanded_group == 6
        }
    ]
    
    buttons = []
    current_y = BUTTON_START_Y
    
    for group in algorithm_groups:
        group_color = GROUP_COLORS[group["id"]]
        
        group_rect = pygame.Rect(
            BUTTON_START_X,
            current_y,
            BUTTON_WIDTH * 2 + BUTTON_SPACING,
            GROUP_BUTTON_HEIGHT
        )
        
        pygame.draw.rect(screen, group_color, group_rect, border_radius=5)
        pygame.draw.rect(screen, (0, 0, 0), group_rect, 2, border_radius=5)
        
        group_text = group_font.render(group["name"], True, TEXT_COLOR)
        text_rect = group_text.get_rect(center=group_rect.center)
        screen.blit(group_text, text_rect)
        
        buttons.append((group_rect, f"GROUP_{group['id']}"))
        current_y += GROUP_BUTTON_HEIGHT + 5
        
        if group["expanded"]:
            num_columns = 2
            column_width = BUTTON_WIDTH
            
            for i, algo in enumerate(group["algorithms"]):
                col = i % num_columns
                row = i // num_columns
                
                rect = pygame.Rect(
                    BUTTON_START_X + col * (column_width + BUTTON_SPACING),
                    current_y + row * (BUTTON_HEIGHT + BUTTON_SPACING),
                    column_width,
                    BUTTON_HEIGHT
                )
                
                color = group_color
                if algo == selected_algorithm:
                    color = tuple(min(c + 40, 255) for c in color)
                
                pygame.draw.rect(screen, color, rect, border_radius=5)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=5)
                
                display_text = algo
                if algo == "SimpleH":
                    display_text = "Simple Hill"
                elif algo == "SteepH":
                    display_text = "Steepest Hill"
                elif algo == "StochHC":
                    display_text = "Stochastic Hill"
                elif algo == "SA":
                    display_text = "Simulated Annealing"
                elif algo == "Nondet":
                    display_text = "Nondeterministic"
                elif algo == "PartialObs":
                    display_text = "Partial Obs"
                elif algo == "No_observation":
                    display_text = "No Observation"
                elif algo == "ForwardCheck":
                    display_text = "Forward Check"
                elif algo == "MinConflicts":
                    display_text = "Min Conflicts"
                elif algo == "Q-Learning":
                    display_text = "Q-Learning"
                
                text_surf = button_font.render(display_text, True, TEXT_COLOR)
                text_rect = text_surf.get_rect(center=rect.center)
                screen.blit(text_surf, text_rect)
                
                buttons.append((rect, algo))
            
            current_y += (len(group["algorithms"]) + num_columns - 1) // num_columns * (BUTTON_HEIGHT + BUTTON_SPACING)
        
        current_y += GROUP_SPACING
    
    return buttons

def draw_info_panel(steps, time_elapsed):
    """Vẽ panel thông tin hiển thị số bước và thời gian"""
    panel_rect = pygame.Rect(GRID_OFFSET_X, GRID_OFFSET_Y + GRID_SIZE * TILE_SIZE + 20, 
                            GRID_SIZE * TILE_SIZE, INFO_PANEL_HEIGHT)
    
    pygame.draw.rect(screen, INFO_PANEL_COLOR, panel_rect, border_radius=10)
    pygame.draw.rect(screen, INFO_BORDER_COLOR, panel_rect, 2, border_radius=10)
    
    if steps is not None:
        steps_text = info_font.render(f"Steps: {steps}", True, (200, 230, 200))
        screen.blit(steps_text, (GRID_OFFSET_X + 20, GRID_OFFSET_Y + GRID_SIZE * TILE_SIZE + 35))
    
    if time_elapsed is not None:
        time_text = info_font.render(f"Time: {time_elapsed:.3f}s", True, (200, 200, 230))
        screen.blit(time_text, (GRID_OFFSET_X + GRID_SIZE * TILE_SIZE - time_text.get_width() - 20, 
                              GRID_OFFSET_Y + GRID_SIZE * TILE_SIZE + 35))

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
                goal_row = (value - 1) // GRID_SIZE  
                goal_col = (value - 1) % GRID_SIZE   
                distance += abs(i - goal_row) + abs(j - goal_col)  
    return distance

def is_solvable(state):
    """Kiểm tra trạng thái puzzle hiện tại có giải được không"""
    flat_state = [num for row in state for num in row if num != 0]
    inversions = 0  
    
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1
                
    return inversions % 2 == 0  

# ========== CÁC THUẬT TOÁN TÌM KIẾM ==========

# 1. Uninformed Search Algorithms
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
    """Depth-Limited DFS (không dùng visited để phù hợp với IDDFS)"""
    stack = [(start, [start], 0)]  
    
    while stack:
        state, path, depth = stack.pop()
        
        if state == goal:
            return path
            
        if depth >= max_depth:
            continue
            
        blank_i, blank_j = find_blank(state)
        
        for di, dj in reversed(directions):
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in path:  
                    stack.append((new_state, path + [new_state], depth + 1))
    return None

def iddfs(start, goal):
    """Iterative Deepening DFS (tối ưu cho 8-puzzle)"""
    depth = 0
    while True:
        result = dfs(start, goal, depth)
        if result is not None:  
            return result
        depth += 1
        if depth > 31: 
            return None

def ucs(start, goal):
    """Tìm kiếm chi phí đồng nhất (tối ưu hơn)"""
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

# 2. Informed Search Algorithms
def a_star(start, goal):
    priority_queue = [(0 + manhattan_distance(start), 0, start, [])]
    visited = set()
    
    while priority_queue:
        _, cost, state, path = heapq.heappop(priority_queue)
        
        if state == goal:
            return path + [state]
        
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
                        (new_cost + manhattan_distance(new_state), new_cost, new_state, path + [state])
                    )
    return None

def ida_star_search(start, goal):
    """Tìm kiếm A* lặp sâu (Iterative Deepening A*)"""
    def search(node, g, threshold, path):
        h = manhattan_distance(node)
        f = g + h
        
        if f > threshold:
            return (False, f) 
        if node == goal:
            return (True, path + [node])  
            
        min_cost = float('inf')
        blank_i, blank_j = find_blank(node)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_node = swap_tiles(node, blank_i, blank_j, ni, nj)
                if new_node not in path:
                    found, result = search(new_node, g + 1, threshold, path + [node])
                    if found:
                        return (True, result)
                    if result < min_cost:
                        min_cost = result
                        
        return (False, min_cost)
    
    threshold = manhattan_distance(start)
    
    while True:
        found, result = search(start, 0, threshold, [])
        
        if found:
            return result
        if result == float('inf'):
            return None
            
        threshold = result

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

# 3. Local Search Algorithms
def simple_hill_climbing(start, goal, max_steps=1000):
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    visited = set()  # Theo dõi các trạng thái đã thăm
    visited.add(current_state)
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        # Tạo các trạng thái kế cận chưa thăm
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    new_h = manhattan_distance(new_state)
                    neighbors.append((new_h, new_state))
        
        if not neighbors:
            break
            
        neighbors.sort()  # Sắp xếp theo heuristic
        
        # Chọn trạng thái tốt nhất chưa thăm
        for h, state in neighbors:
            if h <= current_h:  # Chấp nhận cả trạng thái ngang bằng
                current_state = state
                current_h = h
                path.append(current_state)
                visited.add(current_state)
                break
        else:
            # Nếu không có trạng thái tốt hơn, chọn ngẫu nhiên trong các trạng thái chưa thăm
            unvisited = [state for h, state in neighbors if state not in visited]
            if unvisited:
                current_state = random.choice(unvisited)
                current_h = manhattan_distance(current_state)
                path.append(current_state)
                visited.add(current_state)
            else:
                break
    
    return path

def steepest_hill_climbing(start, goal, max_steps=1000):
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    visited = set()
    visited.add(current_state)
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    new_h = manhattan_distance(new_state)
                    neighbors.append((new_h, new_state))
        
        if not neighbors:
            break
            
        neighbors.sort()
        best_h, best_state = neighbors[0]
        
        if best_h < current_h:
            current_state = best_state
            current_h = best_h
            path.append(current_state)
            visited.add(current_state)
        elif best_h == current_h:
            # Nếu bằng nhau, chọn ngẫu nhiên trong các trạng thái tốt nhất chưa thăm
            best_neighbors = [state for h, state in neighbors if h == best_h and state not in visited]
            if best_neighbors:
                current_state = random.choice(best_neighbors)
                path.append(current_state)
                visited.add(current_state)
            else:
                break
        else:
            # Nếu không có trạng thái tốt hơn, chọn ngẫu nhiên trong các trạng thái chưa thăm
            unvisited = [state for h, state in neighbors if state not in visited]
            if unvisited:
                current_state = random.choice(unvisited)
                current_h = manhattan_distance(current_state)
                path.append(current_state)
                visited.add(current_state)
            else:
                break
    
    return path

def stochastic_hill_climbing(start, goal, max_steps=1000):
    """Stochastic Hill Climbing với cơ chế thoát local optima"""
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    visited = set([current_state])  # Sử dụng set để lưu các trạng thái đã thăm
    stuck_count = 0
    max_stuck = 20  # Số bước kẹt tối đa trước khi áp dụng biện pháp thoát
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        # Tạo danh sách láng giềng hợp lệ
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    new_h = manhattan_distance(new_state)
                    neighbors.append((new_h, new_state))
        
        if not neighbors:
            break  # Không còn nước đi hợp lệ
            
        # Tách các láng giềng thành 2 nhóm: tốt hơn và xấu hơn
        improving = [(h, s) for h, s in neighbors if h < current_h]
        sideways = [(h, s) for h, s in neighbors if h == current_h]
        worsening = [(h, s) for h, s in neighbors if h > current_h]
        
        # Ưu tiên chọn từ các láng giềng tốt hơn
        if improving:
            # Tính trọng số (ưu tiên các bước cải thiện nhiều)
            weights = [1/(h+0.1) for h, s in improving]  # +0.1 để tránh chia cho 0
            total = sum(weights)
            if total > 0:
                probs = [w/total for w in weights]
                idx = random.choices(range(len(improving)), weights=probs)[0]
                current_h, current_state = improving[idx]
                path.append(current_state)
                visited.add(current_state)
                stuck_count = 0
                continue
        
        # Nếu không có láng giềng tốt hơn, xem xét đi ngang
        if sideways:
            current_h, current_state = random.choice(sideways)
            path.append(current_state)
            visited.add(current_state)
            stuck_count += 1
        else:
            stuck_count += 1
            
        # Nếu bị kẹt quá lâu, chấp nhận bước đi xấu hơn để thoát local optima
        if stuck_count > max_stuck and worsening:
            # Chọn ngẫu nhiên một bước đi xấu hơn
            current_h, current_state = random.choice(worsening)
            path.append(current_state)
            visited.add(current_state)
            stuck_count = 0
    
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
            
        next_states.sort()
        current_states = next_states[:beam_width]

    if current_states:
        return current_states[0][2]
    return None

def simulated_annealing(start, goal, max_steps=1000, initial_temp=1000, cooling_rate=0.99):
    """Mô phỏng luyện kim (Simulated Annealing) - Fixed version"""
    current_state = start
    current_h = manhattan_distance(current_state)
    path = [current_state]
    temp = initial_temp
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        temp *= cooling_rate
        if temp < 0.1:
            break
            
        blank_i, blank_j = find_blank(current_state)
        neighbors = []
        
        # Generate all possible neighbors
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                new_h = manhattan_distance(new_state)
                neighbors.append((new_h, new_state))
        
        if not neighbors:
            break
            
        # Randomly select a neighbor
        new_h, new_state = random.choice(neighbors)
        delta_e = current_h - new_h  # Energy difference
        
        # Always accept better moves, sometimes accept worse moves
        if delta_e > 0 or math.exp(delta_e / temp) > random.random():
            current_state = new_state
            current_h = new_h
            path.append(current_state)
    
    return path

def genetic_algorithm(start, goal, population_size=20, max_generations=100, mutation_rate=0.2):
    """Giải thuật di truyền cho bài toán 8-puzzle - Fixed version"""
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
        last_state = path[-1]
        return -manhattan_distance(last_state)  # Negative because we want to maximize
    
    # Khởi tạo quần thể
    population = [generate_individual() for _ in range(population_size)]
    
    for generation in range(max_generations):
        # Đánh giá độ thích nghi
        scored_pop = [(fitness(ind), ind) for ind in population]
        scored_pop.sort(reverse=True, key=lambda x: x[0])
        
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
            min_len = min(len(parent1), len(parent2))
            if min_len > 1:
                crossover_point = random.randint(1, min_len-1)
                child = parent1[:crossover_point] + parent2[crossover_point:]
            else:
                child = parent1 if random.random() < 0.5 else parent2
            
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

# 4. Complex Environments Algorithms
def nondeterministic_search(start, goal, max_steps=1000, max_failures=50):
    current_state = start
    path = [current_state]
    failures = 0
    
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
            
        di, dj = random.choice(possible_moves)
        ni, nj = blank_i + di, blank_j + dj
        
        if random.random() < 0.8:
            new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
            if new_state not in path[-10:]:
                current_state = new_state
                path.append(current_state)
                failures = 0
            else:
                failures += 1
        else:
            failures += 1
            if failures >= max_failures:
                break
    
    return path

def partial_observation_search(start, goal, max_steps=1000):
    current_state = [list(row) for row in start]
    path = [tuple(tuple(row) for row in current_state)]  
    
    for _ in range(max_steps):
        if tuple(tuple(row) for row in current_state) == goal:
            return path
        
        blank_i, blank_j = find_blank(current_state)
        
        visible_tiles = []
        for i in range(max(0, blank_i-1), min(GRID_SIZE, blank_i+2)):
            for j in range(max(0, blank_j-1), min(GRID_SIZE, blank_j+2)):
                visible_tiles.append((i, j, current_state[i][j]))
        
        possible_moves = []
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                possible_moves.append((di, dj, ni, nj))

        best_move = None
        best_improvement = -1
        
        for di, dj, ni, nj in possible_moves:
            tile_value = current_state[ni][nj]
            goal_row, goal_col = (tile_value - 1) // GRID_SIZE, (tile_value - 1) % GRID_SIZE
            
            current_dist = abs(ni - goal_row) + abs(nj - goal_col)
            new_dist = abs(blank_i - goal_row) + abs(blank_j - goal_col)
            improvement = current_dist - new_dist
            
            if improvement > best_improvement:
                best_improvement = improvement
                best_move = (di, dj, ni, nj)
        
        if best_improvement <= 0:
            if possible_moves:
                best_move = random.choice(possible_moves)
            else:
                break  

        if best_move:
            di, dj, ni, nj = best_move
            current_state[blank_i][blank_j], current_state[ni][nj] = current_state[ni][nj], current_state[blank_i][blank_j]
            new_state = tuple(tuple(row) for row in current_state)

            if len(path) < 2 or new_state != path[-2]:
                path.append(new_state)
            else:
                if possible_moves:
                    possible_moves.remove(best_move)
                    if possible_moves:
                        di, dj, ni, nj = random.choice(possible_moves)
                        current_state[blank_i][blank_j], current_state[ni][nj] = current_state[ni][nj], current_state[blank_i][blank_j]
                        path.append(tuple(tuple(row) for row in current_state))
    
    return path

def no_observation_search(start, goal, max_steps=1000):
    """Tìm kiếm trong môi trường không quan sát (phải ghi nhớ các bước đã đi)"""
    current_state = start
    path = [current_state]
    visited = set()
    visited.add(current_state)
    
    for _ in range(max_steps):
        if current_state == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        possible_moves = []
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    possible_moves.append((di, dj))
        
        if not possible_moves:
            if len(path) > 1:
                path.pop()
                current_state = path[-1]
                continue
            else:
                break
            
        di, dj = random.choice(possible_moves)
        ni, nj = blank_i + di, blank_j + dj
        new_state = swap_tiles(current_state, blank_i, blank_j, ni, nj)
        
        current_state = new_state
        path.append(new_state)
        visited.add(new_state)
    
    return path

# 5. CSP Algorithms
def backtracking_csp(start, goal):
    """Giải bài toán 8-puzzle như một CSP sử dụng backtracking"""
    def is_consistent(state):
        """Kiểm tra tính nhất quán của trạng thái"""
        numbers = [num for row in state for num in row if num != 0]
        return len(numbers) == len(set(numbers))
    
    def backtrack(state, path, visited):
        if state == goal:
            return path
            
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited:
                    visited.add(new_state)
                    result = backtrack(new_state, path + [new_state], visited)
                    if result is not None:
                        return result
                    visited.remove(new_state)
        return None
    
    return backtrack(start, [start], {start})

def backtracking_fc_csp(start, goal):
    """Backtracking với forward checking cho bài toán 8-puzzle"""
    def forward_check(state):
        """Kiểm tra các ràng buộc tương lai"""
        numbers = [num for row in state for num in row if num != 0]
        return len(numbers) == len(set(numbers))
    
    def backtrack(state, path, visited):
        if state == goal:
            return path
            
        blank_i, blank_j = find_blank(state)
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                new_state = swap_tiles(state, blank_i, blank_j, ni, nj)
                if new_state not in visited and forward_check(new_state):
                    visited.add(new_state)
                    result = backtrack(new_state, path + [new_state], visited)
                    if result is not None:
                        return result
                    visited.remove(new_state)
        return None
    
    return backtrack(start, [start], {start})

def min_conflicts_csp(start, goal, max_steps=1000):
    """Thuật toán Min-conflicts cho bài toán 8-puzzle"""
    current_state = [list(row) for row in start]
    path = [tuple(tuple(row) for row in current_state)]
    
    for _ in range(max_steps):
        if tuple(tuple(row) for row in current_state) == goal:
            return path
            
        blank_i, blank_j = find_blank(current_state)
        conflicts = []
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = current_state[i][j]
                if value != 0:
                    goal_row = (value - 1) // GRID_SIZE
                    goal_col = (value - 1) % GRID_SIZE
                    distance = abs(i - goal_row) + abs(j - goal_col)
                    if distance > 0:
                        conflicts.append((distance, i, j))
        
        if not conflicts:
            break
            
        conflicts.sort(reverse=True)
        _, conflict_i, conflict_j = conflicts[0]
        
        best_move = None
        best_improvement = -1
        
        for di, dj in directions:
            ni, nj = conflict_i + di, conflict_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE and current_state[ni][nj] == 0:
                goal_row = (current_state[conflict_i][conflict_j] - 1) // GRID_SIZE
                goal_col = (current_state[conflict_i][conflict_j] - 1) % GRID_SIZE
                current_dist = abs(conflict_i - goal_row) + abs(conflict_j - goal_col)
                new_dist = abs(ni - goal_row) + abs(nj - goal_col)
                improvement = current_dist - new_dist
                
                if improvement > best_improvement:
                    best_improvement = improvement
                    best_move = (ni, nj)
        
        if best_move:
            ni, nj = best_move
            current_state[ni][nj], current_state[conflict_i][conflict_j] = current_state[conflict_i][conflict_j], current_state[ni][nj]
            path.append(tuple(tuple(row) for row in current_state))
    
    return path

# 6. Reinforcement Learning Algorithm
def q_learning(start, goal, episodes=1000, max_steps=100, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995):
    """Q-Learning algorithm for 8-puzzle"""
    # Khởi tạo Q-table (dictionary để lưu Q-values)
    q_table = {}
    
    # Hàm để lấy Q-value từ Q-table
    def get_q_value(state, action):
        state_key = tuple(tuple(row) for row in state)
        if state_key not in q_table:
            q_table[state_key] = {}
        if action not in q_table[state_key]:
            q_table[state_key][action] = 0  # Khởi tạo Q-value mặc định
        return q_table[state_key][action]
    
    # Hàm để chọn action (epsilon-greedy)
    def choose_action(state, exploration_rate):
        blank_i, blank_j = find_blank(state)
        possible_actions = []
        
        for di, dj in directions:
            ni, nj = blank_i + di, blank_j + dj
            if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                possible_actions.append((di, dj))
        
        if not possible_actions:
            return None
            
        # Khám phá (chọn ngẫu nhiên)
        if random.random() < exploration_rate:
            return random.choice(possible_actions)
        # Khai thác (chọn action có Q-value cao nhất)
        else:
            q_values = [get_q_value(state, action) for action in possible_actions]
            max_q = max(q_values)
            best_actions = [action for action, q in zip(possible_actions, q_values) if q == max_q]
            return random.choice(best_actions)
    
    # Huấn luyện Q-learning
    for episode in range(episodes):
        current_state = [list(row) for row in start]
        path = [tuple(tuple(row) for row in current_state)]
        
        for step in range(max_steps):
            if tuple(tuple(row) for row in current_state) == goal:
                break
                
            blank_i, blank_j = find_blank(current_state)
            action = choose_action(current_state, exploration_rate)
            
            if action is None:
                break
                
            di, dj = action
            ni, nj = blank_i + di, blank_j + dj
            
            # Thực hiện action
            new_state = [row[:] for row in current_state]
            new_state[blank_i][blank_j], new_state[ni][nj] = new_state[ni][nj], new_state[blank_i][blank_j]
            
            # Tính reward
            if tuple(tuple(row) for row in new_state) == goal:
                reward = 100  # Phần thưởng lớn khi đạt mục tiêu
            else:
                # Phần thưởng dựa trên cải thiện heuristic
                old_h = manhattan_distance(current_state)
                new_h = manhattan_distance(new_state)
                reward = (old_h - new_h) * 0.1  # Scale down để tránh Q-values quá lớn
            
            # Cập nhật Q-value
            current_q = get_q_value(current_state, action)
            
            # Tìm Q-value tối đa cho state mới
            next_state_actions = []
            blank_i_new, blank_j_new = find_blank(new_state)
            for di_new, dj_new in directions:
                ni_new, nj_new = blank_i_new + di_new, blank_j_new + dj_new
                if 0 <= ni_new < GRID_SIZE and 0 <= nj_new < GRID_SIZE:
                    next_state_actions.append((di_new, dj_new))
            
            if next_state_actions:
                max_next_q = max([get_q_value(new_state, a) for a in next_state_actions])
            else:
                max_next_q = 0
                
            # Công thức Q-learning
            new_q = current_q + learning_rate * (reward + discount_factor * max_next_q - current_q)
            
            # Cập nhật Q-table
            state_key = tuple(tuple(row) for row in current_state)
            q_table[state_key][action] = new_q
            
            # Chuyển sang state mới
            current_state = new_state
            path.append(tuple(tuple(row) for row in current_state))
        
        # Giảm exploration rate
        exploration_rate = max(0.01, exploration_rate * exploration_decay)
    
    # Sau khi huấn luyện, tìm đường đi từ start đến goal
    current_state = [list(row) for row in start]
    path = [tuple(tuple(row) for row in current_state)]
    
    for _ in range(max_steps * 2):  # Cho phép nhiều bước hơn để đảm bảo tìm thấy goal
        if tuple(tuple(row) for row in current_state) == goal:
            break
            
        blank_i, blank_j = find_blank(current_state)
        action = choose_action(current_state, 0)  # Không khám phá, chỉ khai thác
        
        if action is None:
            break
            
        di, dj = action
        ni, nj = blank_i + di, blank_j + dj
        
        new_state = [row[:] for row in current_state]
        new_state[blank_i][blank_j], new_state[ni][nj] = new_state[ni][nj], new_state[blank_i][blank_j]
        
        current_state = new_state
        path.append(tuple(tuple(row) for row in current_state))
    
    return path

# ========== VÒNG LẶP CHÍNH CỦA GAME ==========
def main():
    global selected_algorithm, path, step, solving_time, dragging, drag_start_pos, start_state, expanded_group
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(60)
        
        current_state = path[step] if path and step < len(path) else start_state
        
        draw_grid(current_state)
        buttons = draw_buttons()
        draw_info_panel(len(path)-1 if path else None, solving_time if selected_algorithm else None)

        close_button = pygame.Rect(WIDTH - 50, 20, 30, 30)
        pygame.draw.rect(screen, (220, 70, 70), close_button, border_radius=5)
        close_text = button_font.render("×", True, TEXT_COLOR)
        screen.blit(close_text, (WIDTH - 42, 20))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if close_button.collidepoint(mouse_pos):
                    running = False
                    continue
                
                button_clicked = False
                for rect, algo in buttons:
                    if rect.collidepoint(mouse_pos):
                        button_clicked = True
                        
                        if algo.startswith("GROUP_"):
                            group_id = int(algo.split("_")[1])
                            expanded_group = group_id if expanded_group != group_id else None
                        else:
                            selected_algorithm = algo
                            start_time = time.time()
                            
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
                                    "PartialObs": partial_observation_search,
                                    "No_observation": no_observation_search,
                                    "Backtracking": backtracking_csp,
                                    "ForwardCheck": backtracking_fc_csp,
                                    "MinConflicts": min_conflicts_csp,
                                    "Q-Learning": q_learning
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
                
                if blank_pos and (
                    (abs(dragging[0] - blank_pos[0]) == 1 and dragging[1] == blank_pos[1]) or 
                    (abs(dragging[1] - blank_pos[1]) == 1 and dragging[0] == blank_pos[0])):
                    
                    start_state = swap_tiles(start_state, dragging[0], dragging[1], blank_pos[0], blank_pos[1])

                dragging = None
                path = None
                step = 0
                solving_time = 0
                selected_algorithm = None
            
            elif event.type == pygame.MOUSEMOTION and dragging:
                pass

        if path and step < len(path) - 1:
            pygame.time.delay(STEP_DELAY)
            step += 1
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()