
# imports
import pygame as pg
import random as rd

pg.init() # initialising pygame


# constants
SCREEN_SIZE = (720, 1280)
HUD_HEIGHT  = 260
BORDER_WIDTH = 10
FPS = 60
BG = 'grey'
CELL_SIZE = 50
GRID_COLOR = '#4B3F55' # light shade
MOVE_INTERVAL = 200


# derived values
GRID_WIDTH = (SCREEN_SIZE[0] - 2 * BORDER_WIDTH) // CELL_SIZE
GRID_HEIGHT = (
    SCREEN_SIZE[1] - HUD_HEIGHT  - 2 * BORDER_WIDTH
) // CELL_SIZE



# coustom move timer
MOVE_EVENT = pg.event.custom_type()
pg.time.set_timer(MOVE_EVENT, MOVE_INTERVAL)



screen = pg.display.set_mode(SCREEN_SIZE)
import sprites as sp
clock = pg.time.Clock()


head = {
direction : sp.load_sprite(sp.head[direction], CELL_SIZE)
for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT')
}

body = sp.load_sprite(sp.body, CELL_SIZE-1)

tail = {
direction : sp.load_sprite(sp.tail[direction], CELL_SIZE)
for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT')
}


class Snake():
    """classic tile based snake with edge warping"""
    def __init__(self, x, y):
        """initialise class and create list[tuple] of snakes body as per initial length"""
        self.x = x
        self.y = y
        self.init_len = 4
        self.body = [(x-n, y) for n in range(self.init_len)]
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.alive = True
        self.ate_food = False
        self.score = 0
        self.t_direction = "LEFT"

    def tail_direction(self):
        tail_x, tail_y = self.body[-1]
        prev_x, prev_y = self.body[-2]

        if tail_x == (prev_x + 1) % GRID_WIDTH:
            self.t_direction = 'RIGHT'
            
        elif tail_x == (prev_x - 1) % GRID_WIDTH:
            self.t_direction = 'LEFT'
            
        elif tail_y == (prev_y + 1) % GRID_HEIGHT:
            self.t_direction = 'DOWN'
            
        elif tail_y == (prev_y - 1) % GRID_HEIGHT:
            self.t_direction = 'UP'



    def draw(self):
        """draws snake body
        while distinguishing between head and tail"""
        for i, coords in enumerate(self.body):
            x_px = BORDER_WIDTH + coords[0] * CELL_SIZE
            y_px = BORDER_WIDTH + coords[1] * CELL_SIZE
            
            c_x = x_px + CELL_SIZE // 2
            c_y = y_px + CELL_SIZE // 2
            
            if i == 0:
                screen.blit(head[self.direction], (x_px, y_px))
            elif i == len(self.body)-1:
                screen.blit(tail[self.t_direction], (x_px, y_px))
            else:
                screen.blit(body, (x_px, y_px))


    def move_and_grow(self, food):
        """handle movement, self collision growth and scoring"""
        self.direction = self.next_direction

        x, y = self.body[0]

        if self.direction == 'RIGHT':
            x += 1
        elif self.direction == 'LEFT':
            x -= 1
        elif self.direction == 'UP':
            y -= 1
        elif self.direction == 'DOWN':
            y += 1

        x %= GRID_WIDTH
        y %= GRID_HEIGHT

        new_head = (x, y)
        self.ate_food = new_head == food.position

        self.body.insert(0, new_head)

        if not self.ate_food:
            self.body.pop()
        else:
            food.spawn(self)
            self.score += 1
            print(f"{self.score=}")

        for segment in self.body[1:]:
            if self.body[0] == segment:
                self.alive = False

        self.tail_direction()


def draw_cells():
    """draws the play area (grid)"""
    for x in range(
    BORDER_WIDTH,
    SCREEN_SIZE[0] - BORDER_WIDTH ,
    CELL_SIZE
    ):
        for y in range(BORDER_WIDTH, SCREEN_SIZE[1] - BORDER_WIDTH - HUD_HEIGHT , CELL_SIZE):
            cell = pg.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen,GRID_COLOR , cell, 1)



def draw_hud(player):
    """draw hud and display score"""

    border = pg.Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1] - HUD_HEIGHT )

    hud = pg.Rect(0,SCREEN_SIZE[1] - HUD_HEIGHT , SCREEN_SIZE[0], HUD_HEIGHT )

    pg.draw.rect(screen, 'black', border, BORDER_WIDTH)

    pg.draw.rect(screen, 'lightblue', hud)
    pg.draw.rect(screen, 'black', hud , BORDER_WIDTH)

    font = pg.font.Font(None, 60)
    score = font.render(f"SCORE: {player.score}", True, 'black')
    #screen.blit(score, (45, 695))
    score_rect = score.get_rect()
    score_rect.midleft = (hud.left + 45, hud.centery)
    screen.blit(score, score_rect)




class Food():
    """food class"""
    def __init__(self, player):
        """initialise the class and set initial food postion"""
        self.position = None
        self.spawn(player)

    def spawn(self, player):
        """select a new position excluding the snake body places"""
        available_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x,y) not in player.body
        ]
        self.position = rd.choice(available_cells)


    def draw(self):
        """draw food"""

        x, y = self.position

        #getting center needed for drawing circle
        center_x = BORDER_WIDTH + x * CELL_SIZE + CELL_SIZE // 2
        center_y = BORDER_WIDTH + y * CELL_SIZE + CELL_SIZE // 2

        pg.draw.circle(
            screen,
            'red',
            (center_x, center_y),
            CELL_SIZE // 2
        )


def handle_events(player, food):
    """handle Pygame event.
    also handle keyboard input and change direction"""

    running = True
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            player.move_and_grow(food)
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_UP) and player.direction != 'DOWN':
                if player.direction != 'UP':
                    player.next_direction = 'UP'

            elif event.key in (pg.K_s, pg.K_DOWN) and player.direction != 'UP':
                if player.direction != 'DOWN':
                    player.next_direction = 'DOWN'

            elif event.key in (pg.K_a, pg.K_LEFT) and player.direction != 'RIGHT':
                if player.direction != 'LEFT':
                    player.next_direction = 'LEFT'

            elif event.key in (pg.K_d, pg.K_RIGHT) and player.direction != 'LEFT':
                if player.direction != 'RIGHT':
                    player.next_direction = 'RIGHT'


    return running


def draw_game(player, food):
    """draw the game"""
    screen.fill(BG)
    draw_cells()
    player.draw()
    food.draw()
    draw_hud(player)
    pg.display.flip()







def game():
    """runs one match"""
    running = True
    player = Snake(4,3)
    food = Food(player)
    while running:
        if not player.alive:
            running = False
            break


        running = handle_events(player, food)

        draw_game(player, food)

        clock.tick(FPS)


game()
pg.quit()