import pygame

from ..constants import H


def draw_platform(surf, platform, cam_y, fonts, theme):
    sy = int(platform.y - cam_y)
    if sy < -20 or sy > H + 20:
        return
    pygame.draw.rect(surf, theme['top'], (platform.x, sy,     platform.w, 6))
    pygame.draw.rect(surf, theme['bot'], (platform.x, sy + 6, platform.w, 6))

    if platform.safe:
        pygame.draw.rect(surf, (255, 215, 0), (platform.x, sy, platform.w, platform.h), 2)
        lbl = fonts['sm'].render(f'Floor {platform.fl}', True, (255, 235, 100))
        surf.blit(lbl, (platform.x + platform.w // 2 - lbl.get_width() // 2, sy - 16))
    elif platform.fl > 0 and platform.fl % 10 == 0:
        lbl = fonts['xs'].render(str(platform.fl), True, (220, 235, 255))
        surf.blit(lbl, (platform.x + platform.w // 2 - lbl.get_width() // 2, sy - 13))
