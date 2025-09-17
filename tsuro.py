import arcade
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Tsuro Game"
TILE_SIZE = 100
GRID_SIZE = 6

# Possible connection templates
TILE_CONNECTIONS = [
    {0: 5, 1: 7, 2: 6, 3: 4},
    {0: 7, 1: 4, 2: 5, 3: 6},
    {0: 3, 1: 7, 2: 5, 4: 6},
    {0: 1, 2: 7, 3: 5, 4: 6},
]

# Tile colors
TILE_COLORS = [
    arcade.color.BLUE,
    arcade.color.GREEN,
    arcade.color.ORANGE,
    arcade.color.AMETHYST,
]

# --- Tile Class ---
class Tile:
    def __init__(self, connections, color):
        self.connections = connections
        self.color = color

    def draw(self, x, y):
      arcade.draw_lrbt_rectangle_filled(
          x - TILE_SIZE // 2,
          x + TILE_SIZE // 2,
          y - TILE_SIZE // 2,
          y + TILE_SIZE // 2,
          self.color
      )

      arcade.draw_lrbt_rectangle_outline(
          x - TILE_SIZE // 2,
          x + TILE_SIZE // 2,
          y - TILE_SIZE // 2,
          y + TILE_SIZE // 2,
          arcade.color.BLACK,
          2
      )

        # Draw simple lines as paths
      for port, conn in self.connections.items():
          start_x, start_y = self.get_port_coords(x, y, port)
          end_x, end_y = self.get_port_coords(x, y, conn)
          arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK, 4)

    def get_port_coords(self, x, y, port):
        offset = TILE_SIZE // 2
        if port == 0:
            return x, y + offset
        elif port == 1:
            return x + offset // 2, y + offset
        elif port == 2:
            return x + offset, y + offset // 2
        elif port == 3:
            return x + offset, y
        elif port == 4:
            return x + offset, y - offset // 2
        elif port == 5:
            return x, y - offset
        elif port == 6:
            return x - offset, y - offset // 2
        elif port == 7:
            return x - offset // 2, y + offset
        return x, y

# --- Board Class ---
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def place_tile(self, row, col, tile):
        self.grid[row][col] = tile

    def draw(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * TILE_SIZE + TILE_SIZE // 2
                y = row * TILE_SIZE + TILE_SIZE // 2
                tile = self.grid[row][col]
                if tile:
                    tile.draw(x, y)
                else:
                    arcade.draw_lrbt_rectangle_outline(x - TILE_SIZE // 2,x + TILE_SIZE // 2,y - TILE_SIZE // 2,y + TILE_SIZE // 2,arcade.color.WHITE)

# --- Player Class ---
class Player:
    def __init__(self, color, start_pos, start_port):
        self.color = color
        self.row, self.col = start_pos
        self.port = start_port
        self.alive = True

    def draw(self):
        x = self.col * TILE_SIZE + TILE_SIZE // 2
        y = self.row * TILE_SIZE + TILE_SIZE // 2
        arcade.draw_circle_filled(x, y, 10, self.color)

# --- Global game state ---
board = None
players = None
tiles = None

# --- Drawing function ---
def draw():
    arcade.start_render()
    
    board.draw()
    for player in players:
        if player.alive:
            player.draw()
    arcade.finish_render()

# --- Mouse click handler ---
def on_mouse_press(x, y, button, modifiers):
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        if board.grid[row][col] is None and tiles:
            tile = tiles.pop()
            board.place_tile(row, col, tile)
    draw()

# --- Main function ---
def main():
    global board, players, tiles

    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_background_color(arcade.color.BROWN)
    board = Board()
    players = [
        Player(arcade.color.RED, (0, 0), 6),
        Player(arcade.color.BLUE, (GRID_SIZE - 1, GRID_SIZE - 1), 4)
    ]
    tiles = []
    for _ in range(30):
        conn = random.choice(TILE_CONNECTIONS)
        color = random.choice(TILE_COLORS)
        tiles.append(Tile(conn, color))
    
    draw()
    arcade.run()

if __name__ == "__main__":
    main()
