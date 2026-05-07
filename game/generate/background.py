import pygame
import random

from ..constants import W, H


def make_bg(theme):
    surf = pygame.Surface((W, H))
    bt, bb = theme['bg_top'], theme['bg_bot']
    for row in range(H):
        t = row / H
        r = int(bt[0] + (bb[0] - bt[0]) * t)
        g = int(bt[1] + (bb[1] - bt[1]) * t)
        b = int(bt[2] + (bb[2] - bt[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, row), (W, row))
    return surf


def make_snow():
    return [
        {'x': random.uniform(0, W), 'y': random.uniform(0, H),
         'r': random.uniform(0.8, 2.2),
         'sx': random.uniform(-0.25, 0.25),
         'sy': random.uniform(0.3, 1.0)}
        for _ in range(55)
    ]


def draw_snow(screen, snow):
    for s in snow:
        s['x'] = (s['x'] + s['sx']) % W
        s['y'] += s['sy']
        if s['y'] > H:
            s['y'] = 0.0
        pygame.draw.circle(screen, (210, 235, 255),
                           (int(s['x']), int(s['y'])), max(1, int(s['r'])))
