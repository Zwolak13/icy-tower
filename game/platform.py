import pygame
import random

from .constants import W, H, WALL_W


class Platform:
    def __init__(self, x, y, w, fl, safe=False):
        self.x    = x
        self.y    = y
        self.w    = w
        self.h    = 12
        self.fl   = fl
        self.safe = safe

    def draw(self, surf, cam_y, fonts, theme):
        sy = int(self.y - cam_y)
        if sy < -20 or sy > H + 20:
            return
        pygame.draw.rect(surf, theme['top'], (self.x, sy,     self.w, 6))
        pygame.draw.rect(surf, theme['bot'], (self.x, sy + 6, self.w, 6))

        if self.safe:
            pygame.draw.rect(surf, (255, 215, 0), (self.x, sy, self.w, self.h), 2)
            lbl = fonts['sm'].render(f'Floor {self.fl}', True, (255, 235, 100))
            surf.blit(lbl, (self.x + self.w // 2 - lbl.get_width() // 2, sy - 16))
        elif self.fl > 0 and self.fl % 10 == 0:
            lbl = fonts['xs'].render(str(self.fl), True, (220, 235, 255))
            surf.blit(lbl, (self.x + self.w // 2 - lbl.get_width() // 2, sy - 13))


def new_platform(prev, fl):
    t      = min(fl / 200.0, 1.0)
    gap    = int(62 + t * 58)
    y      = prev.y - gap

    if fl > 0 and fl % 100 == 0:
        return Platform(WALL_W, y, W - WALL_W * 2, fl, safe=True)

    base_w   = int(140 - t * 90)
    variance = int(base_w * 0.45)
    w        = max(30, min(W - WALL_W * 2, base_w + random.randint(-variance, variance)))

    reach = int(130 - t * 35)
    pc    = prev.x + prev.w // 2
    lo    = max(WALL_W, pc - reach - w // 2)
    hi    = min(W - WALL_W - w, pc + reach - w // 2)
    x     = int(lo + random.random() * max(0, hi - lo))
    return Platform(x, y, w, fl)
