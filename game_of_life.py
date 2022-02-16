import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import time 

import config
import input_parser

def draw_cell(screen, x, y, width=config.TILE_WIDTH, color=config.BLUE, filled=0):
    square = pygame.Rect(x, y, width, width)
    pygame.draw.rect(screen, color, square, filled)


def initialize_data(board_size, initial_dataset):
    max_x, max_y = board_size

    board = set()
    for x, y in initial_dataset:
        if x > max_x:
            raise ValueError(f'dataset contains points ({x}, {y}) greater than the screen\'s'
                             f' x-axis ({max_x}, {max_y})')
        if y > max_y:
            raise ValueError(f'dataset contains points ({x}, {y}) greater than the screen\'s'
                             f' y-axis ({max_x}, {max_y})')

        board.add((x, y))

    return board


def clear_board(screen):
    screen.fill(config.WHITE)


def display_board(screen, board):
    for x, y in board:
        draw_cell(screen, x*config.TILE_WIDTH, y*config.TILE_WIDTH)


def find_neighbors(cell, max_x, max_y):
    x, y = cell
    
    neighbors = set()

    lower = (y-1) % max_y
    upper = (y+1) % max_y
    left = (x-1) % max_x
    right = (x+1) % max_x
    
    neighbors.add((x, lower))
    neighbors.add((x, upper))
    neighbors.add((left, y))
    neighbors.add((right, y))
    neighbors.add((left, lower))
    neighbors.add((left, upper))
    neighbors.add((right, lower))
    neighbors.add((right, upper))    
    
    return neighbors


def check_will_live(cell, board, max_x, max_y):
    neighbors = find_neighbors(cell, max_x, max_y)
    return len([n for n in neighbors if n in board]) in (2, 3)


def check_new_life(center, board, checked_cells, max_x, max_y):
    x, y = center
    fertile_areas = set()

    for neighbor in find_neighbors(center, max_x, max_y):
        if neighbor not in checked_cells and neighbor not in board:
            fertile_areas.add(neighbor)

    babies = set()
    barren = set()
    for cell in fertile_areas:
        neighbors = find_neighbors(cell, max_x, max_y)

        if len([n for n in neighbors if n in board]) == 3:
            babies.add(cell)
        else:
            barren.add(cell)

    return babies, barren


def update(board, grid_size):
    checked_cells = set()
    next_board = set()

    for cell in board:
        if check_will_live(cell, board, grid_size, grid_size):
            next_board.add(cell)
        checked_cells.add(cell)

        babies, barren = check_new_life(cell, board, checked_cells, grid_size, grid_size)
        checked_cells.update(babies)
        checked_cells.update(barren)

        next_board.update(babies)

    return next_board


def game_loop(init_shape, grid_size, iterations):
    pygame.init()
    pygame.display.set_caption('Game of Life')
    
    window_width = grid_size * config.TILE_WIDTH 
    window_height = grid_size * config.TILE_WIDTH

    screen = pygame.display.set_mode( (window_width, window_height), 
            pygame.RESIZABLE, pygame.DOUBLEBUF)    
    # clock = pygame.time.Clock()

    board = initialize_data((grid_size, grid_size), init_shape)
    alive_history = [len(board)]
    display_board(screen, board)
    
    for _ in range(iterations):
        board = update(board, grid_size)
        alive_history.append(len(board))
        clear_board(screen)
        display_board(screen, board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.VIDEORESIZE:                
                screen = pygame.display.set_mode((event.w, event.h),
                                                pygame.RESIZABLE)

        pygame.display.update()

    return alive_history


if __name__ == '__main__':
    init_shape = input_parser.get_init_shape()
    grid_size = input_parser.get_grid_size()
    iterations = input_parser.get_iterations()

    start_time = time.time()
    print("Simulation started at: " + time.ctime(start_time))

    alive_history = game_loop(init_shape, grid_size, iterations)
    
    end_time = time.time()
    print("Simulation ended at: " + time.ctime(end_time))

    
    total_alive = sum(alive_history)
    total_dead = len(alive_history) * grid_size * grid_size - total_alive
    
    print(f"Time elapsed(execution time): {(end_time - start_time) * 1000} milliseconds") 
    print(f"Total Alive Cells: {total_alive}")
    print(f"Total Dead Alive: {total_dead}")
    

    