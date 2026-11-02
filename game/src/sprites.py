from pathlib import Path
import pygame as pg

ASSETS = Path(__file__).resolve().parent.parent / 'assets' / 'Sprites'

body = pg.image.load(ASSETS / 'snake_body.png').convert_alpha()

head = {
    direction: pg.image.load(
        ASSETS / f'snake_head_{direction.lower()}.png'
    ).convert_alpha()
    for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT')
}

tail = {
    direction: pg.image.load(
        ASSETS / f'snake_tail_{direction.lower()}.png'
    ).convert_alpha()
    for direction in ('UP', 'DOWN', 'LEFT', 'RIGHT')
}

def load_sprite(image, size):
    return pg.transform.scale(image, (size, size))


