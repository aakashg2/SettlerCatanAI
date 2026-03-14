import pygame
import math
import sys
import threading

# ── Tile layout ───────────────────────────────────────────────────────────────
TILE_LAYOUT = [
    [0,  1,  2],
    [3,  4,  5,  6],
    [7,  8,  9, 10, 11],
    [12, 13, 14, 15],
    [16, 17, 18]
]

# ── Colors ────────────────────────────────────────────────────────────────────
RESOURCE_COLORS = {
    'rock':   (130, 130, 130),
    'mud':    (178,  90,  30),
    'wheat':  (240, 200,  40),
    'wood':   ( 34, 139,  34),
    'sheep':  (144, 238, 144),
    'desert': (237, 201, 136),
}
PLAYER_COLORS = {
    'red':    (220,  50,  50),
    'blue':   ( 50, 100, 220),
    'green':  ( 30, 160,  30),
    'yellow': (220, 200,   0),
    'orange': (230, 120,  20),
    'white':  (230, 230, 230),
}
DEFAULT_PLAYER_COLORS = [
    (220,  50,  50),
    ( 50, 100, 220),
    ( 30, 160,  30),
    (220, 200,   0),
]

COLOR_BLACK  = (  0,   0,   0)
COLOR_WHITE  = (255, 255, 255)
COLOR_BORDER = ( 60,  40,  20)
COLOR_BG     = ( 30,  60,  30)
COLOR_HOT    = (200,   0,   0)
COLOR_ROBBER = ( 20,  20,  20)
COLOR_NODE   = (200, 200, 200)
COLOR_SIDEBAR_BG = ( 20,  45,  20)

# ── Window settings ───────────────────────────────────────────────────────────
WIN_W      = 1200
WIN_H      = 950
HEX_RADIUS = 82
SIDEBAR_W  = 220

# Board area width = WIN_W - SIDEBAR_W
BOARD_W    = WIN_W - SIDEBAR_W
ORIGIN     = (BOARD_W // 2, 229)   # computed to center 5-row hex grid vertically

# ── Hex geometry ──────────────────────────────────────────────────────────────
# Pointy-top hex: node angles match Board.py [30,330,270,210,150,90]
NODE_ANGLES_RAD = [math.radians(a) for a in [30, 90, 150, 210, 270, 330]]  # node_idx 0=30°, 1=90°, ..., 5=330°
HEX_W = math.sqrt(3)  # pointy-top horizontal spacing
HEX_H = 1.5            # pointy-top vertical row spacing


def compute_tile_centers():
    centers = {}
    for row_idx, row in enumerate(TILE_LAYOUT):
        x_offset = -(len(row) - 1) * HEX_W / 2.0
        y = -row_idx * HEX_H
        for col_idx, tile_idx in enumerate(row):
            centers[tile_idx] = (x_offset + col_idx * HEX_W, y)
    return centers


def world_to_screen(wx, wy):
    sx = int(ORIGIN[0] + wx * HEX_RADIUS)
    sy = int(ORIGIN[1] - wy * HEX_RADIUS)
    return (sx, sy)


def get_hex_corners(tile_idx, tile_centers):
    cx, cy = tile_centers[tile_idx]
    return [
        world_to_screen(cx + math.cos(a), cy + math.sin(a))
        for a in NODE_ANGLES_RAD
    ]


def get_hex_center_screen(tile_idx, tile_centers):
    cx, cy = tile_centers[tile_idx]
    return world_to_screen(cx, cy)


def build_node_positions(tile_centers):
    """
    Returns a dict: (round_wx, round_wy) -> (screen_x, screen_y)
    Used to draw all 54 unique settlement nodes.
    """
    positions = {}
    for tile_idx in range(19):
        cx, cy = tile_centers[tile_idx]
        for angle in NODE_ANGLES_RAD:
            wx = cx + math.cos(angle)
            wy = cy + math.sin(angle)
            key = (round(wx, 4), round(wy, 4))
            if key not in positions:
                positions[key] = world_to_screen(wx, wy)
    return positions


# ── Drawing functions ─────────────────────────────────────────────────────────

def draw_tile(surface, tile, tile_idx, tile_centers, robber_idx, fonts):
    font_res, font_num, font_small = fonts
    corners   = get_hex_corners(tile_idx, tile_centers)
    center_px = get_hex_center_screen(tile_idx, tile_centers)
    cx, cy    = center_px
    color     = RESOURCE_COLORS.get(tile.resource, (180, 180, 180))

    # Hex fill and border
    pygame.draw.polygon(surface, color,        corners)
    pygame.draw.polygon(surface, COLOR_BORDER, corners, 3)

    # Resource label
    label = tile.resource.upper()
    surf  = font_res.render(label, True, COLOR_BLACK)
    surface.blit(surf, surf.get_rect(center=(cx, cy - HEX_RADIUS // 6)))

    # Number token
    if tile.number > 0:
        token_r   = HEX_RADIUS // 4
        token_y   = cy + HEX_RADIUS // 5
        num_color = COLOR_HOT if tile.number in (6, 8) else COLOR_BLACK

        pygame.draw.circle(surface, COLOR_WHITE,  (cx, token_y), token_r)
        pygame.draw.circle(surface, COLOR_BORDER, (cx, token_y), token_r, 2)

        num_surf = font_num.render(str(tile.number), True, num_color)
        surface.blit(num_surf, num_surf.get_rect(center=(cx, token_y)))

        # Red probability dots for 6 and 8
        if tile.number in (6, 8):
            dot_y = token_y + token_r + 7
            for i in range(5):
                pygame.draw.circle(surface, COLOR_HOT,
                                   (cx + (i - 2) * 8, dot_y), 3)

    # Tile index (small)
    idx_surf = font_small.render(f'#{tile_idx}', True, (90, 90, 90))
    surface.blit(idx_surf, idx_surf.get_rect(center=(cx, cy - HEX_RADIUS // 2 + 10)))

    # Robber token
    if tile_idx == robber_idx:
        rx, ry  = cx + HEX_RADIUS // 3, cy - HEX_RADIUS // 3
        rob_r   = HEX_RADIUS // 5
        pygame.draw.circle(surface, COLOR_ROBBER, (rx, ry), rob_r)
        r_surf  = font_small.render('R', True, COLOR_WHITE)
        surface.blit(r_surf, r_surf.get_rect(center=(rx, ry)))


def draw_nodes(surface, node_positions):
    for (sx, sy) in node_positions.values():
        pygame.draw.circle(surface, COLOR_NODE,   (sx, sy), 6)
        pygame.draw.circle(surface, COLOR_BORDER, (sx, sy), 6, 1)


def draw_settlements_and_cities(surface, players, nodemap, tile_centers, player_color_map):
    """Draw player settlements (squares) and cities (larger square + triangle)."""
    for player in players:
        color = player_color_map.get(player.name, (200, 200, 200))

        for (tile_idx, node_idx) in player.settlements:
            cx, cy = tile_centers[tile_idx]
            angle  = NODE_ANGLES_RAD[node_idx]
            wx     = cx + math.cos(angle)
            wy     = cy + math.sin(angle)
            sx, sy = world_to_screen(wx, wy)
            s = 10
            pygame.draw.rect(surface, color,        (sx - s, sy - s, s*2, s*2))
            pygame.draw.rect(surface, COLOR_BORDER, (sx - s, sy - s, s*2, s*2), 2)

        for (tile_idx, node_idx) in player.cities:
            cx, cy = tile_centers[tile_idx]
            angle  = NODE_ANGLES_RAD[node_idx]
            wx     = cx + math.cos(angle)
            wy     = cy + math.sin(angle)
            sx, sy = world_to_screen(wx, wy)
            s = 13
            # Base square
            pygame.draw.rect(surface, color,        (sx - s, sy - s//2, s*2, s + s//2))
            pygame.draw.rect(surface, COLOR_BORDER, (sx - s, sy - s//2, s*2, s + s//2), 2)
            # Roof triangle
            pygame.draw.polygon(surface, color,
                                [(sx - s, sy - s//2), (sx + s, sy - s//2), (sx, sy - s - s//2)])
            pygame.draw.polygon(surface, COLOR_BORDER,
                                [(sx - s, sy - s//2), (sx + s, sy - s//2), (sx, sy - s - s//2)], 2)


def draw_roads(surface, board, tile_centers, player_color_map):
    """Draw roads as thick colored lines on owned edges."""
    drawn = set()
    for u, v, data in board.G.edges(data=True):
        owner = data.get('roadowner')
        if owner is None:
            continue
        edge_key = tuple(sorted([id(u), id(v)]))
        if edge_key in drawn:
            continue
        drawn.add(edge_key)

        # Find screen positions via nodemap
        pos_u = pos_v = None
        for (tile_idx, node_idx), node_obj in board.nodemap.items():
            if node_obj is u:
                cx, cy = tile_centers[tile_idx]
                angle  = NODE_ANGLES_RAD[node_idx]
                pos_u  = world_to_screen(cx + math.cos(angle), cy + math.sin(angle))
            if node_obj is v:
                cx, cy = tile_centers[tile_idx]
                angle  = NODE_ANGLES_RAD[node_idx]
                pos_v  = world_to_screen(cx + math.cos(angle), cy + math.sin(angle))
            if pos_u and pos_v:
                break

        if pos_u and pos_v:
            color = player_color_map.get(owner, COLOR_WHITE)
            pygame.draw.line(surface, COLOR_BORDER, pos_u, pos_v, 8)
            pygame.draw.line(surface, color,        pos_u, pos_v, 5)


def draw_sidebar(surface, players, player_color_map, fonts, win_h, board_w):
    font_res, font_num, font_small = fonts
    font_header = font_num

    # Background
    pygame.draw.rect(surface, COLOR_SIDEBAR_BG, (board_w, 0, WIN_W - board_w, win_h))
    pygame.draw.line(surface, COLOR_BORDER, (board_w, 0), (board_w, win_h), 2)

    x  = board_w + 12
    y  = 20

    title = font_header.render('PLAYERS', True, COLOR_WHITE)
    surface.blit(title, (x, y))
    y += 32

    for player in players:
        color = player_color_map.get(player.name, (200, 200, 200))

        # Player name badge
        pygame.draw.rect(surface, color, (x, y, 190, 22), border_radius=4)
        name_surf = font_res.render(player.name, True, COLOR_BLACK)
        surface.blit(name_surf, name_surf.get_rect(center=(x + 95, y + 11)))
        y += 28

        # Stats
        lines = [
            f"VP:  {player.num_VPs}",
            f"Cards: {sum(player.cards.values())}",
            f"Roads: {15 - player.roads_inventory}",
            f"Settlements: {5 - player.settlements_inventory}",
            f"Cities: {4 - player.cities_inventory}",
        ]
        for line in lines:
            s = font_small.render(line, True, (200, 220, 200))
            surface.blit(s, (x + 4, y))
            y += 17
        y += 12

    # Legend
    y += 10
    legend_title = font_res.render('RESOURCES', True, COLOR_WHITE)
    surface.blit(legend_title, (x, y))
    y += 22
    for resource, color in RESOURCE_COLORS.items():
        pygame.draw.rect(surface, color,        (x, y, 16, 16))
        pygame.draw.rect(surface, COLOR_BORDER, (x, y, 16, 16), 1)
        label = font_small.render(resource.upper(), True, (200, 220, 200))
        surface.blit(label, (x + 22, y + 1))
        y += 20

    # Robber indicator
    y += 10
    rob_surf = font_small.render('● R = Robber', True, (180, 180, 180))
    surface.blit(rob_surf, (x, y))


# ── Node index legend (top-left corner) ──────────────────────────────────────

def draw_node_legend(surface, fonts):
    """
    Draws a small dummy hex in the top-left corner with each node_idx
    labelled at its correct position (counter-clockwise from 30°).
    """
    font_res, font_num, font_small = fonts
    font_label = font_small

    # Legend panel position and size
    PANEL_X   = 10
    PANEL_Y   = 10
    PANEL_W   = 175
    PANEL_H   = 195
    HEX_R     = 48          # radius of the dummy hex
    HEX_CX    = PANEL_X + PANEL_W // 2
    HEX_CY    = PANEL_Y + 30 + HEX_R + 18   # leave room for title

    # Semi-transparent dark panel background
    panel_surf = pygame.Surface((PANEL_W, PANEL_H), pygame.SRCALPHA)
    panel_surf.fill((10, 30, 10, 200))
    surface.blit(panel_surf, (PANEL_X, PANEL_Y))
    pygame.draw.rect(surface, COLOR_BORDER, (PANEL_X, PANEL_Y, PANEL_W, PANEL_H), 2)

    # Title
    title_surf = font_res.render('node_idx reference', True, COLOR_WHITE)
    surface.blit(title_surf, title_surf.get_rect(center=(PANEL_X + PANEL_W // 2, PANEL_Y + 12)))

    # Draw dummy hex outline — same angle convention as the board
    # node_idx 0=30°, 1=90°, 2=150°, 3=210°, 4=270°, 5=330°
    NODE_ANGLES = [math.radians(a) for a in [30, 90, 150, 210, 270, 330]]
    hex_corners = [
        (int(HEX_CX + HEX_R * math.cos(a)),
         int(HEX_CY - HEX_R * math.sin(a)))   # flip y to match screen coords
        for a in NODE_ANGLES
    ]

    # Fill and border
    pygame.draw.polygon(surface, (50, 90, 50), hex_corners)
    pygame.draw.polygon(surface, COLOR_BORDER, hex_corners, 2)

    # "tile" label in center
    tile_surf = font_small.render('tile', True, (180, 220, 180))
    surface.blit(tile_surf, tile_surf.get_rect(center=(HEX_CX, HEX_CY)))

    # Draw each node as a circle with its index label
    NODE_COLORS = [
        (255, 100, 100),   # 0 - red
        (255, 180,  60),   # 1 - orange
        (255, 255,  80),   # 2 - yellow
        ( 80, 220,  80),   # 3 - green
        ( 80, 180, 255),   # 4 - blue
        (200,  80, 255),   # 5 - purple
    ]

    NODE_R = 10   # circle radius for each node dot
    LABEL_OFFSET = 16   # how far to push the text label away from center

    for i, (cx, cy) in enumerate(hex_corners):
        color = NODE_COLORS[i]

        # Colored circle at the node
        pygame.draw.circle(surface, color,        (cx, cy), NODE_R)
        pygame.draw.circle(surface, COLOR_BORDER, (cx, cy), NODE_R, 1)

        # Index number inside the circle
        idx_surf = font_label.render(str(i), True, COLOR_BLACK)
        surface.blit(idx_surf, idx_surf.get_rect(center=(cx, cy)))

        # Angle label pushed outward from hex center
        angle = NODE_ANGLES[i]
        lx = int(cx + LABEL_OFFSET * math.cos(angle))
        ly = int(cy - LABEL_OFFSET * math.sin(angle))
        angle_deg = 30 + i * 60
        angle_surf = font_label.render(f'{angle_deg}°', True, color)
        surface.blit(angle_surf, angle_surf.get_rect(center=(lx, ly)))


# ── Main visualizer class ──────────────────────────────────────────────────────

class BoardVisualizer:
    """
    Pygame-based Catan board visualizer.

    Usage:
        viz = BoardVisualizer(board, players)
        viz.run()          # opens window, blocks until closed

    Or for a single-frame update (e.g. called after each turn):
        viz = BoardVisualizer(board, players)
        viz.init()
        while game_running:
            ... game logic ...
            viz.draw()
            pygame.time.wait(100)
        viz.quit()
    """

    def __init__(self, board, players):
        self.board        = board
        self.players      = players
        self.tile_centers = compute_tile_centers()
        self.node_positions = build_node_positions(self.tile_centers)

        # Assign a color to each player
        self.player_color_map = {}
        for i, player in enumerate(players):
            name_color = PLAYER_COLORS.get(player.color.lower().strip(), None)
            self.player_color_map[player.name] = (
                name_color if name_color else DEFAULT_PLAYER_COLORS[i % len(DEFAULT_PLAYER_COLORS)]
            )

        self.screen = None
        self.fonts  = None
        self.clock  = None

        # Threading support
        self._redraw_needed  = threading.Event()
        self._continue_event = threading.Event()
        self._pause_message  = None

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption('Catan Board')
        self.clock  = pygame.time.Clock()
        self.fonts  = (
            pygame.font.SysFont('Arial', 13, bold=True),   # resource label
            pygame.font.SysFont('Arial', 18, bold=True),   # number token
            pygame.font.SysFont('Arial', 11),              # small text
        )

    def draw(self):
        self.screen.fill(COLOR_BG)

        # Tiles
        for tile_idx in range(19):
            draw_tile(self.screen, self.board.tiles[tile_idx], tile_idx,
                      self.tile_centers, self.board.robber, self.fonts)

        # Roads
        draw_roads(self.screen, self.board, self.tile_centers, self.player_color_map)

        # Settlement nodes (unoccupied spots)
        draw_nodes(self.screen, self.node_positions)

        # Settlements and cities
        draw_settlements_and_cities(self.screen, self.players,
                                    self.board.nodemap, self.tile_centers,
                                    self.player_color_map)

        # Sidebar
        draw_sidebar(self.screen, self.players, self.player_color_map,
                     self.fonts, WIN_H, BOARD_W)

        # Title
        title_font = pygame.font.SysFont('Arial', 22, bold=True)
        title_surf = title_font.render('CATAN BOARD', True, COLOR_WHITE)
        self.screen.blit(title_surf,
                         title_surf.get_rect(center=(BOARD_W // 2, 18)))

        # Node index reference legend (top-left)
        draw_node_legend(self.screen, self.fonts)

        pygame.display.flip()

    def refresh(self):
        """Redraw one frame and process events. Returns False if window was closed."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        self.draw()
        self.clock.tick(30)
        return True

    def pause(self, message="Press SPACE or ENTER to continue"):
        """Show the current board state and block until the user presses SPACE/ENTER."""
        if self.screen is None:
            self.init()
        # Draw message overlay
        self._draw_with_message(message)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                        waiting = False
            self.clock.tick(30)
        return True

    def _draw_with_message(self, message):
        self.draw()
        font = pygame.font.SysFont('Arial', 16, bold=True)
        surf = font.render(message, True, COLOR_WHITE)
        rect = surf.get_rect(center=(BOARD_W // 2, WIN_H - 20))
        bg = pygame.Surface((rect.width + 16, rect.height + 8), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))
        self.screen.blit(bg, (rect.x - 8, rect.y - 4))
        self.screen.blit(surf, rect)
        pygame.display.flip()

    # ── Threaded API (game logic runs in background thread) ──────────────────

    def request_refresh(self):
        """Called from game thread: signal the main thread to redraw."""
        self._redraw_needed.set()

    def request_pause(self, message="Press SPACE or ENTER to continue"):
        """Called from game thread: show message overlay and block until SPACE/ENTER."""
        self._pause_message = message
        self._continue_event.clear()
        self._redraw_needed.set()
        self._continue_event.wait()
        self._pause_message = None
        self._redraw_needed.set()

    def run_loop(self):
        """
        Main-thread pygame event loop for use with threaded game logic.

        Start game logic in a daemon thread, then call this to keep the
        window alive and responsive:

            t = threading.Thread(target=game_logic, args=(game, viz), daemon=True)
            t.start()
            viz.run_loop()
        """
        self.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self._continue_event.set()

            if self._redraw_needed.is_set():
                self._redraw_needed.clear()
                if self._pause_message:
                    self._draw_with_message(self._pause_message)
                else:
                    self.draw()

            self.clock.tick(30)
        self.quit()

    def run(self):
        """Open the window and block until the user closes it."""
        self.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            self.draw()
            self.clock.tick(30)
        self.quit()

    def quit(self):
        pygame.quit()

    def save_screenshot(self, path='catan_board.png'):
        """Save current frame to a PNG — useful for testing headlessly."""
        if self.screen is None:
            self.init()
            self.draw()
        pygame.image.save(self.screen, path)
        print(f"Screenshot saved to {path}")


# ── Standalone test (mock board + players) ────────────────────────────────────
if __name__ == '__main__':
    import random

    class MockTile:
        def __init__(self, resource, number):
            self.resource = resource
            self.number   = number

    class MockNode:
        def __init__(self): self.owner = None

    class MockPlayer:
        def __init__(self, name, color):
            self.name               = name
            self.color              = color
            self.num_VPs            = 0
            self.cards              = {'rock':0,'wood':0,'wheat':0,'mud':0,'sheep':0}
            self.roads_inventory    = 15
            self.settlements_inventory = 5
            self.cities_inventory   = 4
            self.settlements        = []
            self.cities             = []

    class MockBoard:
        def __init__(self):
            import networkx as nx
            res  = ["rock"]*3+["mud"]*3+["wheat"]*4+["wood"]*4+["sheep"]*4
            nums = [2,12]+2*[3,4,5,6,8,9,10,11]
            random.shuffle(res); random.shuffle(nums)
            iv = random.randint(0,18)
            res  = res[:iv]+['desert']+res[iv:]
            nums = nums[:iv]+[-1]+nums[iv:]
            self.tiles   = [MockTile(res[i], nums[i]) for i in range(19)]
            self.robber  = iv
            self.G       = nx.Graph()
            self.nodemap = {}

    board   = MockBoard()
    players = [
        MockPlayer('Alice', 'red'),
        MockPlayer('Bob',   'blue'),
    ]
    # Give Alice a mock settlement on tile 4, node 0
    players[0].settlements = [(4, 0)]
    players[0].num_VPs     = 2
    players[1].settlements = [(9, 3)]
    players[1].num_VPs     = 1

    viz = BoardVisualizer(board, players)
    viz.init()
    viz.draw()
    viz.save_screenshot('/home/claude/catan_final.png')
    pygame.quit()