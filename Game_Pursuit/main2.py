import json
import time
import pygame
import random
import heapq
from heapq import heappush, heappop
import math
from collections import deque
import cv2
import os
import platform
import subprocess
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

current_map_index = 0

# Từ điển lưu dữ liệu hiệu suất
performance_data = {
    'BFS': {'states': 0, 'time': 0.0},
    'A*': {'states': 0, 'time': 0.0},
    'Beam Search': {'states': 0, 'time': 0.0},
    'AND-OR Tree': {'states': 0, 'time': 0.0},
    'Forward-Checking': {'states': 0, 'time': 0.0},
    'Q-Learning': {'states': 0, 'time': 0.0}
}

video_path = os.path.abspath("asset/anh_background/background1.mp4")
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Không thể mở video tại {video_path}")
else:
    print(f"Video mở thành công: {video_path}")

# Khởi tạo Pygame
pygame.init()

# Thiết lập cửa sổ game
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
MAZE_WIDTH = GRID_WIDTH * GRID_SIZE
MAZE_HEIGHT = GRID_HEIGHT * GRID_SIZE
option_font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pursuit Game")

# Tính toán tọa độ để căn giữa mê cung
MAZE_OFFSET_X = (WINDOW_WIDTH - MAZE_WIDTH) // 2
MAZE_OFFSET_Y = (WINDOW_HEIGHT - MAZE_HEIGHT) // 2

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GREEN = (150, 255, 150)
YELLOW = (255, 255, 0)
DARK_RED = (150, 0, 0)
DARK_BLUE = (20, 20, 50)
GREEN = (0, 255, 0)
xanhnhat = (150, 255, 150)
hongdam = (255, 20, 149)
hongnhat = (253, 38, 252)

# Thiết lập FPS
clock = pygame.time.Clock()
FPS = 60

# Tải font chữ
try:
    font = pygame.font.Font("freesansbold.ttf", 20)
    font_large = pygame.font.Font("freesansbold.ttf", 40)
    font_small = pygame.font.Font("freesansbold.ttf", 18)
except:
    font = pygame.font.Font(None, 20)
    font_large = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 18)

# Tạo lưới
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Định nghĩa các bản đồ
MAPS = {
    "Me cung": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    ]
}

def draw_grid(exit_pos=None):
    try:
        spike_img = pygame.image.load(r"asset\anh_icon\bay.png").convert_alpha()
        spike_img = pygame.transform.scale(spike_img, (GRID_SIZE - 5, GRID_SIZE - 5))
    except Exception as e:
        print(f"Không thể tải hình ảnh gai: {e}")
        spike_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
        pygame.draw.rect(spike_img, RED, (0, 0, GRID_SIZE - 5, GRID_SIZE - 5))

    pygame.draw.rect(screen, DARK_GRAY, (MAZE_OFFSET_X, MAZE_OFFSET_Y, MAZE_WIDTH, MAZE_HEIGHT), 3)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(MAZE_OFFSET_X + x * GRID_SIZE, MAZE_OFFSET_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if grid[y][x] == 1:
                pass  # Tường không vẽ (do đã có WALL_TEXTURE)
            elif grid[y][x] == 2:  # Lối ra
                pygame.draw.rect(screen, YELLOW, rect)
                screen.blit(door_img, (rect.x + 2.5, rect.y + 2.5))
                pygame.draw.rect(screen, BLACK, rect, 1)
            elif grid[y][x] == 6:  # Gai
                pygame.draw.rect(screen, xanhnhat, rect)  # Nền ô gai
                screen.blit(spike_img, (rect.x + 2.5, rect.y + 2.5))
                pygame.draw.rect(screen, BLACK, rect, 1)
            else:
                pygame.draw.rect(screen, xanhnhat, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Tải bản đồ
def load_map(map_name):
    global grid
    grid = [row[:] for row in MAPS[map_name]]

# Lấy vị trí trống
def get_empty_position():
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if grid[y][x] == 0:
            return (x, y)

# Hàm tìm vị trí lối ra
def get_exit_position():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 2:
                return (x, y)
    return None

# Chuyển đổi tọa độ
def to_grid_pos(x, y):
    return ((x - MAZE_OFFSET_X) // GRID_SIZE, (y - MAZE_OFFSET_Y) // GRID_SIZE)

def to_pixel_pos(grid_x, grid_y):
    return (MAZE_OFFSET_X + grid_x * GRID_SIZE + GRID_SIZE // 2, MAZE_OFFSET_Y + grid_y * GRID_SIZE + GRID_SIZE // 2)

def spawn_spikes(grid, enemy_pos, exit_pos, num_spikes=5):
    spike_positions = []
    for _ in range(num_spikes):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        while (grid[y][x] != 0 or (x, y) == enemy_pos or (x, y) == exit_pos or
               (x, y) in spike_positions):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
        grid[y][x] = 6  # Gai có giá trị 6 trên lưới
        spike_positions.append((x, y))
        print(f"Đặt gai tại: ({x}, {y})")
    return grid


# Thuật toán
def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        next_x, next_y = x + dx, y + dy
        next_pos = (next_x, next_y)
        if (0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and
            grid[next_y][next_x] != 1 and grid[next_y][next_x] != 6):  # Loại bỏ ô gai
            neighbors.append(next_pos)
    return neighbors

def bfs_search(start, goal):
    queue = deque([start])
    came_from = {start: None}
    visited = {start}
    states_explored = 1

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        neighbors = get_neighbors(current)
        for next_pos in neighbors:
            if next_pos not in visited:
                queue.append(next_pos)
                visited.add(next_pos)
                came_from[next_pos] = current
                states_explored += 1

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], states_explored
    path.append(start)
    path.reverse()

    for x, y in path:
        if grid[y][x] == 1:
            return [], states_explored
    return path, states_explored

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    states_explored = 1

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break
        neighbors = get_neighbors(current)
        for next_pos in neighbors:
            new_cost = cost_so_far[current] + 1
            states_explored += 1
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], states_explored
    path.append(start)
    path.reverse()
    for x, y in path:
        if grid[y][x] == 1:
            return [], states_explored
    return path, states_explored

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def beam_search(start, goal):
    beam_width = 10
    current_states = [(manhattan_distance(start, goal), start, [start])]
    states_explored = 1
    step = 0

    while current_states and step < 100:
        new_states = []
        for _, current_pos, path in current_states:
            if current_pos == goal:
                return path, states_explored
            neighbors = get_neighbors(current_pos)
            for neighbor in neighbors:
                if neighbor in path:
                    continue
                new_path = path + [neighbor]
                heuristic = manhattan_distance(neighbor, goal)
                new_states.append((heuristic, neighbor, new_path))
                states_explored += 1

        new_states.sort(key=lambda x: x[0])
        current_states = new_states[:beam_width]
        step += 1

    print(f"Beam Search failed to find a path to goal after {step} steps.")
    return [], states_explored

def and_or_tree_search(start, goal):
    queue = deque([(start, [start])])
    visited = set()
    states_explored = 1

    while queue:
        state, path = queue.popleft()
        position = state
        if position in visited:
            continue
        visited.add(position)
        if position == goal:
            return path, states_explored

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        possible_moves = []

        for dx, dy in directions:
            for steps in range(1, 4):
                next_x = position[0] + dx * steps
                next_y = position[1] + dy * steps
                next_pos = (next_x, next_y)
                valid = True
                if not (0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and grid[next_y][next_x] != 1):
                    valid = False
                else:
                    for s in range(1, steps):
                        check_x = position[0] + dx * s
                        check_y = position[1] + dy * s
                        if not (0 <= check_x < GRID_WIDTH and 0 <= check_y < GRID_HEIGHT and grid[check_y][check_x] != 1 and grid[check_y][check_x] != 6):
                            valid = False
                            break

                if valid and next_pos not in visited and next_pos not in path:
                    prob = random.random()
                    if steps == 1 and prob < 0.95:
                        possible_moves.append((next_pos, steps))
                    elif steps == 2 and prob < 0.98:
                        possible_moves.append((next_pos, steps))
                    elif steps == 3 and prob < 1.0:
                        possible_moves.append((next_pos, steps))

        states_explored += len(possible_moves)
        possible_moves.sort(key=lambda move: manhattan_distance(move[0], goal))

        for next_pos, steps in possible_moves:
            new_path = path + [next_pos]
            queue.append((next_pos, new_path))

    print(f"AND-OR Tree Search failed to find a path to goal.")
    return [], states_explored



def can_reach_goal(pos, goal, visited, states_explored_ref):
    frontier = [(heuristic(pos, goal), pos)]
    cost_so_far = {pos: 0}
    max_steps = 1000

    steps = 0
    while frontier:
        steps += 1
        if steps > max_steps:
            return False

        _, current = heapq.heappop(frontier)
        if current == goal:
            return True

        neighbors = get_neighbors(current)
        for next_pos in neighbors:
            if next_pos in visited:
                continue
            new_cost = cost_so_far[current] + 1
            if new_cost < cost_so_far.get(next_pos, float('inf')):
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                heappush(frontier, (priority, next_pos))
                states_explored_ref[0] += 1

    return False

def forward_checking_search(start, goal):
    def backtrack(path, depth):
        nonlocal states_explored
        if depth >= 100:
            return [], False
        if path[-1] == goal:
            return path, True
        current = path[-1]
        neighbors = get_neighbors(current)
        neighbors.sort(key=lambda pos: heuristic(pos, goal))
        visited = set(path)
        for next_pos in neighbors:
            if next_pos in path:
                continue
            can_reach = can_reach_goal(next_pos, goal, visited, states_explored)
            states_explored[0] += 1
            if can_reach:
                path.append(next_pos)
                result_path, success = backtrack(path, depth + 1)
                if success:
                    return result_path, True
                path.pop()

        return [], False

    states_explored = [0]
    path = [start]
    path, success = backtrack(path, 0)
    if not success:
        print(f"Backtracking Search with Forward Checking failed to find a path to goal.")
        return [], states_explored[0]
    for x, y in path:
        if grid[y][x] == 1:
            return [], states_explored[0]
    return path, states_explored[0]

q_table = {}
epsilon = 0.2

def get_action_from_direction(dx, dy):
    if dx == 0 and dy == -1:
        return 0
    elif dx == 0 and dy == 1:
        return 1
    elif dx == 1 and dy == 0:
        return 2
    elif dx == -1 and dy == 0:
        return 3
    return None

def get_direction_from_action(action):
    if action == 0:
        return 0, -1
    elif action == 1:
        return 0, 1
    elif action == 2:
        return 1, 0
    elif action == 3:
        return -1, 0
    return 0, 0

def q_learning_search(start, goal, max_episodes=100, max_steps=100):
    global epsilon
    alpha = 0.2
    gamma = 0.9
    epsilon = 0.3
    states_explored = 0
    best_states_explored = float('inf')
    no_improvement_count = 0
    convergence_threshold = 0.1

    for episode in range(max_episodes):
        current_pos = start
        max_delta = 0
        episode_states_explored = 0
        epsilon = max(0.05, epsilon * 0.995)

        for step in range(max_steps):
            state = (current_pos[0], current_pos[1])
            if state not in q_table:
                q_table[state] = {a: 0.0 for a in range(4)}

            if random.random() < epsilon:
                action = random.randint(0, 3)
            else:
                action = max(q_table[state], key=q_table[state].get)

            dx, dy = get_direction_from_action(action)
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)
            neighbors = get_neighbors(current_pos)

            if next_pos not in neighbors:
                reward = -10
                next_pos = current_pos
            else:
                distance_before = manhattan_distance(current_pos, goal)
                distance_after = manhattan_distance(next_pos, goal)
                reward = -0.5 + (distance_before - distance_after) * 5
                if next_pos == goal:
                    reward = 100

            next_state = (next_pos[0], next_pos[1])
            if next_state not in q_table:
                q_table[next_state] = {a: 0.0 for a in range(4)}

            old_value = q_table[state][action]
            max_future_q = max(q_table[next_state].values())
            q_table[state][action] = old_value + alpha * (reward + gamma * max_future_q - old_value)
            max_delta = max(max_delta, abs(old_value - q_table[state][action]))

            states_explored += 1
            episode_states_explored += 1
            current_pos = next_pos

            if current_pos == goal:
                break

        if max_delta < convergence_threshold:
            print(f"Q-Learning converged after {episode + 1} episodes")
            break

        if episode_states_explored >= best_states_explored:
            no_improvement_count += 1
        else:
            best_states_explored = episode_states_explored
            no_improvement_count = 0

        if no_improvement_count >= 30:
            print(f"Q-Learning stopped after {episode + 1} episodes due to no improvement")
            break

    path = [start]
    current_pos = start
    visited = set([start])
    steps = 0
    while current_pos != goal and steps < max_steps:
        state = (current_pos[0], current_pos[1])
        if state not in q_table:
            break
        action = max(q_table[state], key=q_table[state].get)
        dx, dy = get_direction_from_action(action)
        next_pos = (current_pos[0] + dx, current_pos[1] + dy)
        if next_pos not in get_neighbors(current_pos) or next_pos in visited:
            break
        visited.add(next_pos)
        path.append(next_pos)
        current_pos = next_pos
        steps += 1

    return path, states_explored

# Class xử lý quái vật
class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, algorithm):
        super().__init__()
        self.algorithm = algorithm
        self.color_map = {
            'BFS': BLUE,
            'A*': YELLOW,
            'Beam Search': RED,
            'AND-OR Tree': GREEN,
            'Forward-Checking': RED,
            'Q-Learning': hongnhat
        }
        self.color = self.color_map.get(algorithm, RED)

        try:
            self.image = pygame.image.load("asset/skin/kethu3.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (28, 28))
            tint_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint_surface.fill((*self.color, 192))
            self.image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            print(f"Tinted {algorithm} enemy with color: {self.color}")
        except Exception as e:
            print(f"Failed to load kethu3.png, using fallback for {algorithm}: {e}")
            self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
            pygame.draw.circle(self.image, self.color, (14, 14), 14)
            pygame.draw.circle(self.image, BLACK, (12, 12), 3)
            pygame.draw.circle(self.image, BLACK, (16, 12), 3)

        self.rect = self.image.get_rect(center=to_pixel_pos(grid_x, grid_y))
        self.grid_pos = [grid_x, grid_y]
        self.pixel_pos = list(to_pixel_pos(grid_x, grid_y))
        self.speed = 90
        self.default_speed = 90
        self.path = []
        self.last_path = []
        self.target_pixel_pos = self.pixel_pos[:]
        self.moving = False
        self.path_update_timer = 0
        self.path_update_interval = FPS // 5

        label_map = {
            'BFS': 'BFS',
            'A*': 'A*',
            'Beam Search': 'BS',
            'AND-OR Tree': 'AOT',
            'Forward-Checking': 'FC',
            'Q-Learning': 'QL'
        }
        self.label_text = label_map.get(self.algorithm, self.algorithm)  # Lưu label_text
        try:
            label_font = pygame.font.Font("freesansbold.ttf", 14)
        except:
            label_font = pygame.font.Font(None, 14)

        def render_text_with_outline(text, font, text_color, outline_color):
            text_surface = font.render(text, True, text_color)
            outline_surface = font.render(text, True, outline_color)
            surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2), (2, -2), (-2, 2)]:
                surface.blit(outline_surface, (dx + 2, dy + 2))
            surface.blit(text_surface, (2, 2))
            return surface

        self.label_surface = render_text_with_outline(self.label_text, label_font, WHITE, BLACK)
        self.label_rect = self.label_surface.get_rect()
        self.label_offset_y = -20

    def update(self):
        delta_time = clock.get_time() / 1000.0
        self.path_update_timer += 1
        if self.path_update_timer >= self.path_update_interval and not self.moving:
            self.path_update_timer = 0
            target_pos = get_exit_position()
            results = choose_algorithm(tuple(self.grid_pos), target_pos, self.algorithm, is_special_mode=True)
            algorithms = ['BFS', 'A*', 'Beam Search', 'AND-OR Tree', 'Forward-Checking', 'Q-Learning']
            self.path, _ = results[algorithms.index(self.algorithm)]

            if self.path and len(self.path) > 1:
                self.last_path = self.path[:]
                next_grid_pos = self.path[1]
                x, y = next_grid_pos
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1 and grid[y][x] != 6:
                    self.target_pixel_pos = list(to_pixel_pos(next_grid_pos[0], next_grid_pos[1]))
                    self.moving = True
                else:
                    self.path = self.last_path[:] if self.last_path else [self.grid_pos]
                    self.moving = False
            else:
                neighbors = get_neighbors(tuple(self.grid_pos))  # get_neighbors đã loại ô gai
                if neighbors:
                    next_pos = random.choice(neighbors)
                    self.path = [self.grid_pos[:], list(next_pos)]
                    self.target_pixel_pos = list(to_pixel_pos(next_pos[0], next_pos[1]))
                    self.moving = True
                    print(f"{self.algorithm} di chuyển ngẫu nhiên đến: {next_pos}")
                else:
                    self.moving = False

        if self.moving and len(self.path) > 1:
            dx = self.target_pixel_pos[0] - self.pixel_pos[0]
            dy = self.target_pixel_pos[1] - self.pixel_pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            speed = self.speed * delta_time
            epsilon = 1.0

            if distance > epsilon:
                if abs(dx) > abs(dy):
                    speed_x = speed if dx > 0 else -speed
                    speed_y = 0
                else:
                    speed_x = 0
                    speed_y = speed if dy > 0 else -speed

                if abs(speed_x) > abs(dx):
                    speed_x = dx
                if abs(speed_y) > abs(dy):
                    speed_y = dy

                self.pixel_pos[0] += speed_x
                self.pixel_pos[1] += speed_y
            else:
                self.pixel_pos = self.target_pixel_pos[:]
                next_grid_pos = self.path[1]
                x, y = next_grid_pos
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1:
                    self.grid_pos = list(next_grid_pos)
                    self.path.pop(0)
                    self.moving = False
                else:
                    self.path = [self.grid_pos[:]]
                    self.moving = False

            self.rect.center = (int(self.pixel_pos[0]), int(self.pixel_pos[1]))
            self.label_rect.center = (self.rect.centerx, self.rect.top + self.label_offset_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.label_surface, self.label_rect)
        print(f"Drawing {self.algorithm} enemy at {self.rect.center} with label: {self.label_text}")

# Lưu thông tin, hiện file, biểu đồ cho thuật toán
algorithm_runs = []
recorded_algorithms = set()

def choose_algorithm(start, goal, selected_algorithm, is_special_mode=False):
    global performance_data, current_map_index, algorithm_runs
    algorithms = ['BFS', 'A*', 'Beam Search', 'AND-OR Tree', 'Forward-Checking', 'Q-Learning']
    results = []

    for algorithm in algorithms:
        start_time = time.perf_counter()
        if algorithm == 'BFS':
            path, states_explored = bfs_search(start, goal)
        elif algorithm == 'A*':
            path, states_explored = a_star_search(start, goal)
        elif algorithm == 'Beam Search':
            path, states_explored = beam_search(start, goal)
        elif algorithm == 'AND-OR Tree':
            path, states_explored = and_or_tree_search(start, goal)
        elif algorithm == 'Forward-Checking':
            path, states_explored = forward_checking_search(start, goal)
        elif algorithm == 'Q-Learning':
            path, states_explored = q_learning_search(start, goal)
        end_time = time.perf_counter()
        runtime_ms = (end_time - start_time) * 1000

        run_info = {
            'algorithm': algorithm,
            'map_index': current_map_index,
            'steps': len(path),
            'runtime_ms': runtime_ms,
            'path': path,
            'states_explored': states_explored
        }
        algorithm_runs.append(run_info)
        performance_data[algorithm]['states'] = states_explored
        performance_data[algorithm]['time'] = runtime_ms
        print(f"Special Mode: Recorded {algorithm} with states: {states_explored}, time: {runtime_ms:.2f} ms")
        results.append((path, states_explored))

    return results

def custom_ylim(data):
    max_value = max(data) if data else 1
    upper_limit = max(max_value * 1.1, 0.01)
    return upper_limit


def plot_comparison(mode='Special Mode'):
    global algorithm_runs
    print("Algorithm runs:", algorithm_runs)

    algorithms = ['BFS', 'A*', 'Beam Search', 'AND-OR Tree', 'Forward-Checking', 'Q-Learning']

    # Lọc lần đầu tiên của mỗi thuật toán
    seen_algorithms = set()
    first_runs = []
    for run in algorithm_runs:
        if run['algorithm'] not in seen_algorithms:
            first_runs.append(run)
            seen_algorithms.add(run['algorithm'])

    # Sắp xếp first_runs theo thứ tự algorithms
    filtered_algorithms = [algo for algo in algorithms if algo in seen_algorithms]
    first_runs = sorted(first_runs, key=lambda x: algorithms.index(x['algorithm']))

    # Dữ liệu cho biểu đồ
    states_explored = [run['states_explored'] for run in first_runs]
    runtimes = [run['runtime_ms'] for run in first_runs]

    # Tạo DataFrame để dễ xử lý
    data = pd.DataFrame({
        'Algorithm': filtered_algorithms,
        'States Explored': states_explored,
        'Runtime (ms)': runtimes
    })

    # Tạo subplot với 2 hàng, 1 cột
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Number of States Explored', 'Runtime'),
        vertical_spacing=0.15
    )

    # Biểu đồ 1: Số trạng thái được khám phá
    fig.add_trace(
        go.Bar(
            x=data['Algorithm'],
            y=data['States Explored'],
            name='States Explored',
            marker_color='skyblue',
            text=data['States Explored'],
            textposition='outside',
            texttemplate='%{text}',
            hovertemplate='Algorithm: %{x}<br>States Explored: %{y}<extra></extra>'
        ),
        row=1, col=1
    )

    # Biểu đồ 2: Thời gian chạy
    fig.add_trace(
        go.Bar(
            x=data['Algorithm'],
            y=data['Runtime (ms)'],
            name='Runtime (ms)',
            marker_color='lightcoral',
            text=data['Runtime (ms)'].round(2),
            textposition='outside',
            texttemplate='%{text:.2f}',
            hovertemplate='Algorithm: %{x}<br>Runtime: %{y:.2f} ms<extra></extra>'
        ),
        row=2, col=1
    )

    # Tùy chỉnh layout
    def custom_ylim(data):
        max_value = max(data) if data else 1
        upper_limit = max(max_value * 1.1, 0.01)
        return upper_limit

    fig.update_yaxes(
        title_text='States Explored',
        range=[0, custom_ylim(states_explored)],
        row=1, col=1
    )
    fig.update_yaxes(
        title_text='Time (ms)',
        range=[0, custom_ylim(runtimes)],
        row=2, col=1
    )

    fig.update_xaxes(
        title_text='Algorithm',
        tickangle=0,
        row=2, col=1
    )
    for i, annotation in enumerate(fig.layout.annotations):
        if i == 0:  # Tiêu đề của biểu đồ 1 ("Number of States Explored")
            annotation.y = 1  # Đẩy tiêu đề lên cao hơn
        elif i == 1:  # Tiêu đề của biểu đồ 2 ("Runtime")
            annotation.y = 0.48  # Giữ nguyên

    fig.update_layout(
        height=920,
        width=1000,
        showlegend=False,
        title_text='Algorithm Performance Comparison',
        title_x=0.5,
        margin=dict(t=100, b=100, l=50, r=50),
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Hiển thị biểu đồ
    fig.show()

def save_algorithm_info_to_file(filename="algorithm_performance.txt", mode='Special Mode'):
    global algorithm_runs
    try:
        # Lọc lần đầu tiên của mỗi thuật toán
        seen_algorithms = set()
        first_runs = []
        for run in algorithm_runs:
            if run['algorithm'] not in seen_algorithms:
                first_runs.append(run)
                seen_algorithms.add(run['algorithm'])

        with open(filename, 'w') as f:
            f.write("Algorithm Performance Report \n")
            f.write("=======================================\n\n")
            for run in first_runs:
                f.write(f"Algorithm: {run['algorithm']}\n")
                f.write(f"Map Index: {run['map_index']}\n")
                f.write(f"States Explored: {run['states_explored']}\n")
                f.write(f"Runtime (ms): {run['runtime_ms']:.2f}\n")
                f.write(f"Path: {run['path']}\n")
                f.write("-----------------------------\n\n")

        system = platform.system().lower()
        try:
            if system == "windows":
                os.startfile(filename)
            elif system == "darwin":
                subprocess.run(["open", filename], check=True)
            elif system == "linux":
                subprocess.run(["xdg-open", filename], check=True)
            else:
                print(f"Auto-open not supported on {system}. Please open the file manually: {filename}")
        except Exception as e:
            print(f"Error opening file: {e}. Please open the file manually: {filename}")

    except Exception as e:
        print(f"Error saving to file: {e}")

# Tải tài nguyên: ảnh, video, âm thanh
# Tải video
background_frames = []
try:
    video_path = os.path.abspath("asset/anh_background/background1.mp4")
    print(f"Đường dẫn video: {video_path}")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"File MP4 không tồn tại: {video_path}")

    cap = cv2.VideoCapture(video_path)
    def get_next_frame():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Quay lại đầu video
            ret, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))
        return pygame.transform.scale(frame_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    if not cap.isOpened():
        raise RuntimeError(f"Không thể mở file MP4: {video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))
        frame_surface = pygame.transform.scale(frame_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        background_frames.append(frame_surface)
    cap.release()
except Exception as e:
    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background.fill((50, 150, 50))
    background_frames = [background]

# Biến để theo dõi khung hình
frame_index = 0
FPS = 30

#--------------------------------------------------------

try:
    background3 = pygame.image.load(r"asset\anh_background\chienthanggame.png").convert()
    background3 = pygame.transform.smoothscale(background3, (WINDOW_WIDTH, WINDOW_HEIGHT))
except:
    background3 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background3.fill((50, 150, 50))

WALL_TEXTURE = pygame.image.load(r"asset/anh_icon/gach3.jpg").convert()
WALL_TEXTURE = pygame.transform.scale(WALL_TEXTURE, (MAZE_WIDTH, MAZE_HEIGHT))

try:
    door_img = pygame.image.load(r"asset\anh_icon\canhcua.png").convert_alpha()
    door_img = pygame.transform.scale(door_img, (GRID_SIZE - 5, GRID_SIZE - 5))
except Exception as e:
    print(f"Không thể tải hình ảnh cánh cửa: {e}")
    door_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    pygame.draw.rect(door_img, YELLOW, (0, 0, GRID_SIZE - 5, GRID_SIZE - 5))

try:
    victory_sound = pygame.mixer.Sound(r"asset\nhac\nhac_chien_thang.mp3")
except Exception as e:
    print(f"Không thể tải âm thanh: {e}")
    victory_sound = None

try:
    door_open_sound = pygame.mixer.Sound(r"asset\nhac\nhac_mo_cua.mp3")
except Exception as e:
    print(f"Không thể tải âm thanh mở cửa: {e}")
    door_open_sound = None

# Màn hình khởi động
def splash_screen():
    try:
        splash_image = pygame.image.load(r"asset\anh_background\anhnen.png").convert()
        splash_image = pygame.transform.smoothscale(splash_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        splash_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        splash_image.fill(DARK_BLUE)
        text = font_large.render("Pursuit Game", True, YELLOW)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        splash_image.blit(text, text_rect)

    ball_size = 50
    ball_surface = pygame.Surface((ball_size, ball_size), pygame.SRCALPHA)
    pygame.draw.circle(ball_surface, (0, 255, 0), (ball_size // 2, ball_size // 2), ball_size // 2)

    center_x, center_y = ball_size // 2, ball_size // 2
    radius = ball_size // 2

    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = center_x + radius * math.cos(rad)
        y1 = center_y + radius * math.sin(rad)
        x2 = center_x - radius * math.cos(rad)
        y2 = center_y - radius * math.sin(rad)
        pygame.draw.line(ball_surface, (255, 255, 255), (x1, y1), (x2, y2), 2)

    for r in range(radius // 3, radius, radius // 3):
        pygame.draw.circle(ball_surface, (255, 255, 255), (center_x, center_y), r, 2)

    pygame.draw.line(ball_surface, (255, 255, 255), (center_x - radius, center_y - radius // 2),
                     (center_x + radius, center_y + radius // 2), 2)
    pygame.draw.line(ball_surface, (255, 255, 255), (center_x - radius, center_y + radius // 2),
                     (center_x + radius, center_y - radius // 2), 2)

    path = []
    for x in range(50, WINDOW_WIDTH - 50, 5):
        y = WINDOW_HEIGHT - 50 + 20 * math.sin(x * 0.02)
        path.append((x, y))

    splash_duration = 7 * 1000
    total_path_length = len(path)
    total_frames = (splash_duration / 1000) * FPS
    ball_speed = total_path_length / total_frames

    start_time = pygame.time.get_ticks()
    path_index = 0
    rotation_angle = 0
    rotation_speed = 360 / total_path_length * ball_speed

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= splash_duration:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                break

        path_index += ball_speed
        if path_index >= len(path):
            path_index = len(path) - 1

        rotation_angle += rotation_speed
        if rotation_angle >= 360:
            rotation_angle -= 360

        rotated_ball = pygame.transform.rotate(ball_surface, rotation_angle)
        rotated_rect = rotated_ball.get_rect(center=(ball_size // 2, ball_size // 2))

        screen.blit(splash_image, (0, 0))
        current_path_index = int(path_index)
        if current_path_index > 0:
            pygame.draw.lines(screen, (0, 255, 0), False, path[:current_path_index + 1], 7)

        ball_pos = path[int(path_index)]
        screen.blit(rotated_ball, (ball_pos[0] - rotated_rect.width // 2, ball_pos[1] - rotated_rect.height // 2))

        pygame.display.flip()
        clock.tick(FPS)

    return True

# Màn hình menu
def menu_screen():
    global frame_index
    menu_active = True
    selected = False
    blink_counter = 0
    blink_interval = 30

    def render_text_with_outline(text, font, text_color, outline_color):
        text_surface = font.render(text, True, text_color)
        outline_surface = font.render(text, True, outline_color)
        surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2), (2, -2), (-2, 2)]:
            surface.blit(outline_surface, (dx + 2, dy + 2))
        surface.blit(text_surface, (2, 2))
        return surface

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_giao_dien.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải menu_music.mp3")

    title_font = pygame.font.Font("freesansbold.ttf", 80)
    option_font = pygame.font.Font("freesansbold.ttf", 60)

    while menu_active:
        if background_frames:
            screen.blit(background_frames[frame_index], (0, 0))
            frame_index = (frame_index + 1) % len(background_frames)
        else:
            screen.fill((50, 150, 50))

        title_text = title_font.render("Pursuit Game", True, YELLOW)
        title_shadow = title_font.render("Pursuit Game", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))

        screen.blit(title_shadow, title_rect.move(2, 2))
        screen.blit(title_text, title_rect)

        blink_counter = (blink_counter + 1) % (blink_interval * 2)
        if blink_counter < blink_interval:
            color = WHITE
        else:
            color = GREEN

        text_surface = render_text_with_outline("Start", option_font, color, DARK_RED)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Selected Special Mode")
                    return "Special Mode"
                elif event.key == pygame.K_ESCAPE:
                    return None

    return None

# Giao diện chiến thắng
def victory_screen(fastest_algo, mode='Special Mode'):
    pygame.mixer.music.stop()
    if victory_sound:
        victory_sound.play()

    screen.blit(background3, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(0)
    screen.blit(overlay, (0, 0))

    def render_text_with_outline(text, font, text_color, outline_color):
        text_surface = font.render(text, True, text_color)
        outline_surface = font.render(text, True, outline_color)
        surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2), (2, -2), (-2, 2)]:
            surface.blit(outline_surface, (dx + 2, dy + 2))
        surface.blit(text_surface, (2, 2))
        return surface

    victory_text = render_text_with_outline("Victory!", font_large, YELLOW, GREEN)
    fastest_text = render_text_with_outline(f"Fastest Algorithm: {fastest_algo}", font, WHITE, BLACK)
    replay_text = render_text_with_outline("Press R to Replay, Q to Quit", font, WHITE, BLACK)
    view_plot_text = render_text_with_outline("Press V to View Plot", font, WHITE, BLACK)
    save_info_text = render_text_with_outline("Press I to Save Algorithm Info", font, WHITE, BLACK)

    spacing = 70
    start_y = WINDOW_HEIGHT // 3

    victory_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, start_y - 20))
    fastest_rect = fastest_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + spacing))
    replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 2 * spacing))
    view_plot_rect = view_plot_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 3 * spacing))
    save_info_rect = save_info_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 4 * spacing))

    waiting = True
    while waiting:
        screen.blit(background3, (0, 0))
        screen.blit(overlay, (0, 0))
        for text, rect in [(victory_text, victory_rect), (fastest_text, fastest_rect),
                           (replay_text, replay_rect), (view_plot_text, view_plot_rect),
                           (save_info_text, save_info_rect)]:
            screen.blit(text, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if victory_sound:
                        victory_sound.stop()
                    return True
                elif event.key == pygame.K_q:
                    if victory_sound:
                        victory_sound.stop()
                    return False
                elif event.key == pygame.K_v:
                    plot_comparison(mode=mode)
                elif event.key == pygame.K_i:
                    save_algorithm_info_to_file(mode=mode)

    return False


# Vòng lặp game chính
running = True
FPS = 60
while running:
    check = 0
    if not splash_screen():
        break

    mode = menu_screen()
    if mode != 'Special Mode':
        break

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_choi_game.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải gameplay_music.mp3")

    game_active = True
    current_map_index = 0
    algorithm_runs = []

    while game_active:
        load_map("Me cung")

        try:
            game_background = pygame.image.load(r"asset\anh_background\map1.webp").convert()
            game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            game_background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            game_background.fill(DARK_BLUE)

        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()

        enemy_pos = (1, 1)
        exit_pos = get_exit_position()
        if grid[enemy_pos[1]][enemy_pos[0]] != 1 and grid[exit_pos[1]][exit_pos[0]] != 1:
            pass
        else:
            enemy_pos = get_empty_position()
            while enemy_pos == exit_pos:
                enemy_pos = get_empty_position()

        # đặt gai trên lưới
        grid = spawn_spikes(grid, enemy_pos, exit_pos, num_spikes=5)

        algorithms = ["BFS", "A*", "Beam Search", "AND-OR Tree", "Forward-Checking", "Q-Learning"]
        for idx, algo in enumerate(algorithms):
            enemy = Enemy(enemy_pos[0], enemy_pos[1], algo)
            enemy.label_offset_y = -20 - (idx * 3)
            all_sprites.add(enemy)
            enemies.add(enemy)
            print(f"Spawned {algo} enemy at position: {enemy_pos}")

        while game_active:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                    running = False

            all_sprites.update()
            for enemy in enemies:
                x, y = enemy.grid_pos
                if grid[y][x] == 1:
                    enemy.grid_pos = list(get_empty_position())
                    enemy.pixel_pos = list(to_pixel_pos(enemy.grid_pos[0], enemy.grid_pos[1]))
                    enemy.rect.center = (int(enemy.pixel_pos[0]), int(enemy.pixel_pos[1]))
                    enemy.path = []
                    enemy.moving = False

                if tuple(enemy.grid_pos) == exit_pos:
                    fastest_algo = enemy.algorithm  # Lấy thuật toán của quái vật đến đầu tiên
                    replay = victory_screen(fastest_algo, mode='Special Mode')
                    if not replay:
                        running = False
                    game_active = False
                    break

            if not game_active:
                break

            screen.blit(game_background, (0, 0))
            screen.blit(WALL_TEXTURE, (MAZE_OFFSET_X, MAZE_OFFSET_Y))
            draw_grid(exit_pos)
            for sprite in all_sprites:
                sprite.draw(screen)

            pygame.display.flip()

pygame.quit()