import pygame
import random
import heapq
import math
from collections import deque

# Khởi tạo Pygame
pygame.init()

# Thiết lập cửa sổ game
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH =20
GRID_HEIGHT = 20
MAZE_WIDTH = GRID_WIDTH * GRID_SIZE  # 600
MAZE_HEIGHT = GRID_HEIGHT * GRID_SIZE  # 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pursuit Game")

# Tính toán tọa độ để căn giữa mê cung
MAZE_OFFSET_X = (WINDOW_WIDTH - MAZE_WIDTH) // 2  # 300
MAZE_OFFSET_Y = (WINDOW_HEIGHT - MAZE_HEIGHT) // 2  # 50

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

# Tạo lưới
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Định nghĩa các bản đồ (giữ nguyên)
MAPS = {
    "Me cung": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    ],
    "Can ho": [
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
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    ],
    "Khach san": [
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
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    ]


}

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

# Vẽ lưới
def draw_grid(exit_pos=None):
    pygame.draw.rect(screen, DARK_GRAY, (MAZE_OFFSET_X, MAZE_OFFSET_Y, MAZE_WIDTH, MAZE_HEIGHT), 5)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(MAZE_OFFSET_X + x * GRID_SIZE, MAZE_OFFSET_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, DARK_GRAY, rect, 2)
            elif grid[y][x] == 2:  # Lối ra
                pygame.draw.rect(screen, YELLOW, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
            elif grid[y][x] == 3:  # Tăng tốc (Speed Boost)
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(speed_boost_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 4:  # Làm chậm (Slow Enemy)
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(slow_enemy_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 5:  # Tàng hình (Invisibility)
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(invisibility_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 6:  # Gai (Spikes)
                pygame.draw.rect(screen, LIGHT_GREEN, rect)  # Nền
                screen.blit(spike_img, (rect.x + 2.5, rect.y + 2.5))  # Hiển thị hình ảnh gai
            else:
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


# hàm tìm vị trí lối ra
def get_exit_position():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 2:
                return (x, y)
    return None  # Nếu không tìm thấy (dự phòng)

# Chuyển đổi tọa độ
def to_grid_pos(x, y):
    return ((x - MAZE_OFFSET_X) // GRID_SIZE, (y - MAZE_OFFSET_Y) // GRID_SIZE)

def to_pixel_pos(grid_x, grid_y):
    return (MAZE_OFFSET_X + grid_x * GRID_SIZE + GRID_SIZE // 2, MAZE_OFFSET_Y + grid_y * GRID_SIZE + GRID_SIZE // 2)

# sinh vật phẩm ngẫu nhiên
def spawn_items(grid, player_pos, enemy_pos, exit_pos, num_items=3, num_spikes=2):
    """
    Sinh ngẫu nhiên các vật phẩm và gai trên bản đồ.
    - num_items: Số lượng vật phẩm (Speed Boost, Slow Enemy, Invisibility).
    - num_spikes: Số lượng gai.
    """
    item_types = [3, 4, 5]  # 3: Speed Boost, 4: Slow Enemy, 5: Invisibility
    placed_items = 0
    placed_spikes = 0

    # Sinh vật phẩm
    while placed_items < num_items:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        pos = (x, y)
        if (grid[y][x] == 0 and pos != player_pos and pos != enemy_pos and pos != exit_pos):
            item_type = random.choice(item_types)
            grid[y][x] = item_type
            placed_items += 1

    # Sinh gai
    while placed_spikes < num_spikes:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        pos = (x, y)
        if (grid[y][x] == 0 and pos != player_pos and pos != enemy_pos and pos != exit_pos):
            grid[y][x] = 6  # Gai
            placed_spikes += 1


# Các hàm thuật toán
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
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] !=1 and
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

# IDS (Iterative Deepening Search)
def ids_search(start, goal):
    def dls(node, goal, depth, came_from, visited):
        if depth < 0:
            return False, None
        if node == goal:
            return True, node
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (node[0] + dx, node[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] !=1 and
                    next_pos not in visited):
                visited.add(next_pos)
                came_from[next_pos] = node
                found, result = dls(next_pos, goal, depth - 1, came_from, visited)
                if found:
                    return True, result
        return False, None

    depth = 0
    while True:
        came_from = {start: None}
        visited = {start}
        found, result = dls(start, goal, depth, came_from, visited)
        if found:
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
        depth += 1

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
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] !=1):
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
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] !=1 and
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
        self.grid_pos = [grid_x, grid_y]
        self.pixel_pos = list(to_pixel_pos(grid_x, grid_y))
        self.rect.center = self.pixel_pos
        self.speed = 5
        self.default_speed = 5
        self.speed_boost_timer = 0
        self.slow_timer = 0  # Thời gian bị làm chậm bởi gai
        self.health = 100  # Máu tối đa
        self.max_health = 100
        self.health_cooldown = 0  # Thời gian hồi để không bị trừ máu liên tục
        self.original_image = self.image.copy()
        self.blink_timer = 0

    def activate_speed_boost(self):
        self.speed = 8
        self.speed_boost_timer = 10 * FPS

    def hit_spike(self):
        if self.health_cooldown <= 0:  # Chỉ trừ máu nếu không trong thời gian hồi
            self.health -= 20  # Trừ 20 máu khi chạm gai
            self.speed = 3  # Làm chậm
            self.slow_timer = 5 * FPS  # Làm chậm trong 5 giây
            self.health_cooldown = 1 * FPS  # Hồi 1 giây trước khi bị trừ máu tiếp
            self.blink_timer = 1 * FPS
            if spike_sound:
                spike_sound.play()
            if self.health < 0:
                self.health = 0

    def update(self):
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed = self.default_speed

        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.speed = self.default_speed

        if self.health_cooldown > 0:
            self.health_cooldown -= 1

        if self.blink_timer > 0:
            self.blink_timer -= 1
            if self.blink_timer % 10 < 5:  # Nhấp nháy
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        keys = pygame.key.get_pressed()
        target_grid_x, target_grid_y = self.grid_pos[0], self.grid_pos[1]
        if keys[pygame.K_LEFT]:
            target_grid_x -= 1
        if keys[pygame.K_RIGHT]:
            target_grid_x += 1
        if keys[pygame.K_UP]:
            target_grid_y -= 1
        if keys[pygame.K_DOWN]:
            target_grid_y += 1
        if (0 <= target_grid_x < GRID_WIDTH and 0 <= target_grid_y < GRID_HEIGHT and
                grid[target_grid_y][target_grid_x] != 1):
            target_pixel_pos = to_pixel_pos(target_grid_x, target_grid_y)
            if self.pixel_pos[0] < target_pixel_pos[0]:
                self.pixel_pos[0] += self.speed
            elif self.pixel_pos[0] > target_pixel_pos[0]:
                self.pixel_pos[0] -= self.speed
            if self.pixel_pos[1] < target_pixel_pos[1]:
                self.pixel_pos[1] += self.speed
            elif self.pixel_pos[1] > target_pixel_pos[1]:
                self.pixel_pos[1] -= self.speed
            if abs(self.pixel_pos[0] - target_pixel_pos[0]) < self.speed and \
               abs(self.pixel_pos[1] - target_pixel_pos[1]) < self.speed:
                self.pixel_pos = list(target_pixel_pos)
                self.grid_pos = [target_grid_x, target_grid_y]
        self.rect.center = (int(self.pixel_pos[0]), int(self.pixel_pos[1]))



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
            self.move_delay = 30
        elif difficulty == "Medium":
            self.move_delay = 15
        else:
            self.move_delay = 5
        self.default_move_delay = self.move_delay
        self.slow_timer = 0
        self.invisibility_timer = 0

    def activate_slow(self):
        self.move_delay = self.default_move_delay * 2  # Làm chậm
        self.slow_timer = 10 * FPS  # 10 giây

    def activate_invisibility(self):
        self.invisibility_timer = 5 * FPS  # 5 giây

    def update(self):
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.move_delay = self.default_move_delay

        if self.invisibility_timer > 0:
            self.invisibility_timer -= 1

        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            if self.invisibility_timer > 0:
                # Di chuyển ngẫu nhiên khi người chơi tàng hình
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                random.shuffle(directions)
                for dx, dy in directions:
                    next_pos = (self.grid_pos[0] + dx, self.grid_pos[1] + dy)
                    x, y = next_pos
                    if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1):
                        self.grid_pos = next_pos
                        self.rect.center = to_pixel_pos(next_pos[0], next_pos[1])
                        break
            else:
                player_grid_pos = tuple(self.player.grid_pos)
                if self.algorithm == "BFS":
                    self.path = bfs_search(self.grid_pos, player_grid_pos)
                elif self.algorithm == "IDS":
                    self.path = ids_search(self.grid_pos, player_grid_pos)
                elif self.algorithm == "A*":
                    self.path = a_star_search(self.grid_pos, player_grid_pos)
                elif self.algorithm == "IDA*":
                    self.path = ida_star_search(self.grid_pos, player_grid_pos)
                if len(self.path) > 1:
                    next_pos = self.path[1]
                    self.grid_pos = next_pos
                    self.rect.center = to_pixel_pos(next_pos[0], next_pos[1])
                elif len(self.path) == 0:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    random.shuffle(directions)
                    for dx, dy in directions:
                        next_pos = (self.grid_pos[0] + dx, self.grid_pos[1] + dy)
                        x, y = next_pos
                        if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1):
                            self.grid_pos = next_pos
                            self.rect.center = to_pixel_pos(next_pos[0], next_pos[1])
                            break




# Tải hình nền bắt đầu game
try:
    background = pygame.image.load(r"asset\anh_backgound\anh8.jpg").convert()
    background = pygame.transform.smoothscale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Dùng smoothscale cho chất lượng tốt hơn
except:
    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background.fill((50, 150, 50))

# Tải hình nền kết thúc game
try:
    background2 = pygame.image.load(r"asset\anh_backgound\anhdep.jpg").convert()
    background2 = pygame.transform.smoothscale(background2, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Dùng smoothscale cho chất lượng tốt hơn
except:
    background2 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background2.fill((50, 150, 50))

# tải ảnh vật phẩm
try:
    speed_boost_img = pygame.image.load(r"asset\anh_icon\Giay.jpg").convert_alpha()# giay tang toc
    speed_boost_img = pygame.transform.scale(speed_boost_img, (GRID_SIZE - 5, GRID_SIZE - 5))  # Thu nhỏ để vừa ô
    slow_enemy_img = pygame.image.load(r"asset\anh_icon\lonuoc2.png").convert_alpha() # lo nuoc lam cham quai vat
    slow_enemy_img = pygame.transform.scale(slow_enemy_img, (GRID_SIZE - 5, GRID_SIZE - 5))
    invisibility_img = pygame.image.load(r"asset\anh_icon\aochoang1.png").convert_alpha() # ao choang tang hinh
    invisibility_img = pygame.transform.scale(invisibility_img, (GRID_SIZE - 5, GRID_SIZE - 5))
except pygame.error as e:
    print(f"Không thể tải hình ảnh vật phẩm: {e}")
    # Dùng hình mặc định nếu không tải được
    speed_boost_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    speed_boost_img.fill(BLUE)
    slow_enemy_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    slow_enemy_img.fill(WHITE)
    invisibility_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    invisibility_img.fill((128, 0, 128))

# Tải hình ảnh gai
try:
    spike_img = pygame.image.load(r"asset\anh_icon\bay.png").convert_alpha()
    spike_img = pygame.transform.scale(spike_img, (GRID_SIZE - 5, GRID_SIZE - 5))  # Thu nhỏ để vừa ô (25x25)
except Exception as e:
    print(f"Không thể tải hình ảnh gai: {e}")
    # Nếu không tải được, dùng hình mặc định (vẽ thủ công)
    spike_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    pygame.draw.circle(spike_img, RED, (12.5, 12.5), 8)
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1, y1 = 12.5, 12.5
        x2 = x1 + math.cos(rad) * 12
        y2 = y1 + math.sin(rad) * 12
        pygame.draw.line(spike_img, RED, (x1, y1), (x2, y2), 2)

# tai am thanh nhat vat pham
try:
    pickup_sound = pygame.mixer.Sound(r"asset\nhac\nhac_nhat_do.mp3")
except Exception as e:
    print(f"Không thể tải âm thanh: {e}")
    pickup_sound = None

# tai am thanh cham gai
try:
    spike_sound = pygame.mixer.Sound(r"asset\nhac\nhac_dinh_bay.mp3")
except:
    spike_sound = None

# Tải âm thanh dung game
try:
    collision_sound = pygame.mixer.Sound(r"asset\nhac\nhac_thua_cuoc.mp3")
except:
    collision_sound = None

# tai am thanh chien thang
try:
    victory_sound = pygame.mixer.Sound(r"asset\nhac\nhac_chien_thang.mp3")
except Exception as e:
    print(f"Không thể tải âm thanh: {e}")
    victory_sound = None



# Menu chọn thuật toán, chế độ chơi và bản đồ (cập nhật kích thước)
def menu_screen():
    # Tải và phát nhạc cho menu
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_giao_dien.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải menu_music.mp3")

    # Danh sách thuật toán
    uninformed_algorithms = ["BFS", "IDS"]
    informed_algorithms = ["A*", "IDA*"]
    all_algorithms = uninformed_algorithms + informed_algorithms  # Hợp nhất để chọn
    difficulties = ["Easy", "Medium", "Hard"]

    selected_idx = 0  # Chỉ số thuật toán được chọn (trong all_algorithms)
    selected_difficulty = 0
    selecting = "algorithm"  # Chọn thuật toán trước, rồi độ khó

    while True:
        screen.blit(background, (0, 0))
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        #overlay.fill(DARK_BLUE)
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        # Tiêu đề game
        title = font_large.render("Pursuit Game", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 60))
        title_bg = pygame.Surface((title_rect.width + 20, title_rect.height + 10))
        title_bg.fill(BLACK)
        title_bg.set_alpha(150)
        screen.blit(title_bg, (title_rect.x - 10, title_rect.y - 5))
        screen.blit(title, title_rect)

        # Nhóm Uninformed Search
        uninformed_text = font.render("Uninformed Search:", True, WHITE)
        uninformed_rect = uninformed_text.get_rect(center=(WINDOW_WIDTH // 2, 110))
        uninformed_bg = pygame.Surface((uninformed_rect.width + 20, uninformed_rect.height + 10))
        uninformed_bg.fill(BLACK)
        uninformed_bg.set_alpha(150)
        screen.blit(uninformed_bg, (uninformed_rect.x - 10, uninformed_rect.y - 5))
        screen.blit(uninformed_text, uninformed_rect)

        for i, algo in enumerate(uninformed_algorithms):
            color = YELLOW if (selecting == "algorithm" and selected_idx == i) else WHITE
            text = font_small.render(algo, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 150 + i * 30))
            if selecting == "algorithm" and selected_idx == i:
                pygame.draw.rect(screen, YELLOW, text_rect.inflate(20, 10), 2)
            screen.blit(text, text_rect)

        # Nhóm Informed Search
        informed_text = font.render("Informed Search:", True, WHITE)
        informed_rect = informed_text.get_rect(center=(WINDOW_WIDTH // 2, 220))
        informed_bg = pygame.Surface((informed_rect.width + 20, informed_rect.height + 10))
        informed_bg.fill(BLACK)
        informed_bg.set_alpha(150)
        screen.blit(informed_bg, (informed_rect.x - 10, informed_rect.y - 5))
        screen.blit(informed_text, informed_rect)

        for i, algo in enumerate(informed_algorithms):
            global_idx = i + len(uninformed_algorithms)  # Chỉ số trong all_algorithms
            color = YELLOW if (selecting == "algorithm" and selected_idx == global_idx) else WHITE
            text = font_small.render(algo, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 260 + i * 30))
            if selecting == "algorithm" and selected_idx == global_idx:
                pygame.draw.rect(screen, YELLOW, text_rect.inflate(20, 10), 2)
            screen.blit(text, text_rect)

        # Chọn độ khó
        diff_text = font.render("Select Difficulty:", True, WHITE)
        diff_rect = diff_text.get_rect(center=(WINDOW_WIDTH // 2, 350))
        diff_bg = pygame.Surface((diff_rect.width + 20, diff_rect.height + 10))
        diff_bg.fill(BLACK)
        diff_bg.set_alpha(150)
        screen.blit(diff_bg, (diff_rect.x - 10, diff_rect.y - 5))
        screen.blit(diff_text, diff_rect)

        for i, diff in enumerate(difficulties):
            color = YELLOW if (selecting == "difficulty" and i == selected_difficulty) else WHITE
            text = font_small.render(diff, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 380 + i * 30))
            if selecting == "difficulty" and i == selected_difficulty:
                pygame.draw.rect(screen, YELLOW, text_rect.inflate(20, 10), 2)
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None  # Trả về None nếu thoát
            if event.type == pygame.KEYDOWN:
                if selecting == "algorithm":
                    if event.key == pygame.K_UP:
                        selected_idx = (selected_idx - 1) % len(all_algorithms)
                    elif event.key == pygame.K_DOWN:
                        selected_idx = (selected_idx + 1) % len(all_algorithms)
                    elif event.key == pygame.K_RETURN:
                        selected_algorithm = all_algorithms[selected_idx]
                        selecting = "difficulty"
                elif selecting == "difficulty":
                    if event.key == pygame.K_UP:
                        selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                    elif event.key == pygame.K_DOWN:
                        selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                    elif event.key == pygame.K_RETURN:
                        return selected_algorithm, difficulties[selected_difficulty]  # Trả về thuật toán và độ khó


# Game Over (cập nhật kích thước)
def game_over_screen(final_score):
    pygame.mixer.music.stop()  # Dừng nhạc gameplay
    screen.blit(background2, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(120)
    screen.blit(overlay, (0, 0))

    game_over_text = font_large.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    replay_text = font.render("Press R to Replay", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + 20))

    for text, rect in [(game_over_text, game_over_rect), (score_text, score_rect), (replay_text, replay_rect)]:
        bg = pygame.Surface((rect.width + 20, rect.height + 10))
        bg.fill(BLACK)
        bg.set_alpha(100)
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

def victory_screen(final_score):
    pygame.mixer.music.stop()  # Dừng nhạc nền
    if victory_sound:  # Phát âm thanh chiến thắng
        victory_sound.play()

    screen.blit(background2, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(100)
    screen.blit(overlay, (0, 0))

    victory_text = font_large.render("You Win!", True, YELLOW)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    replay_text = font.render("Press R to Replay", True, WHITE)

    victory_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + 20))

    for text, rect in [(victory_text, victory_rect), (score_text, score_rect), (replay_text, replay_rect)]:
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
                    victory_sound.stop()
                    return True
    return False


# Vẽ bảng thông tin (HUD) (đặt bên ngoài mê cung, bên phải)
def draw_hud(score, algorithm, difficulty, map_name, player):
    hud_width = 220
    hud_height = 180  # Tăng chiều cao để chứa thanh máu
    hud = pygame.Surface((hud_width, hud_height))
    hud.fill(DARK_BLUE)
    hud.set_alpha(200)

    hud_x = MAZE_OFFSET_X + MAZE_WIDTH + 20
    hud_y = MAZE_OFFSET_Y + 10
    screen.blit(hud, (hud_x, hud_y))

    score_text = font.render(f"Score: {score}", True, WHITE)
    algo_text = font_small.render(f"Algorithm: {algorithm}", True, WHITE)
    diff_text = font_small.render(f"Difficulty: {difficulty}", True, WHITE)
    map_text = font_small.render(f"Map: {map_name}", True, WHITE)
    health_text = font_small.render(f"Health: {player.health}", True, WHITE)

    screen.blit(score_text, (hud_x + 10, hud_y + 10))
    screen.blit(algo_text, (hud_x + 10, hud_y + 40))
    screen.blit(diff_text, (hud_x + 10, hud_y + 70))
    screen.blit(map_text, (hud_x + 10, hud_y + 100))
    screen.blit(health_text, (hud_x + 10, hud_y + 130))

    # Vẽ thanh máu
    health_bar_width = 150
    health_bar_height = 10
    health_ratio = player.health / player.max_health
    pygame.draw.rect(screen, RED, (hud_x + 10, hud_y + 150, health_bar_width, health_bar_height))  # Nền thanh máu
    pygame.draw.rect(screen, (0, 255, 0), (hud_x + 10, hud_y + 150, health_bar_width * health_ratio, health_bar_height))  # Thanh máu
    pygame.draw.rect(screen, BLACK, (hud_x + 10, hud_y + 150, health_bar_width, health_bar_height), 2)  # Viền


MAP_BACKGROUNDS = {
    "Me cung": r"asset\anh_backgound\anh.webp",
    "Can ho": r"asset\anh_backgound\anh4.jpg",
    "Khach san": r"asset\anh_backgound\anhgame3.png",
}

# Vòng lặp game chính
# Vòng lặp game chính
running = True
while running:
    algorithm, difficulty = menu_screen()
    if algorithm is None:
        break

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_choi_game.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải gameplay_music.mp3")

    map_order = ["Me cung", "Can ho", "Khach san"]
    current_map_idx = 0

    score = 0
    game_active = True

    while game_active and current_map_idx < len(map_order):
        # Tải bản đồ
        load_map(map_order[current_map_idx])

        # Tải hình nền tương ứng với bản đồ
        try:
            game_background = pygame.image.load(MAP_BACKGROUNDS[map_order[current_map_idx]]).convert()
            game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print(f"Không thể tải hình nền cho {map_order[current_map_idx]}: {e}")
            game_background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            game_background.fill(DARK_BLUE)  # Hình nền mặc định nếu lỗi

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

        exit_pos = get_exit_position()
        spawn_items(grid, player_pos, enemy_pos, exit_pos, num_items=3, num_spikes=5)

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

            if tuple(player.grid_pos) == exit_pos:
                current_map_idx += 1
                if current_map_idx >= len(map_order):
                    replay = victory_screen(score)
                    if not replay:
                        running = False
                    game_active = False
                break

            player_grid_x, player_grid_y = player.grid_pos
            item = grid[player_grid_y][player_grid_x]
            if item in [3, 4, 5, 6]:
                if item == 3:
                    player.activate_speed_boost()
                    if pickup_sound:
                        pickup_sound.play()
                elif item == 4:
                    enemy.activate_slow()
                    if pickup_sound:
                        pickup_sound.play()
                elif item == 5:
                    enemy.activate_invisibility()
                    if pickup_sound:
                        pickup_sound.play()
                elif item == 6:
                    player.hit_spike()
                if item != 6:
                    grid[player_grid_y][player_grid_x] = 0

            if player.health <= 0:
                if collision_sound:
                    collision_sound.play()
                game_active = False

            screen.blit(game_background, (0, 0))
            draw_grid(exit_pos)
            all_sprites.draw(screen)
            draw_hud(score, algorithm, difficulty, map_order[current_map_idx], player)
            pygame.display.flip()

    if running and not game_active and current_map_idx < len(map_order):
        replay = game_over_screen(score)
        if not replay:
            running = False

pygame.quit()
