import pygame as pg
import random as rd
pg.init()

SCREEN_SIZE = (500, 760)
HUD_HEIGHT  = 100
BORDER_WIDTH = 10
FPS = 60
BG = 'grey'
SHELL_SIZE = 40
GRID_COLOR = '#4B3F55' # light shade


MOVE_INTERVAL = 200
MOVE_EVENT = pg.event.custom_type()
pg.time.set_timer(MOVE_EVENT, MOVE_INTERVAL)

GRID_WIDTH = (SCREEN_SIZE[0] - 2 * BORDER_WIDTH) // SHELL_SIZE
GRID_HEIGHT = (
    SCREEN_SIZE[1] - HUD_HEIGHT  - 2 * BORDER_WIDTH
) // SHELL_SIZE

screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

class Snake(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.body = []
        self.init_len =4
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.alive = True
        self.ate_food = False
        self.score = 0
        
        for n in range(self.init_len):
            self.body.append((x-n,y))
        
    def draw(self):
        for i, coords in enumerate(self.body):
            x_px = BORDER_WIDTH + coords[0] * SHELL_SIZE
            y_px = BORDER_WIDTH + coords[1] * SHELL_SIZE
            c_x = x_px + SHELL_SIZE // 2
            c_y = y_px + SHELL_SIZE // 2
            if i == 0:
                pg.draw.rect(screen, 'Green', (x_px, y_px, SHELL_SIZE, SHELL_SIZE))
                pg.draw.circle(screen, 'black', (c_x, c_y) , 10)
            elif i == len(self.body)-1:
                pg.draw.rect(screen, 'darkgreen', (x_px+5, y_px+5, SHELL_SIZE-5, SHELL_SIZE-10))
            else:
                pg.draw.rect(screen, 'Green', (x_px, y_px, SHELL_SIZE, SHELL_SIZE))
                
                
    def movement(self, food):
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
            food.spawn()
            self.score += 1
            print(f"{self.score=}")
            
        for segment in self.body[1:]:
            if self.body[0] == segment:
                self.alive = False
      
      
      
def draw_shells():
    for x in range(
    BORDER_WIDTH,
    SCREEN_SIZE[0] - BORDER_WIDTH ,
    SHELL_SIZE
    ):
        for y in range(BORDER_WIDTH, SCREEN_SIZE[1] - BORDER_WIDTH - HUD_HEIGHT , SHELL_SIZE):
            shell = pg.Rect(x, y, SHELL_SIZE, SHELL_SIZE)
            pg.draw.rect(screen,GRID_COLOR , shell, 1)
    border1 = pg.Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1] - HUD_HEIGHT )
    
    hud = pg.Rect(0,SCREEN_SIZE[1] - HUD_HEIGHT , SCREEN_SIZE[0], HUD_HEIGHT )
    pg.draw.rect(screen, 'black', border1, BORDER_WIDTH)
    pg.draw.rect(screen, 'blue', hud)
    pg.draw.rect(screen, 'black', hud , BORDER_WIDTH)

class Food(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = None
        self.spawn()

    def spawn(self):
        available_shells = [
        (x, y) 
        for x in range(GRID_WIDTH) 
        for y in range(GRID_HEIGHT) 
        if (x,y) not in player.body
        ]
        self.position = rd.choice(available_shells)
        

    def draw(self):
        x, y = self.position
    
        center_x = BORDER_WIDTH + x * SHELL_SIZE + SHELL_SIZE // 2
        center_y = BORDER_WIDTH + y * SHELL_SIZE + SHELL_SIZE // 2
    
        pg.draw.circle(
            screen,
            'red',
            (center_x, center_y),
            SHELL_SIZE // 2
        )
        




running = True


player = Snake(4,3)
food = Food()
font = pg.font.Font(None, 60)
while running:
    if not player.alive:
        running = False
        break
        
    
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            player.movement(food)
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
        
    score = font.render(f"SCORE: {player.score}", True, 'black')
    screen.fill(BG)
    
        
    draw_shells()
    player.draw()
    food.draw()
    screen.blit(score, (45, 695))
    pg.display.flip()
    

    
    
    clock.tick(FPS)

pg.quit()