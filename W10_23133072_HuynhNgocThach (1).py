import pygame
import sys
import heapq
from collections import deque
import time 
import random
import math

# ========== CONSTANTS ==========
WIDTH, HEIGHT = 600, 800
GRID_SIZE = 3
TILE_SIZE = 150
GRID_OFFSET_X = (WIDTH - GRID_SIZE * TILE_SIZE) // 2
GRID_OFFSET_Y = 80
FONT_SIZE = 60
STEP_DELAY = 300
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 130
BUTTON_SPACING = 10
BUTTON_START_Y = HEIGHT - 230
INFO_PANEL_HEIGHT = 60

# Colors
BACKGROUND_COLOR = (40, 40, 50)
TILE_COLORS = {
    1: (255, 100, 100), 2: (100, 255, 100), 3: (100, 100, 255),
    4: (255, 255, 100), 5: (255, 100, 255), 6: (100, 255, 255),
    7: (200, 150, 100), 8: (150, 200, 150), 0: (70, 70, 80)
}
BUTTON_COLORS = [
    (255, 50, 50), (80, 80, 80), (255, 200, 50), (50, 200, 100),
    (220, 220, 220), (100, 50, 200), (150, 100, 200), (200, 150, 100),
    (100, 200, 150), (150, 200, 200), (200, 100, 150), (150, 150, 200),
    (200, 50, 100), (200, 50, 50)
]
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
INFO_PANEL_COLOR = (60, 60, 70)
INFO_BORDER_COLOR = (100, 100, 110)

# Game states
goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
start_state = ((8, 6, 7), (2, 5, 4), (3, 0, 1)) 
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# ========== INITIALIZATION ==========
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle AI Solver")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, 32)
title_font = pygame.font.Font(None, 48)
info_font = pygame.font.Font(None, 34)

# Game variables
selected_algorithm = None
path = None
step = 0
solving_time = 0
dragging = None
drag_start_pos = None

# ========== HELPER FUNCTIONS ==========
def draw_grid(state):
    """Draw the puzzle grid with visual effects"""
    screen.fill(BACKGROUND_COLOR)
    
    # Draw title
    title = title_font.render("8-Puzzle AI Solver", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Draw tiles
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            rect = pygame.Rect(
                GRID_OFFSET_X + j * TILE_SIZE, 
                GRID_OFFSET_Y + i * TILE_SIZE, 
                TILE_SIZE, 
                TILE_SIZE
            )
            
            # Tile shadow effect
            pygame.draw.rect(screen, SHADOW_COLOR, rect.inflate(6, 6), border_radius=10)
            pygame.draw.rect(screen, TILE_COLORS[value], rect, border_radius=8)
            
            if value != 0:
                # Text with shadow effect
                text_shadow = font.render(str(value), True, SHADOW_COLOR)
                screen.blit(text_shadow, (rect.x + TILE_SIZE//3 + 2, rect.y + TILE_SIZE//4 + 2))
                text = font.render(str(value), True, TEXT_COLOR)
                screen.blit(text, (rect.x + TILE_SIZE//3, rect.y + TILE_SIZE//4))

def draw_buttons():
    """Draw algorithm selection buttons"""
    global selected_algorithm
    
    button_texts = ["A*", "BFS", "DFS", "Greedy", 
                   "UCS", "IDA*", "IDDFS", "SimpleH", 
                   "SteepH", "StochHC", "SA", "Beam",
                   "Genetic", "QUIT"]
    
    buttons = []
    buttons_per_row = 4
    
    # Calculate centered button positions
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
        
        # Button color (brighter when selected)
        color = BUTTON_COLORS[i]
        if text == selected_algorithm:
            color = tuple(min(c + 40, 255) for c in color)
        
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)
        
        # Button text (shorten if needed)
        display_text = text if len(text) <= 7 else text[:6] + "."
        text_surf = button_font.render(display_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
        
        buttons.append((rect, text))
    
    return buttons

def draw_info_panel(steps, time_elapsed):
    """Draw the information panel showing steps and time"""
    panel_rect = pygame.Rect(20, BUTTON_START_Y - INFO_PANEL_HEIGHT - 10, 
                            WIDTH - 40, INFO_PANEL_HEIGHT)
    
    # Panel background
    pygame.draw.rect(screen, INFO_PANEL_COLOR, panel_rect, border_radius=10)
    pygame.draw.rect(screen, INFO_BORDER_COLOR, panel_rect, 2, border_radius=10)
    
    # Steps information
    if steps is not None:
        steps_text = info_font.render(f"Steps: {steps}", True, (200, 230, 200))
        screen.blit(steps_text, (40, BUTTON_START_Y - INFO_PANEL_HEIGHT + 15))
    
    # Time information
    if time_elapsed is not None:
        time_text = info_font.render(f"Time: {time_elapsed:.3f}s", True, (200, 200, 230))
        screen.blit(time_text, (WIDTH - time_text.get_width() - 40, 
                              BUTTON_START_Y - INFO_PANEL_HEIGHT + 15))

def find_blank(state):
    """Find the position of the blank tile (0)"""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if state[i][j] == 0:
                return i, j
    return None

def swap_tiles(state, i1, j1, i2, j2):
    """Swap two tiles in the puzzle"""
    state_list = [list(row) for row in state]
    state_list[i1][j1], state_list[i2][j2] = state_list[i2][j2], state_list[i1][j1]
    return tuple(tuple(row) for row in state_list)

def manhattan_distance(state):
    """Calculate Manhattan distance heuristic"""
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
    """Check if the current puzzle state is solvable"""
    flat_state = [num for row in state for num in row if num != 0]
    inversions = 0
    
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1
                
    return inversions % 2 == 0

# ========== SEARCH ALGORITHMS ==========
def a_star(start, goal):
    """A* search algorithm"""
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
    """Breadth-First Search"""
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
    """Depth-First Search with depth limit"""
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
    """Iterative Deepening DFS"""
    depth = 0
    while True:
        result = dfs(start, goal, depth)
        if result is not None:
            return result
        depth += 1
        if depth > 100:  # Prevent infinite loop
            return None

def greedy(start, goal):
    """Greedy Best-First Search"""
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
    """Uniform Cost Search"""
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
    """Iterative Deepening A*"""
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
    """Simple Hill Climbing"""
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
            
        # Find the best neighbor
        neighbors.sort()
        best_h, best_state = neighbors[0]
        
        if best_h >= current_h:
            break
            
        current_state = best_state
        current_h = best_h
        path.append(current_state)
    
    return path

def steepest_hill_climbing(start, goal, max_steps=1000):
    """Steepest-Ascent Hill Climbing"""
    return simple_hill_climbing(start, goal, max_steps)  # Same as simple in our implementation

def stochastic_hill_climbing(start, goal, max_steps=1000):
    """Stochastic Hill Climbing"""
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
            
        # Randomly select a better neighbor
        better_neighbors = [state for h, state in neighbors if h < current_h]
        if better_neighbors:
            current_state = random.choice(better_neighbors)
            current_h = manhattan_distance(current_state)
            path.append(current_state)
        else:
            break
    
    return path

def simulated_annealing(start, goal, max_steps=1000, initial_temp=1000, cooling_rate=0.99):
    """Simulated Annealing"""
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
        delta_e = current_h - new_h
        
        # Accept better or sometimes worse solutions
        if delta_e > 0 or math.exp(delta_e / temp) > random.random():
            current_state = new_state
            current_h = new_h
            path.append(current_state)
    
    return path

def beam_search(start, goal, beam_width=2, max_steps=1000):
    """Beam Search"""
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
            
        # Keep only the best beam_width states
        next_states.sort()
        current_states = next_states[:beam_width]
    
    # Return best path found
    if current_states:
        return current_states[0][2]
    return None

def genetic_algorithm(start, goal, population_size=20, max_generations=100, mutation_rate=0.2):
    """Genetic Algorithm for 8-puzzle"""
    def generate_individual():
        """Create an individual by making random moves from start state"""
        individual = start
        path = [individual]
        steps = random.randint(5, 30)  # Random number of moves
        
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
        """Evaluate fitness of an individual (lower distance is better)"""
        return -manhattan_distance(path[-1])  # Negative because we want to maximize
    
    # Initialize population
    population = [generate_individual() for _ in range(population_size)]
    
    for generation in range(max_generations):
        # Evaluate fitness
        scored_pop = [(fitness(ind), ind) for ind in population]
        scored_pop.sort(reverse=True)
        
        # Check for solution
        best_individual = scored_pop[0][1]
        if best_individual[-1] == goal:
            return best_individual
        
        # Selection - keep top half
        selected = [ind for score, ind in scored_pop[:population_size//2]]
        
        # Reproduction
        new_population = selected.copy()
        
        while len(new_population) < population_size:
            # Choose parents
            parent1, parent2 = random.choices(selected, k=2)
            
            # Crossover - combine parts of parent paths
            crossover_point = min(len(parent1), len(parent2)) // 2
            child = parent1[:crossover_point] + parent2[crossover_point:]
            
            # Mutation - sometimes add a random move
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
    
    # Return best individual found
    best_individual = max([(fitness(ind), ind) for ind in population], key=lambda x: x[0])[1]
    return best_individual

# ========== MAIN GAME LOOP ==========
def main():
    global selected_algorithm, path, step, solving_time, dragging, drag_start_pos, start_state
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Limit FPS and handle events
        clock.tick(60)
        
        # Get current state to display
        current_state = path[step] if path and step < len(path) else start_state
        
        # Draw all UI elements
        draw_grid(current_state)
        buttons = draw_buttons()
        draw_info_panel(len(path)-1 if path else None, solving_time if selected_algorithm else None)
        
        # Draw close button
        close_button = pygame.Rect(WIDTH - 50, 20, 30, 30)
        pygame.draw.rect(screen, (220, 70, 70), close_button, border_radius=5)
        close_text = button_font.render("×", True, TEXT_COLOR)
        screen.blit(close_text, (WIDTH - 42, 20))
        
        pygame.display.flip()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check close button
                if close_button.collidepoint(mouse_pos):
                    running = False
                    continue
                
                # Check algorithm buttons
                button_clicked = False
                for rect, algo in buttons:
                    if rect.collidepoint(mouse_pos):
                        button_clicked = True
                        if algo == "QUIT":
                            running = False
                        else:
                            selected_algorithm = algo
                            start_time = time.time()
                            
                            # Run selected algorithm
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
                                    "Genetic": genetic_algorithm
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
                
                # Handle tile dragging if no button was clicked
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
                
                # Check if tile was dragged to adjacent blank space
                if blank_pos and (
                    (abs(dragging[0] - blank_pos[0]) == 1 and dragging[1] == blank_pos[1]) or 
                    (abs(dragging[1] - blank_pos[1]) == 1 and dragging[0] == blank_pos[0])):
                    
                    start_state = swap_tiles(start_state, dragging[0], dragging[1], blank_pos[0], blank_pos[1])
                
                # Reset dragging and solution
                dragging = None
                path = None
                step = 0
                solving_time = 0
                selected_algorithm = None
            
            elif event.type == pygame.MOUSEMOTION and dragging:
                # Could add visual feedback for dragging here
                pass
        
        # Auto-advance solution animation
        if path and step < len(path) - 1:
            pygame.time.delay(STEP_DELAY)
            step += 1
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()