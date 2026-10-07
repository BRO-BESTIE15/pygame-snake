import pygame as pg

pg.init()

SCREEN_SIZE = (710, 755)
FPS = 1
BG = "grey"
SHELL_SIZE = 50
GRID_COLOR = "#4B3F55"


screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()


def draw_shells():
    for x in range(5, SCREEN_SIZE[0]-5, SHELL_SIZE):
        for y in range(5, SCREEN_SIZE[1]-50, SHELL_SIZE):
            shell = pg.Rect(x, y, SHELL_SIZE, SHELL_SIZE)
            pg.draw.rect(screen,GRID_COLOR , shell, 1)
    border1 = pg.Rect(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]-50)
    
    hud = pg.Rect(0,705, SCREEN_SIZE[0],50)
    hud_border = hud
    pg.draw.rect(screen, "black", border1, 5)
    pg.draw.rect(screen, "blue", hud)
    pg.draw.rect(screen, 'black', hud_border,5)

running = True




while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(BG)

    draw_shells()

    pg.display.flip()
    
    
    
    
    clock.tick(FPS)

pg.quit()