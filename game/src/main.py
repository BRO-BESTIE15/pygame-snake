import pygame as pg

pg.init()

SCREEN_SIZE = (500, 760)
HUD_HEIGHT  = 100
BORDER_WIDTH = 10
FPS = 60
BG = 'grey'
SHELL_SIZE = 40
GRID_COLOR = '#4B3F55' # light shade


MOVE_INTERVAL = 500
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
        self.direction = 'RIGHT'
        self.init_len = 4
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
                
                
    def movement(self):
        self.body.pop()
        x,y = self.body[0]
        if self.direction == 'RIGHT':
            x+=1
        elif self.direction == 'LEFT':
            x-=1
        elif self.direction == 'UP':
            y-=1
        elif self.direction == 'DOWN':
            y+=1
            
        x %= GRID_WIDTH
        y %= GRID_HEIGHT
        
        self.body.insert(0, (x,y))
      
      
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

running = True


player = Snake(4,8)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == MOVE_EVENT:
            player.movement()
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_w, pg.K_UP) and player.direction != 'DOWN':
                player.direction = 'UP'
            elif event.key in (pg.K_s, pg.K_DOWN) and player.direction != 'UP':
                player.direction = 'DOWN'
            elif event.key in (pg.K_a, pg.K_LEFT) and player.direction != 'RIGHT':
                player.direction = 'LEFT'
            elif event.key in (pg.K_d, pg.K_RIGHT) and player.direction != 'LEFT':
                player.direction = 'RIGHT'

    screen.fill(BG)
    draw_shells()
    player.draw()
    pg.display.flip()
    
    
    
    clock.tick(FPS)

pg.quit()