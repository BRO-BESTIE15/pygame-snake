
from __future__ import annotations

# imports
from typing import Literal

import pygame as pg
import random as rd


Direction = Literal['UP', 'DOWN', 'LEFT', 'RIGHT']
Position = tuple[int, int]

pg.init() # initialising pygame


# constants
SCREEN_SIZE = (720, 670)
HUD_HEIGHT  = 50
BORDER_WIDTH = 10
FPS = 60
BG = 'grey'
CELL_SIZE = 25
GRID_COLOR = '#4B3F55' # light shade
MOVE_INTERVAL = 500


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


head: dict[Direction, pg.Surface] = {
direction : sp.load_sprite(sp.head[direction], CELL_SIZE)
for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT')
}

body: pg.Surface = sp.load_sprite(sp.body, CELL_SIZE-1)

tail: dict[Direction, pg.Surface] = {
direction : sp.load_sprite(sp.tail[direction], CELL_SIZE)
for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT')
}


class Snake():
    """classic tile based snake with edge warping"""
    def __init__(self, x: int, y: int) -> None:
        """initialise class and create list[tuple] of snakes body as per initial length"""
        self.x = x
        self.y = y
        self.init_len = 50
        self.body: list[Position] = [(x-n, y) for n in range(self.init_len)]
        self.direction: Direction = 'RIGHT'
        self.next_direction: Direction = 'RIGHT'
        self.alive: bool = True
        self.ate_food: bool = False
        self.score: int = 0
        self.t_direction: Direction = "LEFT"

    def tail_direction(self) -> None:
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



    def draw(self) -> None:
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


    def move_and_grow(self, food: Food) -> None:
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

        # Wrap at the edges so the snake re-enters on the opposite side.
        x %= GRID_WIDTH
        y %= GRID_HEIGHT

        new_head = (x, y)
        self.ate_food = new_head == food.position

        self.body.insert(0, new_head)

        # Keep the tail in place when eating to make the snake grow.
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


def draw_cells() -> None:
    """draws the play area (grid)"""
    for x in range(
    BORDER_WIDTH,
    SCREEN_SIZE[0] - BORDER_WIDTH ,
    CELL_SIZE
    ):
        for y in range(BORDER_WIDTH, SCREEN_SIZE[1] - BORDER_WIDTH - HUD_HEIGHT , CELL_SIZE):
            cell = pg.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen,GRID_COLOR , cell, 1)



def draw_hud(player: Snake) -> None:
    """draw hud and display score"""

    border = pg.Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1] - HUD_HEIGHT )

    hud = pg.Rect(0,SCREEN_SIZE[1] - HUD_HEIGHT , SCREEN_SIZE[0], HUD_HEIGHT )

    pg.draw.rect(screen, 'black', border, BORDER_WIDTH)

    pg.draw.rect(screen, 'lightblue', hud)
    pg.draw.rect(screen, 'black', hud , BORDER_WIDTH)

    font = pg.font.Font(None, 40)
    score = font.render(f"SCORE: {player.score}", True, 'black')
    #screen.blit(score, (45, 695))
    score_rect = score.get_rect()
    score_rect.midleft = (hud.left + 45, hud.centery)
    screen.blit(score, score_rect)




class Food():
    """food class"""
    def __init__(self, player: Snake) -> None:
        """initialise the class and set initial food postion"""
        self.position: Position | None = None
        self.spawn(player)

    def spawn(self, player: Snake) -> None:
        """select a new position excluding the snake body places"""
        # Choose only cells the snake does not currently occupy.
        available_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x,y) not in player.body
        ]
        self.position = rd.choice(available_cells)


    def draw(self) -> None:
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


def handle_events(player: Snake, food: Food) -> bool:
    """handle Pygame event.
    also handle keyboard input and change direction"""

    running = True
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            player.move_and_grow(food)
        if event.type == pg.KEYDOWN:
            # Ignore a turn directly back into the snake's current direction.
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


def draw_game(player: Snake, food: Food) -> None:
    """draw the game"""
    screen.fill(BG)
    draw_cells()
    player.draw()
    food.draw()
    draw_hud(player)
    pg.display.flip()







def game() -> None:
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


def game_over() -> bool:
    
    overlay = pg.Rect(0, 0, 500, 500)
    overlay.center = screen.get_rect().center
    pg.draw.rect(screen, 'black', overlay)
    pg.draw.rect(screen, 'white', overlay, 5)
    
    button1 = pg.Rect(0, 0, 300, 80)
    button1.center = (overlay.centerx, overlay.centery - 50)
    
    button2 = pg.Rect(0, 0, 300, 80)
    button2.center = (overlay.centerx, overlay.centery + 70)
    
    font = pg.font.Font(None, 80)
    title_font = pg.font.Font(None, 55)
    title = title_font.render("GAME OVER", True, 'white')
    title_rect = title.get_rect(
    center=(overlay.centerx, overlay.top + 60)
)



    run = True
    retry = False
    
    while run:
    
        # ---------------- EVENTS ----------------
        for event in pg.event.get():
    
            if event.type == pg.QUIT:
                run = False
    
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
    
                    if button1.collidepoint(event.pos):
                        retry = True
                        run = False
    
                    elif button2.collidepoint(event.pos):
                        run = False
    
        # ---------------- DRAWING ----------------
        pg.draw.rect(screen, 'grey', button1, border_radius=15)
        pg.draw.rect(screen, 'grey', button2, border_radius=15)
        screen.blit(title, title_rect)
        txt1 = font.render("Retry", True, 'white')
        txt2 = font.render("Quit", True, 'white')
        
        screen.blit(txt1, txt1.get_rect(center=button1.center))
        screen.blit(txt2, txt2.get_rect(center=button2.center))
        
        pg.display.flip()
        
        clock.tick(60)

    return retry

def main() -> None:
    running = True

    while running:
        game()

        if not pg.get_init():
            break

        retry = game_over()

        if not retry:
            running = False

    pg.quit()


if __name__ == "__main__":
    main()
