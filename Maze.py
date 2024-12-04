# -*- coding: utf-8 -*-
import pygame
import sys
from collections import deque


# Función para encontrar todos los caminos usando BFS
def bfs_all_paths(maze, start, goal):
    queue = deque([[start]])
    all_paths = []

    while queue:
        path = queue.popleft()
        x, y = path[-1]

        if (x, y) == goal:
            all_paths.append(path)
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and 
                maze[nx][ny] == 0 and (nx, ny) not in path):
                new_path = list(path)
                new_path.append((nx, ny))
                queue.append(new_path)
                
    return all_paths

# Función para visualizar los caminos con pygame
import pygame
import sys

def visualize_paths(maze, path_fast, path_slow, start, goal):
    pygame.init()
    screen_width, screen_height = 850, 600  # Increased width for the sidebar
    sidebar_width = 250
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Visual with Sidebar')

    cell_size = screen_height // len(maze)  # Adjust cell size based on height
    colors = {
        'wall': (11, 79, 108),
        'path_fast': (32, 191, 85),  # Verde para el camino más rápido
        'path_slow': (232, 95, 92),  # Rojo para el camino menos eficiente
        'start': (241, 247, 238),
        'goal': (232, 144, 5),
        'empty': (255, 255, 255),
        'sidebar': (11, 79, 108)  # Light grey for the sidebar
    }

    font = pygame.font.SysFont(None, 24)  # Default font with size 24

    def draw_sidebar():
        # Draw the sidebar background
        pygame.draw.rect(screen, colors['sidebar'], (screen_width - sidebar_width, 0, sidebar_width, screen_height))
        # Render the text
        text_lines = [
            ("Inicio", colors['start']),
            ("Camino mas corto", colors['path_fast']),
            ("Camino menos eficiente", colors['path_slow']),
            ("Meta", colors['goal']),
        ]
        for i, (line, color) in enumerate(text_lines):
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (screen_width - sidebar_width + 10, 20 + i * 30))

    def draw_maze(current_step_fast=None, current_step_slow=None):
        screen.fill(colors['empty'])
        for i, row in enumerate(maze):
            for j, cell in enumerate(row):
                color = colors['wall'] if cell == 1 else colors['empty']
                pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

        if current_step_fast:
            for (x, y) in current_step_fast:
                pygame.draw.rect(screen, colors['path_fast'], (y * cell_size, x * cell_size, cell_size, cell_size))

        if current_step_slow:
            for (x, y) in current_step_slow:
                pygame.draw.rect(screen, colors['path_slow'], (y * cell_size, x * cell_size, cell_size, cell_size))

        pygame.draw.rect(screen, colors['start'], (start[1] * cell_size, start[0] * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, colors['goal'], (goal[1] * cell_size, goal[0] * cell_size, cell_size, cell_size))

        draw_sidebar()  # Draw the sidebar with the maze

        pygame.display.flip()

    # Mostrar paso a paso
    max_steps = max(len(path_fast), len(path_slow))
    for step in range(max_steps):
        current_step_fast = path_fast[:step + 1] if step < len(path_fast) else path_fast
        current_step_slow = path_slow[:step + 1] if step < len(path_slow) else path_slow
        draw_maze(current_step_fast, current_step_slow)
        pygame.time.wait(500)  # Esperar 500 ms entre pasos
    return
            

# Example usage:
# visualize_paths(your_maze, your_fast_path, your_slow_path, start_coordinates, goal_coordinates)

# Función principal para el juego Maze Runner
def maze_game():
    # Datos del laberinto
    maze = [
[0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
[1, 1, 0, 1, 0, 1, 0, 1, 0, 0], 
[0, 1, 0, 0, 0, 0, 0, 1, 1, 0], 
[0, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 1, 1, 1, 0, 1], 
[0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
[0, 1, 0, 0, 0, 1, 0, 0, 1, 0], 
[0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
    ]

    start = (0, 0)
    goal = (9, 9)

    # Encontrar todos los caminos y visualizar
    all_paths = bfs_all_paths(maze, start, goal)
    if all_paths:
        path_fast = min(all_paths, key=len)
        path_slow = max(all_paths, key=len)
        visualize_paths(maze, path_fast, path_slow, start, goal)
    else:
        print("No se encontro un camino.")
