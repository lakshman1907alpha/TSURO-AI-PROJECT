import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Tsuro"
TILE_SIZE = 100
GRID_SIZE = 6

TILE_CONNECTIONS = [
    {0: 5, 1: 7, 2: 6, 3: 4},
    {0: 7, 1: 4, 2: 5, 3: 6},
    {0: 3, 1: 7, 2: 5, 4: 6},
    {0: 1, 2: 7, 3: 5, 4: 6},
]

TILE_COLORS = [
    arcade.color.BLUE,
    arcade.color.GREEN,
    arcade.color.ORANGE,
    arcade.color.AMETHYST,
]

def port_screen_coords(row, col, port):
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = row * TILE_SIZE + TILE_SIZE // 2
    offset = TILE_SIZE // 2
    if port == 0:
        return x - offset // 2, y + offset
    if port == 1:
        return x + offset // 2, y + offset
    if port == 2:
        return x + offset, y + offset // 2
    if port == 3:
        return x + offset, y - offset // 2
    if port == 4:
        return x + offset // 2, y - offset
    if port == 5:
        return x - offset // 2, y - offset
    if port == 6:
        return x - offset, y - offset // 2
    if port == 7:
        return x - offset, y + offset // 2
    return x, y

def is_outer_port(row, col, port):
    top_row = (row == GRID_SIZE - 1)
    bottom_row = (row == 0)
    left_col = (col == 0)
    right_col = (col == GRID_SIZE - 1)
    if top_row and port in (0, 1):
        return True
    if bottom_row and port in (4, 5):
        return True
    if left_col and port in (6, 7):
        return True
    if right_col and port in (2, 3):
        return True
    return False

class Tile:
    def __init__(self, connections, color):
        self.connections = connections
        self.color = color

    def draw(self, row, col):
        x = col * TILE_SIZE + TILE_SIZE // 2
        y = row * TILE_SIZE + TILE_SIZE // 2
        arcade.draw_lrbt_rectangle_filled(
            x - TILE_SIZE // 2,
            x + TILE_SIZE // 2,
            y - TILE_SIZE // 2,
            y + TILE_SIZE // 2,
            self.color,
        )
        arcade.draw_lrbt_rectangle_outline(
            x - TILE_SIZE // 2,
            x + TILE_SIZE // 2,
            y - TILE_SIZE // 2,
            y + TILE_SIZE // 2,
            arcade.color.BLACK,
            2,
        )
        for port, conn in self.connections.items():
            start_x, start_y = port_screen_coords(row, col, port)
            end_x, end_y = port_screen_coords(row, col, conn)
            arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.BLACK, 4)

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def place_tile(self, row, col, tile):
        self.grid[row][col] = tile

    def draw(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile = self.grid[row][col]
                if tile:
                    tile.draw(row, col)
                else:
                    x = col * TILE_SIZE + TILE_SIZE // 2
                    y = row * TILE_SIZE + TILE_SIZE // 2
                    arcade.draw_lrbt_rectangle_outline(
                        x - TILE_SIZE // 2,
                        x + TILE_SIZE // 2,
                        y - TILE_SIZE // 2,
                        y + TILE_SIZE // 2,
                        arcade.color.LIGHT_GRAY,
                    )
                if row in (0, GRID_SIZE - 1) or col in (0, GRID_SIZE - 1):
                    for port in range(8):
                        if is_outer_port(row, col, port):
                            px, py = port_screen_coords(row, col, port)
                            arcade.draw_circle_filled(px, py, 5, arcade.color.WHITE_SMOKE)
                            label = f"P{port}\n({int(px)},{int(py)})"
                            arcade.draw_text(label, px + 6, py + 6, arcade.color.BLACK, 8, anchor_x="left")

class Player:
    def __init__(self, color, start_pos, start_port):
        self.color = color
        self.row, self.col = start_pos
        self.port = start_port
        self.alive = True

    def draw(self):
        px, py = port_screen_coords(self.row, self.col, self.port)
        arcade.draw_circle_filled(px, py, 10, self.color)
        arcade.draw_circle_outline(px, py, 12, arcade.color.BLACK, 2)

board = None
players = None
tiles = None

def draw():
    
    arcade.draw_text(
        SCREEN_TITLE,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT - 24,
        arcade.color.WHITE,
        18,
        anchor_x="center",
    )
    board.draw()
    for player in players:
        if player.alive:
            player.draw()
   

def on_mouse_press(x, y, button, modifiers):
    col = int(x // TILE_SIZE)
    row = int(y // TILE_SIZE)
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        if board.grid[row][col] is None and tiles:
            tile = tiles.pop()
            board.place_tile(row, col, tile)
    arcade.get_window().invalidate()

def main():
    global board, players, tiles
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.start_render()
    arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
    board = Board()
    players = [
        Player(arcade.color.RED, (0, 0), 5),
        Player(arcade.color.BLUE, (GRID_SIZE - 1, GRID_SIZE - 1), 2),
    ]
    tiles = []
    for _ in range(30):
        conn = random.choice(TILE_CONNECTIONS)
        color = random.choice(TILE_COLORS)
        tiles.append(Tile(conn, color))
    window = arcade.get_window()
    window.on_draw = draw
    arcade.finish_render()
    window.on_mouse_press = on_mouse_press
    arcade.run()

if __name__ == "__main__":
    main()
