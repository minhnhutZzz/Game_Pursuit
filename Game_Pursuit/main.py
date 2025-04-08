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
option_font = pygame.font.Font(None, 36)
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
GREEN=(0,255,0)
xanhnhat=(150, 255, 150)


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
    # Stage 1 (Độ khó thấp - bản đồ hiện có)
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
    ],

    # Stage 2 (Độ khó trung bình)
    "Rung sau": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    ],
    "Nha may": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    ],
    "Thanh pho": [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    ]

    # # Stage 3 (Độ khó cao)
    # "Hang dong": [
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    #     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    #     [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    #     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    #     [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    # ],
    # "Cau truc": [
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    #     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    #     [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    #     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    #     [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    # ],
    # "La ma": [
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    #     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
    #     [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    #     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    #     [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    # ]
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
    pygame.draw.rect(screen, DARK_GRAY, (MAZE_OFFSET_X, MAZE_OFFSET_Y, MAZE_WIDTH, MAZE_HEIGHT), 3)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(MAZE_OFFSET_X + x * GRID_SIZE, MAZE_OFFSET_Y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if grid[y][x] == 1:
                #pygame.draw.rect(screen, GRAY, rect)
                #pygame.draw.rect(screen, DARK_GRAY, rect, 2)
                pass
            elif grid[y][x] == 2:  # Lối ra
                pygame.draw.rect(screen, YELLOW, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
            elif grid[y][x] == 3:  # Tăng tốc
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(speed_boost_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 4:  # Làm chậm
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(slow_enemy_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 5:  # Tàng hình
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(invisibility_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 6:  # Gai
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(spike_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 7:  # Trái bom
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(bomb_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x]==8:
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(heal_img, (rect.x+2.5, rect.y+2.5))

            else:
                pygame.draw.rect(screen, xanhnhat, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)


# hàm tìm vị trí lối ra
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



# sinh vật phẩm ngẫu nhiên
def spawn_items(grid, player_pos, enemy_pos, exit_pos, num_items=3, num_spikes=2):
    item_types = [3, 4, 5, 7,8]
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

    # Sinh gai (giữ nguyên)
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
    came_from = {start: None} # từ điển, lưu vt hiện tại và vt trước đó
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

        # tốc độ người chơi
        self.speed = 5
        self.default_speed = 5
        self.speed_boost_timer = 0

        # sức khỏe người chơi
        self.slow_timer = 0  # Thời gian bị làm chậm bởi gai
        self.health = 100  # Máu tối đa
        self.max_health = 100
        self.health_cooldown = 0  # Thời gian hồi để không bị trừ máu liên tục
        self.original_image = self.image.copy()

        # bomb
        self.blink_timer = 0
        self.bombs = 0  # Số lượng bom trong giỏ đồ
        self.b_key_pressed = False

    # hàm thêm bomb
    def add_bomb(self):
        self.bombs += 1
        if pickup_sound:
            pickup_sound.play()

    # hàm sử dụng bomb
    def use_bomb(self):
        if self.bombs > 0:
            self.bombs -= 1
            if bomb_sound:
                bomb_sound.play()

            # Tạo hiệu ứng nổ tại vị trí người chơi
            explosion = Explosion(self.pixel_pos[0], self.pixel_pos[1])
            all_sprites.add(explosion)  # Thêm vào nhóm sprite

            # Phá hủy tường trong phạm vi 3x3, trừ các bức tường ngoài
            px, py = self.grid_pos
            for dy in range(-1, 2):  # -1, 0, 1
                for dx in range(-1, 2):  # -1, 0, 1
                    nx, ny = px + dx, py + dy
                    # Kiểm tra xem ô có nằm trong lưới và không phải là tường ngoài
                    if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 1):
                        # Chỉ phá hủy nếu không phải tường ngoài
                        if not (nx == 0 or nx == GRID_WIDTH - 1 or ny == 0 or ny == GRID_HEIGHT - 1):
                            grid[ny][nx] = 0  # Phá tường thành đường đi

    # tăng tốc
    def activate_speed_boost(self):
        self.speed = 8
        self.speed_boost_timer = 5 * FPS

    # chạm vào gai
    def hit_spike(self):
        if self.health_cooldown <= 0:  # Chỉ trừ máu nếu không trong thời gian hồi
            self.health -= 20  # Trừ 20 máu khi chạm gai
            self.speed = 3  # Làm chậm
            self.slow_timer = 5 * FPS  # Làm chậm trong 5 giây
            self.health_cooldown = 1 * FPS  # thời gian hồi máu
            self.blink_timer = 1 * FPS # thời gian nhấp nháy
            if spike_sound:
                spike_sound.play()
            if self.health < 0:
                self.health = 0

    # hồi máu
    def heal (self, amount=30):
        self.health= min(self.max_health, self.health+amount)
        if pickup_sound:
            pickup_sound.play()


    def update(self):
        # trở về tốc độ ban đầu sau khi tăng tốc
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed = self.default_speed

        # trở về tốc độ ban đầu sau khi làm chậm
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.speed = self.default_speed

        # giảm thời gian hồi phục
        if self.health_cooldown > 0:
            self.health_cooldown -= 1

        # giảm thời gian nhấp nháy
        if self.blink_timer > 0:
            self.blink_timer -= 1
            if self.blink_timer % 10 < 5:  # Nhấp nháy
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        # ấn phím, di chuyển của nhân vật
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

        # hình chữ nhật người chơi
        self.rect.center = (int(self.pixel_pos[0]), int(self.pixel_pos[1]))



class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, player, algorithm, difficulty):
        super().__init__()

        # vẽ quái vật
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

        # vị trí và thông tin khởi tạo
        self.rect = self.image.get_rect()
        self.grid_pos = (grid_x, grid_y)
        self.rect.center = to_pixel_pos(grid_x, grid_y)
        self.player = player
        self.algorithm = algorithm
        self.exit_pos = exit_pos  # Lưu vị trí lối ra
        self.path = []
        self.move_timer = 0

        # cài đặt độ trễ
        if difficulty == "Easy":
            self.move_delay = 30
        elif difficulty == "Medium":
            self.move_delay = 15
        else:
            self.move_delay = 5
        self.default_move_delay = self.move_delay
        self.slow_timer = 0
        self.invisibility_timer = 0

    # trạng thái làm chậm
    def activate_slow(self):
        self.move_delay = self.default_move_delay * 2  # Làm chậm
        self.slow_timer = 5 * FPS  # 10 giây

    # trạng thái tàng hình
    def activate_invisibility(self):
        self.invisibility_timer = 5 * FPS  # 5 giây


    def update(self):
        # đặt lại tốc độ bình thường sau khi hết làm chậm
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.move_delay = self.default_move_delay

        # đặt lại trạng thái bình thường sau khi hết tàng hình
        if self.invisibility_timer > 0:
            self.invisibility_timer -= 1

        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0

            # nếu người chơi đang tàn hình
            if self.invisibility_timer > 0:
                # Di chuyển ngẫu nhiên
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                random.shuffle(directions)
                for dx, dy in directions:
                    next_pos = (self.grid_pos[0] + dx, self.grid_pos[1] + dy)
                    x, y = next_pos
                    if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1):
                        self.grid_pos = next_pos
                        self.rect.center = to_pixel_pos(next_pos[0], next_pos[1])
                        break

            # nếu người chơi không tàn hình
            else:
                # tính khoảng cách đến người chơi và lối ra
                player_dist= heuristic(self.grid_pos, tuple(self.player.grid_pos))
                exit_dist= heuristic(self.grid_pos, self.exit_pos)
                player_to_exit_dist= heuristic(tuple(self.player.grid_pos), self.exit_pos)

                # Logic thông minh cho A* và IDA*
                if self.algorithm in ["A*", "IDA*"] and player_dist>10 and player_to_exit_dist >5:
                    target_pos= self.exit_pos # chặn lối ra nếu người chơi xa
                else:
                    target_pos=tuple(self.player.grid_pos)

                player_grid_pos = tuple(self.player.grid_pos)
                if self.algorithm == "BFS":
                    self.path = bfs_search(self.grid_pos, player_grid_pos)
                elif self.algorithm == "IDS":
                    self.path = ids_search(self.grid_pos, player_grid_pos)
                elif self.algorithm == "A*":
                    self.path = a_star_search(self.grid_pos, player_grid_pos)
                elif self.algorithm == "IDA*":
                    self.path = ida_star_search(self.grid_pos, player_grid_pos)

                # nếu có đường đi thì di chuyển đến bước tiếp theo
                if len(self.path) > 1:
                    next_pos = self.path[1]
                    self.grid_pos = next_pos
                    self.rect.center = to_pixel_pos(next_pos[0], next_pos[1])

                # nếu không có đường đi thì di chuyển ngẫu nhiên
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






# Tải hình nền kết thúc game
try:
    background2 = pygame.image.load(r"asset\anh_backgound\anhdep.jpg").convert()
    background2 = pygame.transform.smoothscale(background2, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Dùng smoothscale cho chất lượng tốt hơn
except:
    background2 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background2.fill((50, 150, 50))

# tải ảnh vật phẩm
try:
    # giay tang toc
    speed_boost_img = pygame.image.load(r"asset\anh_icon\Giay.jpg").convert_alpha()
    speed_boost_img = pygame.transform.scale(speed_boost_img, (GRID_SIZE - 5, GRID_SIZE - 5))

    # lo nuoc lam cham
    slow_enemy_img = pygame.image.load(r"asset\anh_icon\lonuoc2.png").convert_alpha()
    slow_enemy_img = pygame.transform.scale(slow_enemy_img, (GRID_SIZE - 5, GRID_SIZE - 5))

    # ao choang tang hinh
    invisibility_img = pygame.image.load(r"asset\anh_icon\aochoang1.png").convert_alpha()
    invisibility_img = pygame.transform.scale(invisibility_img, (GRID_SIZE - 5, GRID_SIZE - 5))

    # hoi mau
    heal_img = pygame.image.load(r"asset\anh_icon\hoimau.png").convert_alpha()
    heal_img = pygame.transform.scale(heal_img, (GRID_SIZE - 5, GRID_SIZE - 5))

except pygame.error as e:
    print(f"Không thể tải hình ảnh vật phẩm: {e}")
    # Dùng hình mặc định nếu không tải được
    speed_boost_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    speed_boost_img.fill(BLUE)
    slow_enemy_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    slow_enemy_img.fill(WHITE)
    invisibility_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    invisibility_img.fill((128, 0, 128))
    heal_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    pygame.draw.circle(heal_img, (0, 255, 0), (12.5, 12.5), 12)

# Tải hình ảnh gai
try:
    spike_img = pygame.image.load(r"asset\anh_icon\bay.png").convert_alpha()
    spike_img = pygame.transform.scale(spike_img, (GRID_SIZE - 5, GRID_SIZE - 5))
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


# Tải hình ảnh trái bom
try:
    bomb_img = pygame.image.load(r"asset\anh_icon\traibom.jpg").convert_alpha()
    bomb_img = pygame.transform.scale(bomb_img, (GRID_SIZE - 5, GRID_SIZE - 5))
except Exception as e:
    print(f"Không thể tải hình ảnh trái bom: {e}")
    bomb_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    pygame.draw.circle(bomb_img, (100, 0, 0), (12.5, 12.5), 12)  # Hình mặc định


# tải hình ảnh tường
WALL_TEXTURE = pygame.image.load(r"asset/anh_icon/gach3.jpg").convert()
WALL_TEXTURE = pygame.transform.scale(WALL_TEXTURE, (MAZE_WIDTH, MAZE_HEIGHT))


# Tải âm thanh nổ bom
try:
    bomb_sound = pygame.mixer.Sound(r"asset\nhac\tieng_bom.mp3")
except Exception as e:
    print(f"Không thể tải âm thanh nổ bom: {e}")
    bomb_sound = None


# class hieu ung no bom
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []

        # load ảnh bomb nổ
        for i in range(5):
            try:
                img = pygame.image.load(f"asset/anh_icon/explosion/frame_{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (GRID_SIZE * 3, GRID_SIZE * 3))
                self.images.append(img)
            except pygame.error as e:
                print(f"Không thể tải frame_{i}.png: {e}")
                break

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.frame_rate = 5
        self.frame_counter = 0

    def remove_background(self, surface, color, threshold=50):
        """
        Loại bỏ màu nền (color) khỏi surface, với ngưỡng (threshold) để xác định màu gần giống.
        """
        # Tạo một surface mới với alpha channel
        new_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        new_surface.blit(surface, (0, 0))

        # Lấy dữ liệu pixel
        pixel_array = pygame.PixelArray(new_surface)
        target_r, target_g, target_b = color

        # Duyệt qua từng pixel
        for x in range(new_surface.get_width()):
            for y in range(new_surface.get_height()):
                pixel_color = new_surface.unmap_rgb(pixel_array[x, y])
                r, g, b, a = pixel_color.r, pixel_color.g, pixel_color.b, pixel_color.a

                # Tính khoảng cách màu (Euclidean distance trong không gian RGB)
                color_distance = ((r - target_r) ** 2 + (g - target_g) ** 2 + (b - target_b) ** 2) ** 0.5

                # Nếu màu gần với màu cam mục tiêu, làm trong suốt
                if color_distance < threshold:
                    pixel_array[x, y] = (0, 0, 0, 0)  # Trong suốt (alpha = 0)

        del pixel_array
        return new_surface

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_rate:
            self.frame_counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]



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


# Menu chọn thuật toán, chế độ chơi và bản đồ
def menu_screen():
    menu_active = True
    difficulty_options = ["Easy", "Medium", "Hard"]
    selected_difficulty = 0

    try:
        menu_background = pygame.image.load(r"asset\anh_backgound\a1.jpg").convert()
        menu_background = pygame.transform.scale(menu_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        print(f"Không thể tải menu_background.png: {e}")
        menu_background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        menu_background.fill(DARK_BLUE)

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_giao_dien.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải menu_music.mp3")

    title_font = pygame.font.Font(None, 74)
    option_font = pygame.font.Font(None, 50)

    while menu_active:
        screen.blit(menu_background, (0, 0))
        title_text = title_font.render("Pursuit Game", True, YELLOW)
        title_shadow = title_font.render("Pursuit Game", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2+300, WINDOW_HEIGHT // 4-50))

        # Vẽ bóng (lệch xuống dưới và sang phải 3 pixel)
        screen.blit(title_shadow, title_rect.move(3, 3))

        screen.blit(title_text, title_rect)


        for i, difficulty in enumerate(difficulty_options):
            color = YELLOW if i == selected_difficulty else WHITE
            text = option_font.render(difficulty, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2+290, WINDOW_HEIGHT // 2 + i * 60-130))
            screen.blit(text, text_rect)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulty_options)
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                elif event.key == pygame.K_RETURN:
                    return difficulty_options[selected_difficulty]
                elif event.key == pygame.K_ESCAPE:
                    return None

    return None

# Game Over
def game_over_screen(final_score):
    pygame.mixer.music.stop()
    screen.blit(background2, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(120)
    screen.blit(overlay, (0, 0))

    # tiêu đề
    game_over_text = font_large.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    replay_text = font.render("Press R to Replay", True, WHITE)

    # căn chỉnh
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + 20))

    # vẽ nền cho chữ, hiển thị lên màn hình
    for text, rect in [(game_over_text, game_over_rect), (score_text, score_rect), (replay_text, replay_rect)]:
        bg = pygame.Surface((rect.width + 20, rect.height + 10))
        bg.fill(BLACK)
        bg.set_alpha(100)
        screen.blit(bg, (rect.x - 10, rect.y - 5))
        screen.blit(text, rect)

    pygame.display.flip()

    # chờ người chơi thoát
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
    pygame.mixer.music.stop()
    if victory_sound:
        victory_sound.play()

    screen.blit(background2, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(100)
    screen.blit(overlay, (0, 0))

    victory_text = font_large.render("You Win!", True, YELLOW)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    replay_text = font.render("Press R to Replay, Q to Quit", True, WHITE)  # Thêm "Q to Quit"

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
                    if victory_sound:
                        victory_sound.stop()
                    return True
                elif event.key == pygame.K_q:
                    if victory_sound:
                        victory_sound.stop()
                    return False
    return False


# Vẽ bảng thông tin
def draw_hud(score, difficulty, stage_info, player):
    hud_font = pygame.font.Font(None, 36)

    # Thanh máu
    pygame.draw.rect(screen, RED, (10, 190, 150, 12))
    health_width = (player.health / player.max_health) * 150
    pygame.draw.rect(screen, GREEN, (10, 190, health_width, 12))
    pygame.draw.rect(screen, BLACK, (10, 190, 150, 12), 2)

    # Điểm số
    score_text = hud_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 40))

    # Độ khó
    difficulty_text = hud_font.render(f"Difficulty: {difficulty}", True, WHITE)
    screen.blit(difficulty_text, (10, 70))

    # Stage và Map
    stage_text = hud_font.render(stage_info, True, WHITE)
    screen.blit(stage_text, (10, 100))

    # Thuật toán hiện tại (lấy từ STAGE_ALGORITHMS)
    current_stage = int(stage_info.split("Stage ")[1].split(":")[0]) - 1
    map_name = stage_info.split(": ")[1]
    map_idx = STAGES[current_stage].index(map_name)
    algorithm = STAGE_ALGORITHMS[current_stage][map_idx]
    algorithm_text = hud_font.render(f"Enemy AI: {algorithm}", True, WHITE)
    screen.blit(algorithm_text, (10, 130))

    # Số bom
    bomb_text = hud_font.render(f"Bombs: {player.bombs}", True, WHITE)
    screen.blit(bomb_text, (10, 160))

# giao diện chuyển màn chơi
def stage_transition_screen(completed_stage, next_stage, score):
    screen.blit(background2, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(100)
    screen.blit(overlay, (0, 0))

    completed_text = font_large.render(f"Stage {completed_stage} Completed!", True, YELLOW)
    next_text = font.render(f"Next: Stage {next_stage}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    continue_text = font_small.render("Press ENTER to Continue", True, WHITE)

    completed_rect = completed_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    next_rect = next_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3))

    for text, rect in [(completed_text, completed_rect), (next_text, next_rect),
                       (score_text, score_rect), (continue_text, continue_rect)]:
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
                if event.key == pygame.K_RETURN:
                    return True
    return False

MAP_BACKGROUNDS = {
    "Me cung": r"asset\anh_backgound\map1.webp",
    "Can ho": r"asset\anh_backgound\map2.jpg",
    "Khach san": r"asset\anh_backgound\map3.jpg",
    "Rung sau": r"asset\anh_backgound\map4.jpg",
    "Nha may": r"asset\anh_backgound\map5.jpg",
    "Thanh pho": r"asset\anh_backgound\map6.jpg",
    # "Hang dong": r"asset\anh_backgound\hang_dong.jpg",
    # "Cau truc": r"asset\anh_backgound\cau_truc.jpg",
    # "La ma": r"asset\anh_backgound\la_ma.jpg",
}
# Định nghĩa các màn chơi
STAGES = [
    ["Me cung", "Can ho"],  # Stage 1
    ["Khach san", "Rung sau"],  # Stage 2
    ["Nha may", "Thanh pho"],   # Stage 3
]

STAGE_ALGORITHMS = [
    ["BFS", "IDS"],   # Stage 0: Uninformed Search
    ["A*", "IDA*"],   # Stage 1: Informed Search
    ["A*", "IDA*"],   # Stage 2: Informed Search (tạm thời, có thể thay sau)
]


# Vòng lặp game chính
running = True
while running:
    difficulty = menu_screen()
    if difficulty is None:
        break

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_choi_game.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải gameplay_music.mp3")

    score = 0
    current_stage = 0
    game_active = True

    while game_active and current_stage < len(STAGES):
        current_map_idx = 0
        map_order = STAGES[current_stage]

        while game_active and current_map_idx < len(map_order):
            # Tải bản đồ
            load_map(map_order[current_map_idx])

            # Chọn thuật toán dựa trên stage và map
            algorithm = STAGE_ALGORITHMS[current_stage][current_map_idx]

            # Tải hình nền tương ứng với bản đồ
            try:
                game_background = pygame.image.load(MAP_BACKGROUNDS[map_order[current_map_idx]]).convert()
                game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
            except Exception as e:
                print(f"Không thể tải hình nền cho {map_order[current_map_idx]}: {e}")
                game_background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                game_background.fill(DARK_BLUE)

            all_sprites = pygame.sprite.Group()
            enemies = pygame.sprite.Group()

            # Vị trí cố định cho người chơi và quái vật
            player_pos = (1, 1)
            enemy_pos = (18, 1)

            # Kiểm tra xem vị trí có hợp lệ không
            if grid[player_pos[1]][player_pos[0]] != 1 and grid[enemy_pos[1]][enemy_pos[0]] != 1:
                player = Player(player_pos[0], player_pos[1])
                exit_pos = get_exit_position()
                enemy = Enemy(enemy_pos[0], enemy_pos[1], player, algorithm, difficulty)
            else:
                print("Vị trí cố định không hợp lệ, quay lại chọn ngẫu nhiên.")
                player_pos = get_empty_position()
                player = Player(player_pos[0], player_pos[1])
                exit_pos = get_exit_position()
                enemy_pos = get_empty_position()
                while enemy_pos == player_pos:
                    enemy_pos = get_empty_position()
                enemy = Enemy(enemy_pos[0], enemy_pos[1], player, algorithm, difficulty)

            all_sprites.add(player, enemy)
            enemies.add(enemy)

            exit_pos = get_exit_position()

            # Điều chỉnh số lượng vật phẩm và gai theo độ khó của màn
            num_items = max(8 - current_stage, 1)  # Giảm vật phẩm khi màn tăng
            num_spikes = 5 + current_stage  # Tăng gai khi màn tăng
            spawn_items(grid, player_pos, enemy_pos, exit_pos, num_items=num_items, num_spikes=num_spikes)

            while game_active:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_active = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b:
                            player.use_bomb()

                all_sprites.update()
                score += 1

                # Vẽ mọi thứ
                screen.blit(game_background, (0, 0))
                # Vẽ WALL_TEXTURE làm nền cho mê cung
                screen.blit(WALL_TEXTURE, (MAZE_OFFSET_X, MAZE_OFFSET_Y))

                draw_grid(exit_pos)
                all_sprites.draw(screen)
                draw_hud(score, difficulty, f"Stage {current_stage + 1}: {map_order[current_map_idx]}", player)
                pygame.display.flip()

                # Xử lý va chạm với quái vật
                if pygame.sprite.spritecollide(player, enemies, False):
                    if collision_sound:
                        collision_sound.play()
                    game_active = False

                tam = 0
                if tuple(player.grid_pos) == exit_pos:
                    current_map_idx += 1
                    if current_map_idx >= len(map_order):
                        if current_stage + 1 < len(STAGES):
                            # Hiển thị giao diện chuyển màn
                            continue_game = stage_transition_screen(current_stage + 1, current_stage + 2, score)
                            if not continue_game:
                                running = False
                                game_active = False
                            current_stage += 1
                        else:
                            # Đã hoàn thành tất cả các stage
                            replay = victory_screen(score)
                            if replay:  # Nếu bấm R, quay lại menu
                                game_active = False
                                # Đặt lại trạng thái để bắt đầu game mới
                                score = 0
                                current_stage = 0
                                break  # Thoát vòng lặp trong cùng
                            else:  # Nếu bấm Q, thoát game hoàn toàn
                                running = False
                                game_active = False
                                break
                    break

                player_grid_x, player_grid_y = player.grid_pos
                item = grid[player_grid_y][player_grid_x]
                if item in [3, 4, 5, 6, 7, 8]:
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
                    elif item == 7:
                        player.add_bomb()
                    elif item == 8:
                        player.heal(20)
                    if item != 6:
                        grid[player_grid_y][player_grid_x] = 0

                if player.health <= 0:
                    if collision_sound:
                        collision_sound.play()
                    game_active = False

        # Chỉ gọi game_over_screen nếu người chơi thua (game_active = False) và chưa hoàn thành tất cả stage
        if running and game_active == False :
            replay = game_over_screen(score)
            if not replay:
                running = False
            else:
                # Đặt lại trạng thái để quay lại menu
                score = 0
                current_stage = 0
                break

pygame.quit()