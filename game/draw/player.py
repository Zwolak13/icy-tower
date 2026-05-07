import pygame
import math

from ..constants import SPIN_THRESHOLD

SKIN   = (255, 204, 188)
HAT    = ( 15,  20,  70)
JACKET = (200,  35,  35)
PANTS  = ( 25,  35,  95)
EYE    = ( 15,  15,  15)


def _draw_body(surf, player, ox, oy, tick):
    walk = player.on_ground and abs(player.vx) > 0.5
    step = int(math.sin(tick * 0.30) * 3) if walk else 0
    sw   = int(math.sin(tick * 0.30) * 3) if walk else 0

    pygame.draw.rect(surf, HAT,    (ox + 4, oy - 5, 12, 6))
    pygame.draw.rect(surf, HAT,    (ox + 1, oy,     18, 3))
    pygame.draw.rect(surf, SKIN,   (ox + 3, oy + 3, 14, 9))
    ex = ox + 5 if player.facing > 0 else ox + 4
    pygame.draw.rect(surf, EYE,    (ex,      oy + 5, 3, 3))
    pygame.draw.rect(surf, EYE,    (ex + 7,  oy + 5, 3, 3))
    pygame.draw.rect(surf, JACKET, (ox - 2,  oy + 12 + sw, 4, 8))
    pygame.draw.rect(surf, JACKET, (ox + 18, oy + 12 - sw, 4, 8))
    pygame.draw.rect(surf, JACKET, (ox + 2,  oy + 12, 16, 9))
    pygame.draw.rect(surf, PANTS,  (ox + 3,  oy + 21 + step, 6, 7))
    pygame.draw.rect(surf, PANTS,  (ox + 11, oy + 21 - step, 6, 7))


def draw_player(surf, player, cam_y, tick):
    px = int(player.x)
    py = int(player.y - cam_y)
    if not player.on_ground and player.speed_level > SPIN_THRESHOLD:
        tmp = pygame.Surface((60, 60), pygame.SRCALPHA)
        _draw_body(tmp, player, 20, 20, tick)
        rotated = pygame.transform.rotate(tmp, player.spin_angle)
        cx = px + 10
        cy = py + 10
        surf.blit(rotated, (cx - rotated.get_width() // 2,
                            cy - rotated.get_height() // 2))
    else:
        _draw_body(surf, player, px, py, tick)
