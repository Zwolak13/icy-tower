import pygame

from ..constants import W, H, WALL_W, WHITE, YELLOW


def draw_walls(screen, theme, cam_y):
    brick_h = 30
    scroll  = int(-cam_y) % brick_h

    for x0 in (0, W - WALL_W):
        pygame.draw.rect(screen, theme['wall_i'], (x0, 0, WALL_W, H))

        for row in range(-brick_h, H + brick_h, brick_h):
            y = row + scroll
            pygame.draw.line(screen, theme['wall_o'], (x0, y), (x0 + WALL_W, y), 1)

        edge_x = x0 + WALL_W - 2 if x0 == 0 else x0
        pygame.draw.rect(screen, theme['wall_o'], (edge_x, 0, 2, H))


def draw_hud(screen, fonts, score, lb, theme, player, combo, c_timer):
    hud = pygame.Surface((145, 80), pygame.SRCALPHA)
    hud.fill((0, 0, 0, 115))
    screen.blit(hud, (5, 5))

    sc = fonts['md'].render(f'Floor {score}', True, WHITE)
    screen.blit(sc, (12, 9))

    best = lb[0]['score'] if lb else 0
    bt   = fonts['xs'].render(f'Best: {best}', True, (128, 222, 234))
    screen.blit(bt, (12, 38))

    th_name = fonts['xs'].render(theme['name'], True, theme['wall_o'])
    screen.blit(th_name, (12, 52))

    t = (player.speed_level / 100) if player else 0
    pygame.draw.rect(screen, (20, 20, 50), (12, 66, 120, 6))
    if t > 0:
        col = (int(41 + 198 * t), int(182 - 99 * t), int(246 - 166 * t))
        pygame.draw.rect(screen, col, (12, 66, int(120 * t), 6))

    if combo > 1:
        alpha = min(255, c_timer * 255 // 45)
        sz    = min(14, combo - 1)
        cs    = fonts['combo'][sz].render(f'x{combo} COMBO!', True, YELLOW)
        cs.set_alpha(alpha)
        screen.blit(cs, (W // 2 - cs.get_width() // 2, 60))
