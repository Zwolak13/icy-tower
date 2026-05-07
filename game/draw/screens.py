import pygame

from ..constants import W, H, WHITE, GOLD, CYAN, RED_C


def draw_title(screen, fonts, lb, blink):
    pan = pygame.Surface((W - 30, 163), pygame.SRCALPHA)
    pan.fill((4, 18, 36, 237))
    screen.blit(pan, (15, 18))
    pygame.draw.rect(screen, CYAN, (15, 18, W - 30, 163), 2)

    t = fonts['title'].render('ICY TOWER', True, CYAN)
    screen.blit(t, (W // 2 - t.get_width() // 2, 26))

    for i, ln in enumerate([
        'Arrow keys / WASD  to  move',
        'Up / Space  to  jump',
        'Bounce walls to build speed',
    ]):
        s = fonts['xs'].render(ln, True, (179, 229, 252))
        screen.blit(s, (W // 2 - s.get_width() // 2, 88 + i * 16))

    bc = (128, 222, 234) if blink < 32 else CYAN
    bt = fonts['sm'].render('SPACE  or  UP  to  play', True, bc)
    screen.blit(bt, (W // 2 - bt.get_width() // 2, 152))

    lbp = pygame.Surface((W - 30, H - 207), pygame.SRCALPHA)
    lbp.fill((4, 18, 36, 230))
    screen.blit(lbp, (15, 193))
    pygame.draw.rect(screen, GOLD, (15, 193, W - 30, H - 207), 2)

    lbt = fonts['md'].render('LEADERBOARD', True, GOLD)
    screen.blit(lbt, (W // 2 - lbt.get_width() // 2, 198))

    if not lb:
        nt = fonts['sm'].render('No records yet - play first!', True, (84, 110, 122))
        screen.blit(nt, (W // 2 - nt.get_width() // 2, 278))
    else:
        medal = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]
        for i, e in enumerate(lb[:8]):
            y   = 232 + i * 34
            col = medal[i] if i < 3 else (207, 216, 220)
            fnt = fonts['lb_b'] if i < 3 else fonts['lb_r']
            row = fnt.render(f"{i+1}. {e['name']}  -  Floor {e['score']}", True, col)
            screen.blit(row, (W // 2 - row.get_width() // 2, y))


def draw_dead(screen, fonts, score, lb, name_in):
    ov = pygame.Surface((W, H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 210))
    screen.blit(ov, (0, 0))

    go = fonts['lg'].render('GAME OVER', True, RED_C)
    screen.blit(go, (W // 2 - go.get_width() // 2, 110))

    sc = fonts['md'].render(f'You reached Floor {score}', True, WHITE)
    screen.blit(sc, (W // 2 - sc.get_width() // 2, 158))

    best = lb[0]['score'] if lb else 0
    if score > 0 and score >= best:
        hs = fonts['sm'].render('NEW HIGH SCORE!', True, GOLD)
        screen.blit(hs, (W // 2 - hs.get_width() // 2, 190))

    pr = fonts['sm'].render('Enter your name:', True, (179, 229, 252))
    screen.blit(pr, (W // 2 - pr.get_width() // 2, 238))

    box = pygame.Rect(W // 2 - 115, 258, 230, 44)
    pygame.draw.rect(screen, (0, 18, 38), box)
    pygame.draw.rect(screen, CYAN, box, 2)

    cur = '|' if (pygame.time.get_ticks() // 500) % 2 == 0 else ' '
    if name_in:
        ni = fonts['ni'].render(name_in + cur, True, WHITE)
        screen.blit(ni, (W // 2 - ni.get_width() // 2, 267))
    else:
        ph = fonts['sm'].render('type your name...' + cur, True, (69, 90, 100))
        screen.blit(ph, (W // 2 - ph.get_width() // 2, 272))

    ht = fonts['sm'].render('ENTER to save score', True, (128, 222, 234))
    screen.blit(ht, (W // 2 - ht.get_width() // 2, 320))
