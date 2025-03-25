import pygame
import random
import heapq
import math
from collections import deque

# Khởi tạo Pygame
pygame.init()

# Thiết lập cửa sổ game
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pursuit Game")

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

# Tạo lưới (0: trống, 1: chướng ngại vật)
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Định nghĩa các bản đồ
MAPS = {
    "Me cung cuu cong chúa": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "Căn ho sang trong": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    "Khach san 5 sao": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
}


# Tải bản đồ được chọn
def load_map(map_name):
    global grid
    grid = [row[:] for row in MAPS[map_name]]


# Đảm bảo vị trí ban đầu không nằm trên chướng ngại vật
def get_empty_position():
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if grid[y][x] == 0:
            return (x, y)


# Vẽ lưới và chướng ngại vật
def draw_grid():
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, HEIGHT), 5)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, DARK_GRAY, rect, 2)
            else:
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


# Chuyển đổi tọa độ
def to_grid_pos(x, y):
    return (x // GRID_SIZE, y // GRID_SIZE)


def to_pixel_pos(grid_x, grid_y):
    return (grid_x * GRID_SIZE + GRID_SIZE // 2, grid_y * GRID_SIZE + GRID_SIZE // 2)


# Heuristic cho các thuật toán có thông tin
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# BFS
def bfs_search(start, goal):
    queue = deque([start])
    came_from = {start: None}
    visited = {start}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == 0 and
                    next_pos not in visited):
                queue.append(next_pos)
                visited.add(next_pos)
                came_from[next_pos] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path


# DFS
def dfs_search(start, goal):
    stack = [start]
    came_from = {start: None}
    visited = {start}

    while stack:
        current = stack.pop()
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == 0 and
                    next_pos not in visited):
                stack.append(next_pos)
                visited.add(next_pos)
                came_from[next_pos] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path


# A*
def a_star_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == 0):
                new_cost = cost_so_far[current] + 1
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
            return []
    path.append(start)
    path.reverse()
    return path


# IDA*
def ida_star_search(start, goal):
    def search(node, g, threshold, came_from):
        f = g + heuristic(node, goal)
        if f > threshold:
            return f, None
        if node == goal:
            return f, node
        min_f = float('inf')
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (node[0] + dx, node[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == 0 and
                    next_pos not in came_from):
                came_from[next_pos] = node
                new_f, result = search(next_pos, g + 1, threshold, came_from)
                if result is not None:
                    return new_f, result
                min_f = min(min_f, new_f)
                del came_from[next_pos]
        return min_f, None

    threshold = heuristic(start, goal)
    while True:
        came_from = {start: None}
        new_threshold, result = search(start, 0, threshold, came_from)
        if result is not None:
            path = []
            current = goal
            while current != start:
                path.append(current)
                current = came_from.get(current)
            path.append(start)
            path.reverse()
            return path
        if new_threshold == float('inf'):
            return []
        threshold = new_threshold


# Greedy Best-First Search (GDFS)
def greedy_best_first_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    visited = {start}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == 0 and
                    next_pos not in visited):
                priority = heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, next_pos))
                visited.add(next_pos)
                came_from[next_pos] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path


# Uniform Cost Search (UCS)
def ucs_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        cost, current = heapq.heappop(frontier)
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == 0):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    heapq.heappush(frontier, (new_cost, next_pos))
                    came_from[next_pos] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path


# Lớp Player
class Player(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 5), 5)
        pygame.draw.circle(self.image, BLACK, (8, 4), 1)
        pygame.draw.circle(self.image, BLACK, (12, 4), 1)
        pygame.draw.rect(self.image, BLUE, (8, 10, 4, 6))
        pygame.draw.line(self.image, BLUE, (8, 10), (4, 12), 2)
        pygame.draw.line(self.image, BLUE, (12, 10), (16, 12), 2)
        pygame.draw.line(self.image, BLUE, (9, 16), (9, 20), 2)
        pygame.draw.line(self.image, BLUE, (11, 16), (11, 20), 2)
        self.rect = self.image.get_rect()
        self.grid_pos = (grid_x, grid_y)
        self.rect.center = to_pixel_pos(grid_x, grid_y)
        self.speed = 1

    def update(self):
        keys = pygame.key.get_pressed()
        new_grid_x, new_grid_y = self.grid_pos
        if keys[pygame.K_LEFT]:
            new_grid_x -= self.speed
        if keys[pygame.K_RIGHT]:
            new_grid_x += self.speed
        if keys[pygame.K_UP]:
            new_grid_y -= self.speed
        if keys[pygame.K_DOWN]:
            new_grid_y += self.speed
        if (0 <= new_grid_x < GRID_WIDTH and 0 <= new_grid_y < GRID_HEIGHT and
                grid[new_grid_y][new_grid_x] == 0):
            self.grid_pos = (new_grid_x, new_grid_y)
            self.rect.center = to_pixel_pos(new_grid_x, new_grid_y)


# Lớp Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, player, algorithm, difficulty):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, DARK_RED, (10, 10), 8)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1, y1 = 10, 10
            x2 = x1 + math.cos(rad) * 10
            y2 = y1 + math.sin(rad) * 10
            pygame.draw.line(self.image, RED, (x1, y1), (x2, y2), 2)
        pygame.draw.circle(self.image, WHITE, (8, 8), 2)
        pygame.draw.circle(self.image, WHITE, (12, 8), 2)
        pygame.draw.circle(self.image, BLACK, (8, 8), 1)
        pygame.draw.circle(self.image, BLACK, (12, 8), 1)
        self.rect = self.image.get_rect()
        self.grid_pos = (grid_x, grid_y)
        self.rect.center = to_pixel_pos(grid_x, grid_y)
        self.player = player
        self.algorithm = algorithm
        self.path = []
        self.move_timer = 0
        if difficulty == "Easy":
            self.move_delay = 15
        elif difficulty == "Medium":
            self.move_delay = 10
        else:  # Hard
            self.move_delay = 5

    def update(self):
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            if self.algorithm == "BFS":
                self.path = bfs_search(self.grid_pos, self.player.grid_pos)
            elif self.algorithm == "DFS":
                self.path = dfs_search(self.grid_pos, self.player.grid_pos)
            elif self.algorithm == "A*":
                self.path = a_star_search(self.grid_pos, self.player.grid_pos)
            elif self.algorithm == "IDA*":
                self.path = ida_star_search(self.grid_pos, self.player.grid_pos)
            elif self.algorithm == "GDFS":
                self.path = greedy_best_first_search(self.grid_pos, self.player.grid_pos)
            elif self.algorithm == "UCS":
                self.path = ucs_search(self.grid_pos, self.player.grid_pos)
            if len(self.path) > 1:
                next_pos = self.path[1]
                self.grid_pos = next_pos
                self.rect.center = to_pixel_pos(next_pos[0], next_pos[1])


# Tải hình nền
try:
    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((50, 150, 50))

# Tải âm thanh
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)
    collision_sound = pygame.mixer.Sound("collision.wav")
except:
    collision_sound = None


# Menu chọn thuật toán, chế độ chơi và bản đồ
def menu_screen():
    algorithms = ["BFS", "DFS", "A*", "IDA*", "GDFS", "UCS"]
    difficulties = ["Easy", "Medium", "Hard"]
    maps = list(MAPS.keys())  # ["Map 1", "Map 2", "Map 3"]
    selected_algorithm = 0
    selected_difficulty = 0
    selected_map = 0
    selecting = "algorithm"

    while True:
        screen.blit(background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(DARK_BLUE)
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        # Tiêu đề
        title = font_large.render("Pursuit Game", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 60))
        title_bg = pygame.Surface((title_rect.width + 20, title_rect.height + 10))
        title_bg.fill(BLACK)
        title_bg.set_alpha(150)
        screen.blit(title_bg, (title_rect.x - 10, title_rect.y - 5))
        screen.blit(title, title_rect)

        # Hiển thị lựa chọn thuật toán
        algo_text = font.render("Select Algorithm:", True, WHITE)
        algo_rect = algo_text.get_rect(center=(WIDTH // 2, 110))
        algo_bg = pygame.Surface((algo_rect.width + 20, algo_rect.height + 10))
        algo_bg.fill(BLACK)
        algo_bg.set_alpha(150)
        screen.blit(algo_bg, (algo_rect.x - 10, algo_rect.y - 5))
        screen.blit(algo_text, algo_rect)

        for i, algo in enumerate(algorithms):
            color = YELLOW if i == selected_algorithm else WHITE
            text = font_small.render(algo, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 150 + i * 30))
            if i == selected_algorithm and selecting == "algorithm":
                pygame.draw.rect(screen, YELLOW, text_rect.inflate(20, 10), 2)
            screen.blit(text, text_rect)

        # Hiển thị lựa chọn chế độ chơi
        diff_text = font.render("Select Difficulty:", True, WHITE)
        diff_rect = diff_text.get_rect(center=(WIDTH // 2, 350))
        diff_bg = pygame.Surface((diff_rect.width + 20, diff_rect.height + 10))
        diff_bg.fill(BLACK)
        diff_bg.set_alpha(150)
        screen.blit(diff_bg, (diff_rect.x - 10, diff_rect.y - 5))
        screen.blit(diff_text, diff_rect)

        for i, diff in enumerate(difficulties):
            color = YELLOW if i == selected_difficulty else WHITE
            text = font_small.render(diff, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 380 + i * 30))
            if i == selected_difficulty and selecting == "difficulty":
                pygame.draw.rect(screen, YELLOW, text_rect.inflate(20, 10), 2)
            screen.blit(text, text_rect)

        # Hiển thị lựa chọn bản đồ
        map_text = font.render("Select Map:", True, WHITE)
        map_rect = map_text.get_rect(center=(WIDTH // 2, 470))
        map_bg = pygame.Surface((map_rect.width + 20, map_rect.height + 10))
        map_bg.fill(BLACK)
        map_bg.set_alpha(150)
        screen.blit(map_bg, (map_rect.x - 10, map_rect.y - 5))
        screen.blit(map_text, map_rect)

        for i, map_name in enumerate(maps):
            color = YELLOW if i == selected_map else WHITE
            text = font_small.render(map_name, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 500 + i * 30))
            if i == selected_map and selecting == "map":
                pygame.draw.rect(screen, YELLOW, text_rect.inflate(20, 10), 2)
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None, None
            if event.type == pygame.KEYDOWN:
                if selecting == "algorithm":
                    if event.key == pygame.K_UP:
                        selected_algorithm = (selected_algorithm - 1) % len(algorithms)
                    elif event.key == pygame.K_DOWN:
                        selected_algorithm = (selected_algorithm + 1) % len(algorithms)
                    elif event.key == pygame.K_RETURN:
                        selecting = "difficulty"
                elif selecting == "difficulty":
                    if event.key == pygame.K_UP:
                        selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                    elif event.key == pygame.K_DOWN:
                        selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                    elif event.key == pygame.K_RETURN:
                        selecting = "map"
                else:  # selecting == "map"
                    if event.key == pygame.K_UP:
                        selected_map = (selected_map - 1) % len(maps)
                    elif event.key == pygame.K_DOWN:
                        selected_map = (selected_map + 1) % len(maps)
                    elif event.key == pygame.K_RETURN:
                        return algorithms[selected_algorithm], difficulties[selected_difficulty], maps[selected_map]


# Game Over
def game_over_screen(final_score):
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))

    game_over_text = font_large.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    replay_text = font.render("Press R to Replay", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    replay_rect = replay_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3 + 20))

    for text, rect in [(game_over_text, game_over_rect), (score_text, score_rect), (replay_text, replay_rect)]:
        bg = pygame.Surface((rect.width + 20, rect.height + 10))
        bg.fill(BLACK)
        bg.set_alpha(150)
        screen.blit(bg, (rect.x - 10, rect.y - 5))
        screen.blit(text, rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
    return False


# Vẽ bảng thông tin (HUD)
def draw_hud(score, algorithm, difficulty, map_name):
    hud_width = 220
    hud_height = 140  # Tăng chiều cao để chứa thêm thông tin bản đồ
    hud = pygame.Surface((hud_width, hud_height))
    hud.fill(DARK_BLUE)
    hud.set_alpha(200)
    screen.blit(hud, (10, 10))

    score_text = font.render(f"Score: {score}", True, WHITE)
    algo_text = font_small.render(f"Algorithm: {algorithm}", True, WHITE)
    diff_text = font_small.render(f"Difficulty: {difficulty}", True, WHITE)
    map_text = font_small.render(f"Map: {map_name}", True, WHITE)

    screen.blit(score_text, (20, 20))
    screen.blit(algo_text, (20, 50))
    screen.blit(diff_text, (20, 80))
    screen.blit(map_text, (20, 110))


# Vòng lặp game chính
running = True
while running:
    algorithm, difficulty, map_name = menu_screen()
    if algorithm is None:
        break

    load_map(map_name)
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player_pos = get_empty_position()
    player = Player(player_pos[0], player_pos[1])

    enemy_pos = get_empty_position()
    while enemy_pos == player_pos:
        enemy_pos = get_empty_position()
    enemy = Enemy(enemy_pos[0], enemy_pos[1], player, algorithm, difficulty)

    all_sprites.add(player, enemy)
    enemies.add(enemy)

    score = 0
    game_active = True

    while game_active:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                running = False

        all_sprites.update()
        score += 1

        if pygame.sprite.spritecollide(player, enemies, False):
            if collision_sound:
                collision_sound.play()
            game_active = False

        screen.blit(background, (0, 0))
        draw_grid()
        all_sprites.draw(screen)
        draw_hud(score, algorithm, difficulty, map_name)
        pygame.display.flip()

    if running:
        replay = game_over_screen(score)
        if not replay:
            running = False

pygame.quit()