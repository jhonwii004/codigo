# -*- coding: utf-8 -*-
import pygame
import sys
import random
import subprocess


def memory_game():
    # Inicialización de pygame
    pygame.init()
    screen_width = 800
    screen_height = 600
    sidebar_height = 50
    screen = pygame.display.set_mode((screen_width, screen_height + sidebar_height))
    pygame.display.set_caption('Juego de Memoria')

    # Colores pastel
    WHITE = (139, 170, 173)
    BLACK = (244, 255, 248)
    GREY = (11, 79, 108)
    colors = [
        (255, 182, 193),  # Light Pink
        (173, 216, 230),  # Light Blue
        (152, 251, 152),  # Light Green
        (255, 239, 213),  # Papaya Whip
        (255, 228, 181),  # Moccasin
        (216, 191, 216),  # Thistle
        (240, 230, 140),  # Khaki
        (250, 235, 215)   # Antique White
    ]

    # Formas para las cartas
    shapes = ["circle", "square", "triangle", "pentagon", "hexagon", "octagon", "star", "diamond"]

    # Parámetros de las cartas
    rows, cols = 4, 4
    padding = 10
    card_width = (screen_width - (cols + 1) * padding) // cols
    card_height = ((screen_height - sidebar_height) - (rows + 1) * padding) // rows

    # Función para crear pares de cartas
    def create_pairs():
        items = shapes * 2
        random.shuffle(items)
        return items

    # Función para dibujar formas
    def draw_shape(shape, color, x, y, width, height):
        if shape == "circle":
            pygame.draw.circle(screen, color, (x + width // 2, y + height // 2), min(width, height) // 3)
        elif shape == "square":
            pygame.draw.rect(screen, color, (x + width // 4, y + height // 4, width // 2, height // 2))
        elif shape == "triangle":
            pygame.draw.polygon(screen, color, [(x + width // 2, y + height // 4), 
                                                (x + width // 4, y + 3 * height // 4), 
                                                (x + 3 * width // 4, y + 3 * height // 4)])
        elif shape == "pentagon":
            pygame.draw.polygon(screen, color, [(x + width // 2, y + height // 5), 
                                                (x + width // 4, y + 2 * height // 5), 
                                                (x + width // 3, y + 4 * height // 5), 
                                                (x + 2 * width // 3, y + 4 * height // 5), 
                                                (x + 3 * width // 4, y + 2 * height // 5)])
        elif shape == "hexagon":
            pygame.draw.polygon(screen, color, [(x + width // 2, y + height // 4), 
                                                (x + width // 4, y + height // 2), 
                                                (x + width // 2, y + 3 * height // 4), 
                                                (x + 3 * width // 4, y + height // 2)])
        elif shape == "octagon":
            pygame.draw.polygon(screen, color, [(x + width // 3, y + height // 5), 
                                                (x + 2 * width // 3, y + height // 5), 
                                                (x + 3 * width // 4, y + 2 * height // 5), 
                                                (x + 3 * width // 4, y + 3 * height // 5), 
                                                (x + 2 * width // 3, y + 4 * height // 5), 
                                                (x + width // 3, y + 4 * height // 5), 
                                                (x + width // 4, y + 3 * height // 5), 
                                                (x + width // 4, y + 2 * height // 5)])
        elif shape == "star":
            pygame.draw.polygon(screen, color, [(x + width // 2, y), 
                                                (x + 3 * width // 8, y + 3 * height // 8), 
                                                (x, y + height // 2), 
                                                (x + 3 * width // 8, y + 5 * height // 8), 
                                                (x + width // 2, y + height), 
                                                (x + 5 * width // 8, y + 5 * height // 8), 
                                                (x + width, y + height // 2), 
                                                (x + 5 * width // 8, y + 3 * height // 8)])
        elif shape == "diamond":
            pygame.draw.polygon(screen, color, [(x + width // 2, y), 
                                                (x + 3 * width // 4, y + height // 2), 
                                                (x + width // 2, y + height), 
                                                (x + width // 4, y + height // 2)])

    # Función para dibujar el tablero
    def draw_board(board, revealed, pairs_found):
        screen.fill(GREY)
        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                x = j * (card_width + padding) + padding
                y = i * (card_height + padding) + padding

                if revealed[index]:
                    draw_shape(board[index], colors[shapes.index(board[index])], x, y, card_width, card_height)
                else:
                    pygame.draw.rect(screen, WHITE, (x, y, card_width, card_height))
                    pygame.draw.rect(screen, BLACK, (x, y, card_width, card_height), 2)

        # Dibujar la barra lateral inferior
        pygame.draw.rect(screen, GREY, (0, screen_height, screen_width, sidebar_height))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Pares encontrados: {pairs_found}", True, BLACK)
        screen.blit(text, (10, screen_height + 10))

        pygame.display.flip()

    # Función para mostrar un mensaje con botones
    def display_message(message, buttons=None):
        screen.fill(GREY)
        font = pygame.font.Font(None, 74)
        text = font.render(message, True, BLACK)
        rect = text.get_rect(center=(screen_width // 2, screen_height // 3))
        screen.blit(text, rect)

        button_rects = []
        if buttons:
            button_font = pygame.font.Font(None, 50)
            for idx, (btn_text, btn_action) in enumerate(buttons):
                btn_text_surface = button_font.render(btn_text, True, WHITE)
                btn_rect = btn_text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + idx * 100))
                pygame.draw.rect(screen, BLACK, btn_rect.inflate(20, 20))
                screen.blit(btn_text_surface, btn_rect)
                button_rects.append((btn_rect, btn_action))

        pygame.display.flip()
        return button_rects

    # Lógica principal del juego
    def play_game():
        board = create_pairs()
        revealed = [False] * 16
        pairs_found = 0
        attempts = 0

        running = True
        first_choice = None

        while running:
            draw_board(board, revealed, pairs_found)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < screen_height:  # Asegurarse de que no se haga clic en la barra lateral
                        row = y // (card_height + padding)
                        col = x // (card_width + padding)
                        guess = row * cols + col

                        if 0 <= guess < 16 and not revealed[guess]:
                            if first_choice is None:
                                first_choice = guess
                                revealed[first_choice] = True
                            else:
                                revealed[guess] = True
                                draw_board(board, revealed, pairs_found)
                                pygame.time.wait(1000)  # Esperar 1 segundo
                                if board[first_choice] != board[guess]:
                                    revealed[first_choice] = False
                                    revealed[guess] = False
                                else:
                                    pairs_found += 1
                                    print("Encontraste una pareja!")
                                first_choice = None
                                attempts += 1

                            if all(revealed):
                                display_message(f"¡Lo lograste en {attempts} intentos!")
                                pygame.time.wait(2000)  # Esperar 2 segundos
                                return

    # Repetir el juego según la selección del usuario
    while True:
        play_game()
        buttons = display_message("¿Jugar de nuevo?", [("Sí", True), ("No", False)])

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for btn_rect, btn_action in buttons:
                        if btn_rect.collidepoint(event.pos):
                            if btn_action:
                                waiting_for_input = False
                            else:
                                subprocess.Run(["python", "Menu.py"])
                                pygame.quit()
                                sys.exit()
                                
                                

if __name__ == "__main__":
    memory_game()
