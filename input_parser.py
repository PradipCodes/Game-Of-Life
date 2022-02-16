import config
import shapes

def get_init_shape(grid_size):
    init_shape = input("Select initial shape pattern. {'glider', 'blinker', 'gosper', 'random'} | Default (random):  ") or 'random'
    return shapes.shapes_map[init_shape] if init_shape in shapes.shapes_map else shapes.get_random_shape(grid_size)

def get_grid_size():
    return int(input(f"Enter Grid Size | Default ({config.GRID_SIZE}) : ") or config.GRID_SIZE)

def get_iterations():
    return int(input(f"Enter number of iterations for simulation: Default({config.ITERATIONS})") or config.ITERATIONS)
