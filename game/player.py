import pygame
import math

from .constants import SPIN_THRESHOLD

SKIN   = (255, 204, 188)
HAT    = ( 15,  20,  70)
JACKET = (200,  35,  35)
PANTS  = ( 25,  35,  95)
EYE    = ( 15,  15,  15)


class Player:
    def __init__(self, x, y):
        self.x           = float(x)
        self.y           = float(y)
        self.vx          = 0.0
        self.vy          = 0.0
        self.w           = 20
        self.h           = 28
        self.on_ground   = False
        self.facing      = 1
        self.coyote      = 0
        self.speed_level = 0
        self.spin_angle  = 0.0

    def _draw_body(self, surf, ox, oy, tick):
        walk = self.on_ground and abs(self.vx) > 0.5
        step = int(math.sin(tick * 0.30) * 3) if walk else 0
        sw   = int(math.sin(tick * 0.30) * 3) if walk else 0

        # Hat
        pygame.draw.rect(surf, HAT,    (ox + 4, oy - 5, 12, 6))
        pygame.draw.rect(surf, HAT,    (ox + 1, oy,     18, 3))
        # Head
        pygame.draw.rect(surf, SKIN,   (ox + 3, oy + 3, 14, 9))
        # Eyes
        ex = ox + 5 if self.facing > 0 else ox + 4
        pygame.draw.rect(surf, EYE,    (ex,      oy + 5, 3, 3))
        pygame.draw.rect(surf, EYE,    (ex + 7,  oy + 5, 3, 3))
        # Arms
        pygame.draw.rect(surf, JACKET, (ox - 2, oy + 12 + sw, 4, 8))
        pygame.draw.rect(surf, JACKET, (ox + 18, oy + 12 - sw, 4, 8))
        # Body
        pygame.draw.rect(surf, JACKET, (ox + 2, oy + 12, 16, 9))
        # Legs
        pygame.draw.rect(surf, PANTS,  (ox + 3,  oy + 21 + step, 6, 7))
        pygame.draw.rect(surf, PANTS,  (ox + 11, oy + 21 - step, 6, 7))

    def draw(self, surf, cam_y, tick):
        px = int(self.x)
        py = int(self.y - cam_y)
        if not self.on_ground and self.speed_level > SPIN_THRESHOLD:
            tmp = pygame.Surface((60, 60), pygame.SRCALPHA)
            self._draw_body(tmp, 20, 20, tick)
            rotated = pygame.transform.rotate(tmp, self.spin_angle)
            cx = px + 10
            cy = py + 10
            surf.blit(rotated, (cx - rotated.get_width() // 2,
                                cy - rotated.get_height() // 2))
        else:
            self._draw_body(surf, px, py, tick)
