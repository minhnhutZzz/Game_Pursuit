import json
import time
import pygame
import random
import heapq
from heapq import heappush, heappop
import math
from collections import deque
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
import uuid



current_map_index = 0  # Cập nhật biến này trong game loop khi chuyển map

# Từ điển lưu dữ liệu hiệu suất cho map đầu tiên
performance_data = {
    'BFS': {'states': 0, 'time': 0.0},
    'IDS': {'states': 0, 'time': 0.0},
    'A*': {'states': 0, 'time': 0.0},
    'IDA*': {'states': 0, 'time': 0.0},
    'Simulated Annealing': {'states': 0, 'time': 0.0},
    'Beam Search': {'states': 0, 'time': 0.0}
}

video_path = os.path.abspath("asset/anh_background/background1.mp4")
cap = cv2.VideoCapture(video_path)
print("Đường dẫn tuyệt đối:", video_path)

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
hongdam=(255, 20, 149)
hongnhat=(253, 38, 252)


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
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
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
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
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
            elif grid[y][x]==8: # máu
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(heal_img, (rect.x+2.5, rect.y+2.5))
            elif grid[y][x] == 9:  # Chìa khóa
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(key_img, (rect.x + 2.5, rect.y + 2.5))
            elif grid[y][x] == 10:  # Ngôi sao
                pygame.draw.rect(screen, LIGHT_GREEN, rect)
                screen.blit(star_img, (rect.x + 2.5, rect.y + 2.5))
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
    key_placed = False
    stars_placed = 0

    # Sinh chìa khóa trước
    while not key_placed:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        pos = (x, y)
        if (grid[y][x] == 0 and pos != player_pos and pos != enemy_pos and pos != exit_pos):
            grid[y][x] = 9  # Giá trị cho chìa khóa
            key_placed = True

        # Sinh 3 ngôi sao
        while stars_placed < 3:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            pos = (x, y)
            if (grid[y][x] == 0 and pos != player_pos and pos != enemy_pos and pos != exit_pos):
                grid[y][x] = 10  # Giá trị cho ngôi sao
                stars_placed += 1



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
    came_from = {start: None}
    visited = {start}
    states_explored = 1  # Đếm số trạng thái (nút) được khám phá

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1 and
                    next_pos not in visited):
                queue.append(next_pos)
                visited.add(next_pos)
                came_from[next_pos] = current
                states_explored += 1  # Tăng số trạng thái mỗi khi thêm nút mới

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            print("BFS không tìm thấy đường đi")  # Debug
            return [], states_explored
    path.append(start)
    path.reverse()
    for x, y in path:
        if grid[y][x] == 1:
            print(f"Lỗi: Đường đi BFS chứa ô tường tại ({x}, {y})")  # Debug
            return [], states_explored
    print(f"Đường đi BFS: {path}, States: {states_explored}")  # Debug
    return path, states_explored

# IDS
def ids_search(start, goal):
    def dls(node, goal, depth, came_from, visited):
        nonlocal states_explored
        if depth < 0:
            return False, None
        if node == goal:
            return True, node
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (node[0] + dx, node[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1 and
                    next_pos not in visited):
                visited.add(next_pos)
                came_from[next_pos] = node
                states_explored += 1  # Tăng số trạng thái mỗi khi xem xét nút mới
                found, result = dls(next_pos, goal, depth - 1, came_from, visited)
                if found:
                    return True, result
        return False, None

    depth = 0
    states_explored = 1  # Đếm nút ban đầu
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
                    print("IDS không tìm thấy đường đi")  # Debug
                    return [], states_explored
            path.append(start)
            path.reverse()
            for x, y in path:
                if grid[y][x] == 1:
                    print(f"Lỗi: Đường đi IDS chứa ô tường tại ({x}, {y})")  # Debug
                    return [], states_explored
            print(f"Đường đi IDS: {path}, States: {states_explored}")  # Debug
            return path, states_explored
        depth += 1

# A*
def a_star_search(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    states_explored = 1  # Đếm nút ban đầu

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
                    states_explored += 1  # Tăng số trạng thái mỗi khi thêm nút mới
            else:
                print(f"Bỏ qua ô ({x}, {y}) vì là tường hoặc ngoài lưới")  # Debug

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            print("A* không tìm thấy đường đi")  # Debug
            return [], states_explored
    path.append(start)
    path.reverse()
    for x, y in path:
        if grid[y][x] == 1:
            print(f"Lỗi: Đường đi A* chứa ô tường tại ({x}, {y})")  # Debug
            return [], states_explored
    print(f"Đường đi A*: {path}, States: {states_explored}")  # Debug
    return path, states_explored

# IDA*
def ida_star_search(start, goal):
    def search(node, g, threshold, came_from):
        nonlocal states_explored
        f = g + heuristic(node, goal)
        if f > threshold:
            return f, None
        if node == goal:
            return f, node
        min_f = float('inf')
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (node[0] + dx, node[1] + dy)
            x, y = next_pos
            if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1 and
                    next_pos not in came_from):
                came_from[next_pos] = node
                states_explored += 1  # Tăng số trạng thái mỗi khi xem xét nút mới
                new_f, result = search(next_pos, g + 1, threshold, came_from)
                if result is not None:
                    return new_f, result
                min_f = min(min_f, new_f)
                del came_from[next_pos]
        return min_f, None

    threshold = heuristic(start, goal)
    states_explored = 1  # Đếm nút ban đầu
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
            for x, y in path:
                if grid[y][x] == 1:
                    print(f"Lỗi: Đường đi IDA* chứa ô tường tại ({x}, {y})")  # Debug
                    return [], states_explored
            print(f"Đường đi IDA*: {path}, States: {states_explored}")  # Debug
            return path, states_explored
        if new_threshold == float('inf'):
            print("IDA* không tìm thấy đường đi")  # Debug
            return [], states_explored
        threshold = new_threshold


# --- Thuật toán Simulated Annealing ---
def get_neighbors(pos):
    x, y = pos
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] != 1]

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])




def simulated_annealing_search(start, goal):
    max_iterations = 400
    initial_temp = 50
    cooling_rate = 0.9995
    current_path = [start]
    current_pos = start
    best_path = current_path[:]
    best_cost = manhattan_distance(start, goal)
    temp = initial_temp
    last_good_path = best_path[:]
    states_explored = 1  # Đếm trạng thái ban đầu

    # Khởi tạo đường đi ban đầu
    for _ in range(50):
        neighbors = get_neighbors(current_pos)
        if not neighbors:
            break
        neighbors_with_cost = [(n, manhattan_distance(n, goal)) for n in neighbors]
        neighbors_with_cost.sort(key=lambda x: x[1])
        next_pos = neighbors_with_cost[0][0]
        current_path.append(next_pos)
        current_pos = next_pos
        states_explored += len(neighbors)  # Đếm số hàng xóm được xem xét
        new_cost = manhattan_distance(next_pos, goal)
        if new_cost < best_cost:
            best_path = current_path[:]
            best_cost = new_cost
            last_good_path = best_path[:]
        if current_pos == goal:
            print(f"Đạt mục tiêu trong giai đoạn khởi tạo: {best_path}")  # Debug
            return best_path, states_explored

    # Giai đoạn Simulated Annealing
    for i in range(max_iterations):
        if current_pos == goal:
            print(f"Đạt mục tiêu ở vòng lặp {i}: {best_path}")  # Debug
            return best_path, states_explored
        neighbors = get_neighbors(current_pos)
        if not neighbors:
            print(f"Không có hàng xóm tại {current_pos}, dùng last_good_path")  # Debug
            break
        neighbors_with_cost = [(n, manhattan_distance(n, goal)) for n in neighbors]
        neighbors_with_cost.sort(key=lambda x: x[1])
        if random.random() < 0.9:
            next_pos = neighbors_with_cost[0][0]
        else:
            next_pos = random.choice(neighbors)
        states_explored += len(neighbors)  # Đếm số hàng xóm được xem xét

        new_path = current_path + [next_pos]
        new_cost = manhattan_distance(next_pos, goal)

        if new_cost <= best_cost or random.random() < math.exp((best_cost - new_cost) / temp):
            current_path = new_path
            current_pos = next_pos
            if new_cost < best_cost:
                best_path = new_path[:]
                best_cost = new_cost
                last_good_path = best_path[:]
                print(f"Cải thiện đường đi ở vòng lặp {i}, cost: {best_cost}, path: {best_path}")  # Debug
            elif new_cost == best_cost:
                last_good_path = new_path[:]
        temp *= cooling_rate

    if best_path[-1] == goal:
        print(f"Trả về best_path đạt mục tiêu: {best_path}")  # Debug
        return best_path, states_explored
    elif last_good_path and len(last_good_path) > 1 and manhattan_distance(last_good_path[-1], goal) < manhattan_distance(start, goal):
        print(f"Trả về last_good_path tiến gần mục tiêu: {last_good_path}")  # Debug
        return last_good_path, states_explored
    else:
        bfs_path, bfs_states = bfs_search(start, goal)
        states_explored += bfs_states
        print(f"Simulated Annealing thất bại, dùng BFS: {bfs_path}")  # Debug
        return bfs_path if bfs_path else last_good_path, states_explored





# --- Thuật toán Beam Search ---
def beam_search(start, goal):
    beam_width = 5
    queue = [(manhattan_distance(start, goal), [start])]
    visited = set()
    states_explored = 1  # Đếm trạng thái ban đầu

    while queue:
        new_queue = []
        for _ in range(min(len(queue), beam_width)):
            if not queue:
                break
            _, path = heappop(queue)
            current = path[-1]
            if current == goal:
                return path, states_explored
            if current in visited:
                continue
            visited.add(current)
            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    heappush(new_queue, (manhattan_distance(neighbor, goal), new_path))
                    states_explored += 1  # Tăng số trạng thái mỗi khi thêm nút mới
        queue = new_queue
    path, bfs_states = bfs_search(start, goal)
    states_explored += bfs_states
    return path, states_explored


class Player(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        super().__init__()
        try:
            self.image = pygame.image.load(r"asset/skin/player6.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
        except Exception as e:
            print(f"Không thể tải player6.png: {e}")
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

        self.speed = 120  # Tốc độ pixel/giây (tương đương ~4 pixel/frame ở 60 FPS trước đây)
        self.default_speed = 120
        self.speed_boost_timer = 0
        self.slow_timer = 0
        self.health = 100
        self.max_health = 100
        self.health_cooldown = 0
        self.original_image = self.image.copy()
        self.blink_timer = 0
        self.bombs = 0
        self.b_key_pressed = False
        self.has_key = False
        self.unlock_timer = 0
        self.show_key_message_timer = 0
        self.stars_collected = 0
        self.moving = False
        self.target_pixel_pos = self.pixel_pos[:]
        self.direction = (0, 0)

    def pick_star(self):
        self.stars_collected += 1
        global total_stars
        total_stars += 1
        if pickup_sound:
            pickup_sound.play()

    def pick_key(self):
        self.has_key = True
        if pickup_sound:
            pickup_sound.play()

    def add_bomb(self):
        self.bombs += 1
        if pickup_sound:
            pickup_sound.play()

    def use_bomb(self):
        if self.bombs > 0:
            self.bombs -= 1
            if bomb_sound:
                bomb_sound.play()
            explosion = Explosion(self.pixel_pos[0], self.pixel_pos[1])
            all_sprites.add(explosion)
            px, py = self.grid_pos
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = px + dx, py + dy
                    if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] == 1):
                        if not (nx == 0 or nx == GRID_WIDTH - 1 or ny == 0 or ny == GRID_HEIGHT - 1):
                            grid[ny][nx] = 0
            # Làm mới đường đi cho tất cả kẻ thù
            for enemy in enemies:
                enemy.path = []
                enemy.moving = False
                enemy.path_update_timer = enemy.path_update_interval  # Buộc cập nhật ngay

    def activate_speed_boost(self):
        self.speed = 180  # Tăng tốc lên 180 pixel/giây
        self.speed_boost_timer = 5 * FPS
        if pickup_sound:
            pickup_sound.play()

    def hit_spike(self):
        if self.health_cooldown <= 0:
            self.health -= 20
            self.speed = 90  # Giảm tốc xuống 90 pixel/giây
            self.slow_timer = 5 * FPS
            self.health_cooldown = 1 * FPS
            self.blink_timer = 1 * FPS
            if spike_sound:
                spike_sound.play()
            if self.health < 0:
                self.health = 0

    def heal(self, amount=30):
        self.health = min(self.max_health, self.health + amount)
        if pickup_sound:
            pickup_sound.play()

    def update(self):
        delta_time = clock.get_time() / 1000.0  # Thời gian giữa các khung hình (giây)

        # Xử lý trạng thái tăng tốc
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed = self.default_speed

        # Xử lý trạng thái làm chậm
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.speed = self.default_speed

        # Xử lý thời gian hồi phục
        if self.health_cooldown > 0:
            self.health_cooldown -= 1

        # Xử lý thời gian nhấp nháy
        if self.blink_timer > 0:
            self.blink_timer -= 1
            if self.blink_timer % 10 < 5:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        # Xử lý thời gian mở cửa
        if self.unlock_timer > 0:
            self.unlock_timer -= 1

        # Xử lý thời gian hiển thị thông báo thiếu chìa khóa
        if self.show_key_message_timer > 0:
            self.show_key_message_timer -= 1

        # Xử lý di chuyển
        keys = pygame.key.get_pressed()
        new_direction = (0, 0)

        # Xác định hướng di chuyển mới
        if keys[pygame.K_LEFT]:
            new_direction = (-1, 0)
        elif keys[pygame.K_RIGHT]:
            new_direction = (1, 0)
        if keys[pygame.K_UP]:
            new_direction = (0, -1)
        elif keys[pygame.K_DOWN]:
            new_direction = (0, 1)

        # Nếu đang di chuyển, tiếp tục đến đích
        if self.moving:
            dx = self.target_pixel_pos[0] - self.pixel_pos[0]
            dy = self.target_pixel_pos[1] - self.pixel_pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            speed = self.speed * delta_time  # Tốc độ điều chỉnh theo delta time
            if distance > speed:
                speed_x = (dx / distance) * speed
                speed_y = (dy / distance) * speed
                self.pixel_pos[0] += speed_x
                self.pixel_pos[1] += speed_y
            else:
                self.pixel_pos = self.target_pixel_pos[:]
                self.grid_pos[0] += self.direction[0]
                self.grid_pos[1] += self.direction[1]
                self.moving = False
                self.direction = (0, 0)

        # Nếu không di chuyển, kiểm tra hướng mới
        if not self.moving and new_direction != (0, 0):
            target_grid_x = self.grid_pos[0] + new_direction[0]
            target_grid_y = self.grid_pos[1] + new_direction[1]
            if (0 <= target_grid_x < GRID_WIDTH and 0 <= target_grid_y < GRID_HEIGHT and
                    grid[target_grid_y][target_grid_x] != 1):
                self.moving = True
                self.direction = new_direction
                self.target_pixel_pos = list(to_pixel_pos(target_grid_x, target_grid_y))

        self.rect.center = (int(self.pixel_pos[0]), int(self.pixel_pos[1]))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y, player, algorithm, difficulty):
        super().__init__()
        try:
            self.image = pygame.image.load("asset/skin/kethu3.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (28, 28))
            print("Loaded kethu3.png successfully")
        except Exception as e:
            print(f"Failed to load kethu3.png: {e}")
            self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
            pygame.draw.circle(self.image, RED, (14, 14), 14)
            pygame.draw.circle(self.image, BLACK, (12, 12), 3)
            pygame.draw.circle(self.image, BLACK, (16, 12), 3)

        self.rect = self.image.get_rect(center=to_pixel_pos(grid_x, grid_y))
        self.grid_pos = [grid_x, grid_y]
        self.pixel_pos = list(to_pixel_pos(grid_x, grid_y))
        self.player = player
        self.speed = 90
        self.default_speed = 90
        self.slow_timer = 0
        self.invisibility_timer = 0
        self.algorithm = algorithm  # Lưu thuật toán được chọn
        self.difficulty = difficulty
        self.path = []
        self.last_path = []
        self.target_pixel_pos = self.pixel_pos[:]
        self.moving = False
        self.path_update_timer = 0
        self.path_update_interval = FPS // 5

        if difficulty == "Easy":
            self.speed = 60
        elif difficulty == "Medium":
            self.speed = 90
        else:
            self.speed = 120
        self.default_speed = self.speed

        self.exit_pos = get_exit_position()

    def activate_slow(self):
        self.speed = self.default_speed * 0.5
        self.slow_timer = 5 * FPS
        if pickup_sound:
            pickup_sound.play()

    def activate_invisibility(self):
        self.invisibility_timer = 5 * FPS
        if pickup_sound:
            pickup_sound.play()

    def update(self):
        delta_time = clock.get_time() / 1000.0

        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.speed = self.default_speed

        if self.invisibility_timer > 0:
            self.invisibility_timer -= 1
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

        self.path_update_timer += 1
        if self.path_update_timer >= self.path_update_interval:
            self.path_update_timer = 0
            print(f"Đang cập nhật đường đi cho kẻ thù tại {self.grid_pos}")  # Debug

            if self.invisibility_timer > 0:
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                random.shuffle(directions)
                for dx, dy in directions:
                    next_pos = (self.grid_pos[0] + dx, self.grid_pos[1] + dy)
                    x, y = next_pos
                    if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1):
                        self.path = [self.grid_pos[:], list(next_pos)]
                        self.target_pixel_pos = list(to_pixel_pos(next_pos[0], next_pos[1]))
                        self.moving = True
                        print(f"Chọn di chuyển ngẫu nhiên đến {next_pos}")  # Debug
                        break
                else:
                    print("Không tìm thấy ô hợp lệ để di chuyển ngẫu nhiên")  # Debug
            else:
                target_pos = tuple(self.player.grid_pos)
                print(f"Mục tiêu: {target_pos}, thuật toán: {self.algorithm}")  # Debug
                # Gọi choose_algorithm với thuật toán đã chọn
                self.path, _ = choose_algorithm(tuple(self.grid_pos), target_pos, self.algorithm)

                if self.path and len(self.path) > 1:
                    self.last_path = self.path[:]
                    print(f"Đường đi mới: {self.path}")  # Debug
                else:
                    self.path = self.last_path[:] if self.last_path else []
                    print(f"Không tìm thấy đường đi mới, sử dụng last_path: {self.path}")  # Debug

                if len(self.path) > 1:
                    next_grid_pos = self.path[1]
                    x, y = next_grid_pos
                    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1:
                        self.target_pixel_pos = list(to_pixel_pos(next_grid_pos[0], next_grid_pos[1]))
                        self.moving = True
                    else:
                        self.path = self.last_path[:] if self.last_path else []
                        print(f"Đường đi chứa ô tường tại ({x}, {y}), sử dụng last_path")  # Debug
                else:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    random.shuffle(directions)
                    for dx, dy in directions:
                        next_pos = (self.grid_pos[0] + dx, self.grid_pos[1] + dy)
                        x, y = next_pos
                        if (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1):
                            self.path = [self.grid_pos[:], list(next_pos)]
                            self.target_pixel_pos = list(to_pixel_pos(next_pos[0], next_pos[1]))
                            self.moving = True
                            print(f"Không có đường đi, chọn ngẫu nhiên đến {next_pos}")  # Debug
                            break
                    else:
                        self.moving = False
                        print("Không tìm thấy ô hợp lệ")  # Debug

        if self.moving and len(self.path) > 1:
            dx = self.target_pixel_pos[0] - self.pixel_pos[0]
            dy = self.target_pixel_pos[1] - self.pixel_pos[1]
            distance = max(abs(dx), abs(dy))

            speed = self.speed * delta_time
            if distance > speed:
                if abs(dx) > abs(dy):
                    speed_x = speed if dx > 0 else -speed
                    speed_y = 0
                else:
                    speed_x = 0
                    speed_y = speed if dy > 0 else -speed
                self.pixel_pos[0] += speed_x
                self.pixel_pos[1] += speed_y
            else:
                self.pixel_pos = self.target_pixel_pos[:]
                next_grid_pos = self.path[1]
                x, y = next_grid_pos
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1:
                    self.grid_pos = list(next_grid_pos)
                    self.path.pop(0)
                    self.pixel_pos = list(to_pixel_pos(self.grid_pos[0], self.grid_pos[1]))
                    if len(self.path) > 1:
                        next_grid_pos = self.path[1]
                        x, y = next_grid_pos
                        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] != 1:
                            self.target_pixel_pos = list(to_pixel_pos(next_grid_pos[0], next_grid_pos[1]))
                        else:
                            self.path = self.last_path[:] if self.last_path else []
                            self.moving = False
                            print(f"Ô tiếp theo ({x}, {y}) là tường, sử dụng last_path")  # Debug
                    else:
                        self.moving = False
                        print("Hết đường đi")  # Debug
                else:
                    self.path = self.last_path[:] if self.last_path else []
                    self.moving = False
                    print(f"Ô đích ({x}, {y}) là tường, sử dụng last_path")  # Debug

            self.rect.center = (int(self.pixel_pos[0]), int(self.pixel_pos[1]))
        else:
            print(f"Kẻ thù tại {self.grid_pos} không di chuyển (moving = False)")  # Debug



# Lưu dữ liệu hiệu suất
# def save_performance(algorithm, difficulty, map_name, score, stars, time_taken):
#     global performance_data
#     performance_data.append({
#         'algorithm': algorithm,
#         'difficulty': difficulty,
#         'map': map_name,
#         'score': score,
#         'stars': stars,
#         'time': time_taken,
#         'id': str(uuid.uuid4())
#     })

def choose_algorithm(start, goal, selected_algorithm):
    global performance_data, current_map_index

    if not hasattr(choose_algorithm, "measured_algorithms"):
        choose_algorithm.measured_algorithms = set()

    algorithm = selected_algorithm
    print(f"Running {algorithm} on map {current_map_index}")  # Debug

    start_time = time.perf_counter()
    path = []
    states_explored = 0

    if algorithm == 'BFS':
        path, states_explored = bfs_search(start, goal)
    elif algorithm == 'IDS':
        path, states_explored = ids_search(start, goal)
    elif algorithm == 'A*':
        path, states_explored = a_star_search(start, goal)
    elif algorithm == 'IDA*':
        path, states_explored = ida_star_search(start, goal)
    elif algorithm == 'Simulated Annealing':
        path, states_explored = simulated_annealing_search(start, goal)
    elif algorithm == 'Beam Search':
        path, states_explored = beam_search(start, goal)

    end_time = time.perf_counter()
    runtime_ms = (end_time - start_time) * 1000  # Chuyển sang mili giây

    if current_map_index == 0 and algorithm not in choose_algorithm.measured_algorithms:
        performance_data[algorithm]['states'] = states_explored
        performance_data[algorithm]['time'] = runtime_ms
        choose_algorithm.measured_algorithms.add(algorithm)
        print(f"Updated performance_data for {algorithm}: {performance_data[algorithm]}")  # Debug

    return path, algorithm




# Định nghĩa custom_ylim ở cấp độ toàn cục
def custom_ylim(data):
    max_value = max(data) if data else 1
    upper_limit = max(max_value * 1.1, 0.01)
    return (0, upper_limit)



def plot_comparison():
    global performance_data

    print("Performance data:", performance_data)

    algorithms = ['BFS', 'IDS', 'A*', 'IDA*', 'Simulated Annealing', 'Beam Search']
    states_explored = [performance_data[algo]['states'] for algo in algorithms]
    runtimes = [performance_data[algo]['time'] for algo in algorithms]

    print("States explored per algorithm:", dict(zip(algorithms, states_explored)))  # Debug

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    # Biểu đồ 1: Số trạng thái được khám phá
    ax1.bar(algorithms, states_explored, color='skyblue')
    ax1.set_title('Number of States Explored (First Map)')
    ax1.set_xlabel('Algorithm')
    ax1.set_ylabel('States Explored')
    ax1.set_ylim(custom_ylim(states_explored))
    ax1.tick_params(axis='x', rotation=45)
    for i, v in enumerate(states_explored):
        ax1.text(i, v, str(v), ha='center', va='bottom')

    # Biểu đồ 2: Thời gian chạy (mili giây)
    ax2.bar(algorithms, runtimes, color='lightcoral')
    ax2.set_title('Runtime (First Map)')
    ax2.set_xlabel('Algorithm')
    ax2.set_ylabel('Time (ms)')
    ax2.set_ylim(custom_ylim(runtimes))
    ax2.tick_params(axis='x', rotation=45)
    for i, v in enumerate(runtimes):
        ax2.text(i, v, f'{v:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()



# def plot_comparison(difficulty, map_name):
#     algorithms = ["BFS", "A*"]  # Chỉ sử dụng BFS và A* để đơn giản
#     scores = {alg: [] for alg in algorithms}
#     stars = {alg: [] for alg in algorithms}
#     times = {alg: [] for alg in algorithms}
#
#     for data in performance_data:
#         if data['difficulty'] == difficulty and data['map'] == map_name:
#             alg = data['algorithm']
#             if alg in algorithms:
#                 scores[alg].append(data['score'])
#                 stars[alg].append(data['stars'])
#                 times[alg].append(data['time'])
#
#     plt.figure(figsize=(12, 8))
#     metrics = ['Score', 'Stars', 'Time (s)']
#     colors = ['blue', 'green', 'red']
#     x = np.arange(len(algorithms))
#
#     for i, metric in enumerate(metrics):
#         values = [np.mean(scores[alg]) if scores[alg] else 0 for alg in algorithms] if metric == 'Score' else \
#                  [np.mean(stars[alg]) if stars[alg] else 0 for alg in algorithms] if metric == 'Stars' else \
#                  [np.mean(times[alg]) if times[alg] else 0 for alg in algorithms]
#         plt.bar(x + i*0.25, values, 0.25, label=metric, color=colors[i])
#
#     plt.xlabel('Algorithm')
#     plt.ylabel('Value')
#     plt.title(f'Algorithm Comparison (Difficulty: {difficulty}, Map: {map_name})')
#     plt.xticks(x + 0.25, algorithms)
#     plt.legend()
#     plt.savefig('comparison.png')
#     plt.close()
#
# # Hiển thị biểu đồ
# def comparison_screen(difficulty, map_name):
#     plot_comparison(difficulty, map_name)
#     try:
#         img = pygame.image.load('comparison.png')
#         img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
#     except:
#         img = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
#         img.fill(BLACK)
#         text = font_large.render("No data available", True, WHITE)
#         img.blit(text, text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)))
#
#     running = True
#     while running:
#         screen.blit(img, (0, 0))
#         pygame.display.flip()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#                 return False
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#                 return True
#         clock.tick(FPS)
#     return False

# Tải video (đoạn code của bạn)
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
    print(f"Đã tải {len(background_frames)} khung hình từ video.")
except Exception as e:
    print(f"Lỗi khi tải video: {e}")
    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background.fill((50, 150, 50))
    background_frames = [background]

# Biến để theo dõi khung hình
frame_index = 0
FPS = 30  # Tốc độ khung hình (có thể điều chỉnh theo video gốc)

instructions = [
    "Arrow Keys: Move",
    "B: Use Bomb",
    "Collect Key to Exit",
    "Avoid Enemies and Spikes"
]
for i, instruction in enumerate(instructions):
    text = font_small.render(instruction, True, WHITE)
    screen.blit(text, (10, 280 + i * 20))

# Tải hình nền kết thúc game
try:
    background2 = pygame.image.load(r"asset\anh_background\ketthucgame.png").convert()
    background2 = pygame.transform.smoothscale(background2, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Dùng smoothscale cho chất lượng tốt hơn
except:
    background2 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background2.fill((50, 150, 50))

# Tải hình nền chiến thắng game
try:
    background3 = pygame.image.load(r"asset\anh_background\chienthanggame.png").convert()
    background3 = pygame.transform.smoothscale(background3, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Dùng smoothscale cho chất lượng tốt hơn
except:
    background3 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background3.fill((50, 150, 50))

# Tải hình nền chuyển level
try:
    background4 = pygame.image.load(r"asset\anh_background\anhdep.jpg").convert()
    background4 = pygame.transform.smoothscale(background4, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Dùng smoothscale cho chất lượng tốt hơn
except:
    background4 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    background4.fill((50, 150, 50))

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
    bomb_img = pygame.image.load(r"asset\anh_icon\traibom.png").convert_alpha()
    bomb_img = pygame.transform.scale(bomb_img, (GRID_SIZE - 5, GRID_SIZE - 5))
except Exception as e:
    print(f"Không thể tải hình ảnh trái bom: {e}")
    bomb_img = pygame.Surface((GRID_SIZE - 5, GRID_SIZE - 5), pygame.SRCALPHA)
    pygame.draw.circle(bomb_img, (100, 0, 0), (12.5, 12.5), 12)  # Hình mặc định


# tải hình ảnh tường
WALL_TEXTURE = pygame.image.load(r"asset/anh_icon/gach3.jpg").convert()
WALL_TEXTURE = pygame.transform.scale(WALL_TEXTURE, (MAZE_WIDTH, MAZE_HEIGHT))


# Tải hình ảnh chìa khóa (thêm vào phần tải tài nguyên)
try:
    key_img = pygame.image.load(r"asset\anh_icon\chiakhoa.png").convert_alpha()
    key_img = pygame.transform.scale(key_img, (GRID_SIZE - 5, GRID_SIZE - 5))
except Exception as e:
    print(f"Không thể tải hình ảnh chìa khóa: {e}")


# tải ảnh ngôi sao
try:
    star_img = pygame.image.load(r"asset\anh_icon\ngoisao.png").convert_alpha()
    star_img = pygame.transform.scale(star_img, (GRID_SIZE - 5, GRID_SIZE - 5))
except Exception as e:
    print(f"Không thể tải hình ảnh ngôi sao: {e}")

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



# màn hình khởi động
def splash_screen():
    # Tải ảnh nền
    try:
        splash_image = pygame.image.load(r"asset\anh_background\anhnen.png").convert()
        splash_image = pygame.transform.smoothscale(splash_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    except Exception as e:
        print(f"Không thể tải splash_screen.png: {e}")
        splash_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        splash_image.fill(DARK_BLUE)
        text = font_large.render("Pursuit Game", True, YELLOW)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        splash_image.blit(text, text_rect)

    # Tạo bề mặt cho quả cầu
    ball_size = 50  # Kích thước quả cầu
    ball_surface = pygame.Surface((ball_size, ball_size), pygame.SRCALPHA)

    # Vẽ quả cầu (màu xanh trùng với đường đi)
    pygame.draw.circle(ball_surface, (0, 255, 0), (ball_size // 2, ball_size // 2), ball_size // 2)  # Màu xanh


    # Vẽ lưới màu trắng
    center_x, center_y = ball_size // 2, ball_size // 2
    radius = ball_size // 2

    # Vẽ các đường kinh tuyến (dọc)
    for angle in range(0, 360, 30):  # Mỗi 30 độ
        rad = math.radians(angle)
        x1 = center_x + radius * math.cos(rad)
        y1 = center_y + radius * math.sin(rad)
        x2 = center_x - radius * math.cos(rad)
        y2 = center_y - radius * math.sin(rad)
        pygame.draw.line(ball_surface, (255, 255, 255), (x1, y1), (x2, y2), 2)

    # Vẽ các đường vĩ tuyến (ngang)
    for r in range(radius // 3, radius, radius // 3):  # 2 vòng vĩ tuyến
        pygame.draw.circle(ball_surface, (255, 255, 255), (center_x, center_y), r, 2)

    # Vẽ thêm một vài đường chéo để tăng chi tiết
    pygame.draw.line(ball_surface, (255, 255, 255), (center_x - radius, center_y - radius // 2),
                     (center_x + radius, center_y + radius // 2), 2)
    pygame.draw.line(ball_surface, (255, 255, 255), (center_x - radius, center_y + radius // 2),
                     (center_x + radius, center_y - radius // 2), 2)

    # Tạo đường đi màu xanh (danh sách các điểm tọa độ)
    path = []
    for x in range(50, WINDOW_WIDTH - 50, 5):
        y = WINDOW_HEIGHT - 50 + 20 * math.sin(x * 0.02)  # Đường cong sin
        path.append((x, y))

    # Thời gian hiển thị splash screen
    splash_duration = 7 * 1000  # 7 giây

    # Tính tốc độ để quả cầu đi hết đường trong 7 giây
    total_path_length = len(path)  # Tổng số điểm trên đường đi
    total_frames = (splash_duration / 1000) * FPS  # Tổng số khung hình trong 7 giây
    ball_speed = total_path_length / total_frames  # Tốc độ để đi hết đường đúng 7 giây

    start_time = pygame.time.get_ticks()
    path_index = 0  # Chỉ số điểm hiện tại trên đường đi
    rotation_angle = 0  # Góc xoay của quả cầu
    rotation_speed = 360 / total_path_length * ball_speed  # Tốc độ xoay (độ/frame)

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

        # Cập nhật vị trí quả cầu
        path_index += ball_speed
        if path_index >= len(path):
            path_index = len(path) - 1  # Dừng ở điểm cuối

        # Cập nhật góc xoay để tạo hiệu ứng lăn
        rotation_angle += rotation_speed
        if rotation_angle >= 360:
            rotation_angle -= 360  # Giữ góc trong khoảng 0-360

        # Xoay quả cầu
        rotated_ball = pygame.transform.rotate(ball_surface, rotation_angle)
        rotated_rect = rotated_ball.get_rect(center=(ball_size // 2, ball_size // 2))

        # Vẽ splash screen
        screen.blit(splash_image, (0, 0))

        # Vẽ đường đi màu xanh đến vị trí hiện tại của quả cầu
        current_path_index = int(path_index)
        if current_path_index > 0:
            pygame.draw.lines(screen, (0, 255, 0), False, path[:current_path_index + 1], 7)  # Đường màu xanh

        # Vẽ quả cầu tại vị trí hiện tại
        ball_pos = path[int(path_index)]
        screen.blit(rotated_ball, (ball_pos[0] - rotated_rect.width // 2, ball_pos[1] - rotated_rect.height // 2))

        pygame.display.flip()
        clock.tick(FPS)

    return True



def menu_screen():
    global frame_index
    menu_active = True
    algorithm_options = ["BFS", "IDS", "A*", "IDA*", "Simulated Annealing", "Beam Search"]
    difficulty_options = ["Easy", "Medium", "Hard"]
    selected_algorithm = 0
    selected_difficulty = 0
    state = "algorithm"

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_giao_dien.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải menu_music.mp3")

    title_font = pygame.font.Font("freesansbold.ttf", 80)
    option_font = pygame.font.Font("freesansbold.ttf", 56)
    FPS = 60  # Đồng bộ với game chính

    while menu_active:
        if background_frames:
            screen.blit(background_frames[frame_index], (0, 0))
            frame_index = (frame_index + 1) % len(background_frames)
        else:
            screen.fill((50, 150, 50))

        title_text = title_font.render("Pursuit Game", True, YELLOW)
        title_shadow = title_font.render("Pursuit Game", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))

        screen.blit(title_shadow, title_rect.move(4, 4))
        screen.blit(title_text, title_rect)

        if state == "algorithm":
            instruction_text = option_font.render("Select Algorithm:", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                screen.blit(option_font.render("Select Algorithm:", True, BLACK), instruction_rect.move(*offset))
            screen.blit(instruction_text, instruction_rect)

            for i, algorithm in enumerate(algorithm_options):
                color = YELLOW if i == selected_algorithm else WHITE
                text = option_font.render(algorithm, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 60))
                for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                    screen.blit(option_font.render(algorithm, True, BLACK), text_rect.move(*offset))
                screen.blit(text, text_rect)

        elif state == "difficulty":
            instruction_text = option_font.render("Select Difficulty:", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
            for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                screen.blit(option_font.render("Select Difficulty:", True, BLACK), instruction_rect.move(*offset))
            screen.blit(instruction_text, instruction_rect)

            for i, difficulty in enumerate(difficulty_options):
                color = YELLOW if i == selected_difficulty else WHITE
                text = option_font.render(difficulty, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 60))
                for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                    screen.blit(option_font.render(difficulty, True, BLACK), text_rect.move(*offset))
                screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            elif event.type == pygame.KEYDOWN:
                if state == "algorithm":
                    if event.key == pygame.K_UP:
                        selected_algorithm = (selected_algorithm - 1) % len(algorithm_options)
                    elif event.key == pygame.K_DOWN:
                        selected_algorithm = (selected_algorithm + 1) % len(algorithm_options)
                    elif event.key == pygame.K_RETURN:
                        state = "difficulty"
                    elif event.key == pygame.K_ESCAPE:
                        return None, None
                elif state == "difficulty":
                    if event.key == pygame.K_UP:
                        selected_difficulty = (selected_difficulty - 1) % len(difficulty_options)
                    elif event.key == pygame.K_DOWN:
                        selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                    elif event.key == pygame.K_RETURN:
                        return algorithm_options[selected_algorithm], difficulty_options[selected_difficulty]
                    elif event.key == pygame.K_ESCAPE:
                        return None, None

    return None, None

# Game Over
def game_over_screen(final_score, total_stars):
    pygame.mixer.music.stop()
    screen.blit(background2, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(40)
    screen.blit(overlay, (0, 0))

    # Hàm tạo chữ với viền để nổi bật
    def render_text_with_outline(text, font, text_color, outline_color):
        text_surface = font.render(text, True, text_color)
        outline_surface = font.render(text, True, outline_color)
        surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2), (2, -2), (-2, 2)]:  # 8 hướng viền
            surface.blit(outline_surface, (dx + 2, dy + 2))
        surface.blit(text_surface, (2, 2))
        return surface

    # Tạo các dòng chữ với viền
    game_over_text = render_text_with_outline("Game Over!", font_large, WHITE, RED)
    score_text = render_text_with_outline(f"Final Score: {final_score}", font, WHITE, BLACK)
    stars_text = render_text_with_outline(f"Total Stars: {total_stars}", font, WHITE, BLACK)
    replay_text = render_text_with_outline("Press R to Replay", font, WHITE, BLACK)
    ViewPlot_text = render_text_with_outline("Press V to View Plot", font, WHITE, BLACK)

    # Căn giữa và điều chỉnh khoảng cách đều
    spacing = 70  # Khoảng cách giữa các dòng
    start_y = WINDOW_HEIGHT // 3  # Vị trí bắt đầu từ 1/3 chiều cao màn hình

    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, start_y))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + spacing))
    stars_rect = stars_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 2 * spacing))
    replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 3 * spacing))
    ViewPlot_rect= ViewPlot_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 4 * spacing))

    # Vẽ chữ (bỏ khung chữ nhật màu đen)
    for text, rect in [(game_over_text, game_over_rect), (score_text, score_rect),
                       (stars_text, stars_rect), (replay_text, replay_rect), (ViewPlot_text, ViewPlot_rect)]:
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
                if event.key == pygame.K_v:  # Thêm dòng này
                    plot_comparison()
    return False

# Chiến thắng
def victory_screen(final_score, total_stars):
    pygame.mixer.music.stop()
    if victory_sound:
        victory_sound.play()

    screen.blit(background3, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(0)
    screen.blit(overlay, (0, 0))

    # Hàm tạo chữ với viền để nổi bật
    def render_text_with_outline(text, font, text_color, outline_color):
        text_surface = font.render(text, True, text_color)
        outline_surface = font.render(text, True, outline_color)
        surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2), (2, -2), (-2, 2)]:  # 8 hướng viền
            surface.blit(outline_surface, (dx + 2, dy + 2))
        surface.blit(text_surface, (2, 2))
        return surface

    # Tạo các dòng chữ với viền
    victory_text = render_text_with_outline("You Win!", font_large, YELLOW, GREEN)
    score_text = render_text_with_outline(f"Final Sco re: {final_score}", font, WHITE, BLACK)
    stars_text = render_text_with_outline(f"Total Stars: {total_stars}", font, WHITE, BLACK)
    replay_text = render_text_with_outline("Press R to Replay, Q to Quit", font, WHITE, BLACK)
    ViewPlot_text = render_text_with_outline("Press V to View Plot", font, WHITE, BLACK)

    # Căn giữa và điều chỉnh khoảng cách đều
    spacing = 70  # Khoảng cách giữa các dòng
    start_y = WINDOW_HEIGHT // 3  # Vị trí bắt đầu từ 1/3 chiều cao màn hình

    victory_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, start_y-20))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + spacing))
    stars_rect = stars_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 2 * spacing))
    replay_rect = replay_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 3 * spacing))
    ViewPlot_rect = ViewPlot_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 4 * spacing))

    # Vẽ chữ (bỏ khung chữ nhật màu đen)
    for text, rect in [(victory_text, victory_rect), (score_text, score_rect),
                       (stars_text, stars_rect), (replay_text, replay_rect), (ViewPlot_text, ViewPlot_rect)]:
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
                elif event.key == pygame.K_v:  # Thêm dòng này
                    plot_comparison()
    return False


# Vẽ bảng thông tin
def draw_hud(score, difficulty, stage_info, player, algorithm):
    hud_font = pygame.font.Font(None, 36)

    # Điểm số map hiện tại
    score_text = hud_font.render(f"Map Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 40))

    # Độ khó
    difficulty_text = hud_font.render(f"Difficulty: {difficulty}", True, WHITE)
    screen.blit(difficulty_text, (10, 70))

    # Stage và Map
    stage_text = hud_font.render(stage_info, True, WHITE)
    screen.blit(stage_text, (10, 100))

    # Thuật toán hiện tại (sử dụng algorithm được truyền vào)
    algorithm_text = hud_font.render(f"Enemy AI: {algorithm}", True, WHITE)
    screen.blit(algorithm_text, (10, 130))

    # Số bom
    bomb_text = hud_font.render(f"Bombs: {player.bombs}", True, WHITE)
    screen.blit(bomb_text, (10, 160))

    # Trạng thái chìa khóa
    key = "Yes" if player.has_key else "No"
    key_text = font.render(f"KEY: {key}", True, WHITE)
    screen.blit(key_text, (10, 190))

    # Tổng số ngôi sao
    stars_text = font.render(f"Total Stars: {total_stars}", True, WHITE)
    screen.blit(stars_text, (10, 220))

    # Thanh máu
    pygame.draw.rect(screen, RED, (10, 250, 150, 12))
    health_width = (player.health / player.max_health) * 150
    pygame.draw.rect(screen, GREEN, (10, 250, health_width, 12))
    pygame.draw.rect(screen, BLACK, (10, 250, 150, 12), 2)

def save_high_score(score, stars, file_path="high_scores.json"):
    high_scores = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            high_scores = json.load(f)
    high_scores.append({"score": score, "stars": stars, "timestamp": time.time()})
    with open(file_path, 'w') as f:
        json.dump(high_scores, f)

# Giao diện chuyển màn chơi
def stage_transition_screen(completed_stage, next_stage, score):
    screen.blit(background4, (0, 0))
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill(DARK_BLUE)
    overlay.set_alpha(100)
    screen.blit(overlay, (0, 0))

    # Hàm tạo chữ với viền để nổi bật
    def render_text_with_outline(text, font, text_color, outline_color):
        text_surface = font.render(text, True, text_color)
        outline_surface = font.render(text, True, outline_color)
        surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2), (2, 2), (-2, -2), (2, -2), (-2, 2)]:  # 8 hướng viền
            surface.blit(outline_surface, (dx + 2, dy + 2))
        surface.blit(text_surface, (2, 2))
        return surface

    # Tạo các dòng chữ với viền
    completed_text = render_text_with_outline(f"Stage {completed_stage} Completed!", font_large, YELLOW, GREEN)
    next_text = render_text_with_outline(f"Next: Stage {next_stage}", font, WHITE, BLACK)
    score_text = render_text_with_outline(f"Score: {score}", font, WHITE, BLACK)
    stars_text = render_text_with_outline(f"Total Stars: {total_stars}", font, WHITE, BLACK)
    continue_text = render_text_with_outline("Press ENTER to Continue", font_small, WHITE, BLACK)

    # Căn giữa và điều chỉnh khoảng cách đều
    spacing = 70  # Khoảng cách giữa các dòng
    start_y = WINDOW_HEIGHT // 3  # Vị trí bắt đầu từ 1/3 chiều cao màn hình

    completed_rect = completed_text.get_rect(center=(WINDOW_WIDTH // 2, start_y))
    next_rect = next_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + spacing))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 2 * spacing))
    stars_rect = stars_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 3 * spacing))
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + 4 * spacing))

    # Vẽ chữ (bỏ khung chữ nhật màu đen)
    for text, rect in [(completed_text, completed_rect), (next_text, next_rect),
                       (score_text, score_rect), (stars_text, stars_rect), (continue_text, continue_rect)]:
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
    "Me cung": r"asset\anh_background\map1.webp",
    "Can ho": r"asset\anh_background\map2.jpg",
    "Khach san": r"asset\anh_background\map3.png",
    "Rung sau": r"asset\anh_background\map4.jpg",
    "Nha may": r"asset\anh_background\map5.png",
    "Thanh pho": r"asset\anh_background\map6.jpg",
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


# Vòng lặp game chính
running = True
FPS = 60  # Đặt FPS thống nhất
while running:
    check = 0
    if not splash_screen():
        break

    algorithm, difficulty = menu_screen()
    if algorithm is None or difficulty is None:
        break

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"asset\nhac\nhac_choi_game.mp3")
        pygame.mixer.music.play(-1)
    except:
        print("Không thể tải gameplay_music.mp3")

    total_map_score = 0
    total_stars = 0
    current_stage = 0
    game_active = True

    while game_active and current_stage < len(STAGES):
        current_map_idx = 0
        map_order = STAGES[current_stage]

        while game_active and current_map_idx < len(map_order):
            load_map(map_order[current_map_idx])

            try:
                game_background = pygame.image.load(MAP_BACKGROUNDS[map_order[current_map_idx]]).convert()
                game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
            except Exception as e:
                print(f"Không thể tải hình nền cho {map_order[current_map_idx]}: {e}")
                game_background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
                game_background.fill(DARK_BLUE)

            all_sprites = pygame.sprite.Group()
            enemies = pygame.sprite.Group()

            player_pos = (1, 1)
            enemy_pos = (18, 1)

            if grid[player_pos[1]][player_pos[0]] != 1 and grid[enemy_pos[1]][enemy_pos[0]] != 1:
                player = Player(player_pos[0], player_pos[1])
                exit_pos = get_exit_position()
                # Sử dụng algorithm đã chọn từ menu
                enemy = Enemy(enemy_pos[0], enemy_pos[1], player, algorithm, difficulty)
            else:
                player_pos = get_empty_position()
                enemy_pos = get_empty_position()
                while enemy_pos == player_pos:
                    enemy_pos = get_empty_position()
                player = Player(player_pos[0], player_pos[1])
                exit_pos = get_exit_position()
                # Sử dụng algorithm đã chọn từ menu
                enemy = Enemy(enemy_pos[0], enemy_pos[1], player, algorithm, difficulty)

            all_sprites.add(player, enemy)
            enemies.add(enemy)

            num_enemies = 0
            if (difficulty == "Medium" or difficulty == "Hard") and current_stage > 0:
                num_enemies += current_stage

            enemy_positions = []
            for _ in range(num_enemies):
                enemy_pos = get_empty_position()
                while (enemy_pos == player_pos or enemy_pos == exit_pos or
                       enemy_pos in enemy_positions):
                    enemy_pos = get_empty_position()
                enemy_positions.append(enemy_pos)
                # Sử dụng algorithm đã chọn từ menu
                enemy = Enemy(enemy_pos[0], enemy_pos[1], player, algorithm, difficulty)
                all_sprites.add(enemy)
                enemies.add(enemy)

            num_items = max(10 - current_stage, 1)
            num_spikes = 4 + current_stage
            spawn_items(grid, player_pos, enemy_pos, exit_pos, num_items=num_items, num_spikes=num_spikes)

            map_score = 100
            time_elapsed = 0
            score_decrement_interval = 5 * FPS
            decrement_amount = 5

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
                # Kiểm tra kẻ thù trên ô tường
                for enemy in enemies:
                    x, y = enemy.grid_pos
                    if grid[y][x] == 1:
                        print(f"Kẻ thù tại ({x}, {y}) đang ở trên tường!")
                        # Đặt lại vị trí về ô trống gần nhất
                        enemy.grid_pos = list(get_empty_position())
                        enemy.pixel_pos = list(to_pixel_pos(enemy.grid_pos[0], enemy.grid_pos[1]))
                        enemy.rect.center = (int(enemy.pixel_pos[0]), int(enemy.pixel_pos[1]))
                        enemy.path = []
                        enemy.moving = False
                time_elapsed += 1
                if time_elapsed % score_decrement_interval == 0:
                    map_score = max(0, map_score - decrement_amount)

                screen.blit(game_background, (0, 0))
                screen.blit(WALL_TEXTURE, (MAZE_OFFSET_X, MAZE_OFFSET_Y))
                draw_grid(exit_pos)
                all_sprites.draw(screen)
                # Truyền algorithm đã chọn vào draw_hud
                draw_hud(map_score, difficulty, f"Stage {current_stage + 1}: {map_order[current_map_idx]}", player,
                         algorithm)

                if player.unlock_timer > 0:
                    unlock_text = font.render(f"Opening door... {player.unlock_timer // FPS + 1}s", True, WHITE)
                    screen.blit(unlock_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 50))

                if player.show_key_message_timer > 0:
                    need_key_text = font.render("You need a key to exit!", True, RED)
                    screen.blit(need_key_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 50))

                pygame.display.flip()

                if pygame.sprite.spritecollide(player, enemies, False):
                    if collision_sound:
                        collision_sound.play()
                    game_active = False

                if tuple(player.grid_pos) == exit_pos:
                    if player.has_key:
                        if player.unlock_timer == 0:
                            player.unlock_timer = 5 * FPS
                    else:
                        if player.show_key_message_timer == 0:
                            player.show_key_message_timer = 1 * FPS
                else:
                    if player.unlock_timer > 0:
                        player.unlock_timer = 0

                if player.unlock_timer <= 1 and tuple(player.grid_pos) == exit_pos and player.has_key:
                    player.has_key = False
                    total_map_score += map_score
                    current_map_idx += 1
                    if current_map_idx >= len(map_order):
                        if current_stage + 1 < len(STAGES):
                            continue_game = stage_transition_screen(current_stage + 1, current_stage + 2,
                                                                    total_map_score + total_stars * 5)
                            if not continue_game:
                                running = False
                                game_active = False
                            current_stage += 1
                        else:
                            final_score = total_map_score + total_stars * 5
                            replay = victory_screen(final_score, total_stars)
                            if replay:
                                game_active = False
                                check = 1
                                total_map_score = 0
                                total_stars = 0
                                current_stage = 0
                                break
                            else:
                                running = False
                                game_active = False
                                break
                    break

                player_grid_x, player_grid_y = player.grid_pos
                item = grid[player_grid_y][player_grid_x]
                if item in [3, 4, 5, 6, 7, 8, 9, 10]:
                    if item == 3:
                        player.activate_speed_boost()
                    elif item == 4:
                        for enemy in enemies:
                            enemy.activate_slow()
                    elif item == 5:
                        for enemy in enemies:
                            enemy.activate_invisibility()
                    elif item == 6:
                        player.hit_spike()
                    elif item == 7:
                        player.add_bomb()
                    elif item == 8:
                        player.heal(20)
                    elif item == 9:
                        player.pick_key()
                    elif item == 10:
                        player.pick_star()
                    if item != 6:
                        grid[player_grid_y][player_grid_x] = 0

                if player.health <= 0:
                    if collision_sound:
                        collision_sound.play()
                    game_active = False

        if running and not game_active:
            final_score = total_map_score + total_stars * 5
            if check == 0:
                replay = game_over_screen(final_score, total_stars)
                if not replay:
                    running = False
                else:
                    total_map_score = 0
                    total_stars = 0
                    current_stage = 0
                    break
            else:
                replay = True
                if not replay:
                    running = False
                else:
                    total_map_score = 0
                    total_stars = 0
                    current_stage = 0
                    break

pygame.quit()