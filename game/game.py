import pygame
import random

from .constants import (W, H, WHITE, GOLD, CYAN, RED_C, YELLOW,
                        GRAVITY, JUMP_F, ACCEL, FRIC, MAX_V,
                        WALL_W, THEMES, TITLE, PLAY, DEAD)
from .platform import Platform, new_platform
from .player import Player
from . import leaderboard


class Game:
    def __init__(self, fonts):
        self.fonts   = fonts
        self.state   = TITLE
        self.lb      = leaderboard.load()
        self.tick    = 0
        self.blink   = 0
        self.snow    = [
            {'x': random.uniform(0, W), 'y': random.uniform(0, H),
             'r': random.uniform(0.8, 2.2),
             'sx': random.uniform(-0.25, 0.25),
             'sy': random.uniform(0.3, 1.0)}
            for _ in range(55)
        ]
        self._bgs    = [self._make_bg(t) for t in THEMES]
        self.pl      = None
        self.plats   = []
        self.cam_y   = 0.0
        self.score   = 0
        self.h_floor = 0
        self.combo   = 0
        self.c_timer = 0
        self.name_in = ''

    def _make_bg(self, theme):
        surf = pygame.Surface((W, H))
        bt, bb = theme['bg_top'], theme['bg_bot']
        for row in range(H):
            t = row / H
            r = int(bt[0] + (bb[0] - bt[0]) * t)
            g = int(bt[1] + (bb[1] - bt[1]) * t)
            b = int(bt[2] + (bb[2] - bt[2]) * t)
            pygame.draw.line(surf, (r, g, b), (0, row), (W, row))
        return surf

    def _theme(self):
        return THEMES[(self.h_floor // 100) % len(THEMES)]

    def start(self):
        self.state   = PLAY
        self.score   = 0
        self.h_floor = 0
        self.combo   = 0
        self.c_timer = 0
        self.tick    = 0
        self.name_in = ''
        self.plats   = []

        gnd = Platform(WALL_W, H - 30, W - WALL_W * 2, 0)
        self.plats.append(gnd)
        self.pl    = Player(W // 2 - 10, gnd.y - 28)
        self.cam_y = 0.0

        prev = gnd
        for i in range(1, 51):
            prev = new_platform(prev, i)
            self.plats.append(prev)

    def update(self, pressed, jump_now):
        if self.state != PLAY:
            return
        self.tick += 1
        pl = self.pl

        left  = pressed[pygame.K_LEFT]  or pressed[pygame.K_a]
        right = pressed[pygame.K_RIGHT] or pressed[pygame.K_d]

        if left or right:
            pl.speed_level = min(100, pl.speed_level + 0.4)
        else:
            pl.speed_level = max(0, pl.speed_level - 1.5)

        accel_mult = 1.0 + (pl.speed_level / 100) * 1.1
        spd_cap    = MAX_V + (pl.speed_level / 100) * 3.0

        if left:
            pl.facing = -1
            pl.vx -= ACCEL * accel_mult
            pl.vx  = max(-spd_cap, pl.vx)
        elif right:
            pl.facing = 1
            pl.vx += ACCEL * accel_mult
            pl.vx  = min(spd_cap, pl.vx)
        else:
            pl.vx *= FRIC
            if abs(pl.vx) < 0.08:
                pl.vx = 0.0

        if pl.on_ground:
            pl.coyote = 6
        if pl.coyote > 0:
            pl.coyote -= 1

        if jump_now and pl.coyote > 0:
            speed_ratio  = min(1.0, abs(pl.vx) / (MAX_V * 2.5))
            pl.vy        = JUMP_F - speed_ratio * 5.0
            pl.coyote    = 0
            pl.on_ground = False

        held = pressed[pygame.K_UP] or pressed[pygame.K_SPACE] or pressed[pygame.K_w]
        if not held and pl.vy < -5:
            pl.vy += 0.9

        pl.vy = min(pl.vy + GRAVITY, 22.0)
        pl.x += pl.vx
        pl.y += pl.vy

        if pl.x < WALL_W:
            pl.x      = float(WALL_W)
            pl.vx     = abs(pl.vx) * 0.55
            pl.facing = 1
        elif pl.x + pl.w > W - WALL_W:
            pl.x      = float(W - WALL_W - pl.w)
            pl.vx     = -abs(pl.vx) * 0.55
            pl.facing = -1

        pl.on_ground = False
        if pl.vy >= 0:
            for p in self.plats:
                feet  = pl.y + pl.h
                pfeet = feet - pl.vy
                if (pfeet <= p.y + 1 and feet >= p.y and
                        pl.x + pl.w > p.x + 2 and pl.x < p.x + p.w - 2):
                    pl.y         = float(p.y - pl.h)
                    pl.vy        = 0.0
                    pl.on_ground = True
                    if p.fl > self.h_floor:
                        gained       = p.fl - self.h_floor
                        self.combo   = self.combo + gained if self.c_timer > 0 else 1
                        self.c_timer = 90
                        self.h_floor = p.fl
                        self.score   = self.h_floor
                    break

        if pl.on_ground:
            pl.spin_angle = 0.0
        else:
            pl.spin_angle = (pl.spin_angle - max(2.0, abs(pl.vx) * 3.0)) % 360

        if self.c_timer > 0:
            self.c_timer -= 1
        else:
            self.combo = 0

        tgt = pl.y - H * 0.38
        if tgt < self.cam_y:
            self.cam_y = tgt

        top = self.plats[-1]
        while top.y - self.cam_y > -H * 0.6:
            top = new_platform(top, top.fl + 1)
            self.plats.append(top)

        self.plats = [p for p in self.plats
                      if -(H * 2) < p.y - self.cam_y < H + 320]

        if pl.y - self.cam_y > H + 80:
            self.state = DEAD

    def draw(self, screen):
        theme     = self._theme()
        theme_idx = (self.h_floor // 100) % len(THEMES)
        screen.blit(self._bgs[theme_idx], (0, 0))

        for s in self.snow:
            s['x'] = (s['x'] + s['sx']) % W
            s['y'] += s['sy']
            if s['y'] > H:
                s['y'] = 0.0
            pygame.draw.circle(screen, (210, 235, 255),
                               (int(s['x']), int(s['y'])), max(1, int(s['r'])))

        if self.state == TITLE:
            self._draw_title(screen)
            return

        self._draw_walls(screen, theme)

        for p in self.plats:
            p_theme = THEMES[(p.fl // 100) % len(THEMES)]
            p.draw(screen, self.cam_y, self.fonts, p_theme)

        if self.pl:
            self.pl.draw(screen, self.cam_y, self.tick)

        self._draw_hud(screen, theme)

        if self.state == DEAD:
            self._draw_dead(screen)

    def _draw_walls(self, screen, theme):
        brick_h = 30
        scroll  = int(-self.cam_y) % brick_h

        for x0 in (0, W - WALL_W):
            pygame.draw.rect(screen, theme['wall_i'], (x0, 0, WALL_W, H))

            for row in range(-brick_h, H + brick_h, brick_h):
                y = row + scroll
                pygame.draw.line(screen, theme['wall_o'], (x0, y), (x0 + WALL_W, y), 1)

            edge_x = x0 + WALL_W - 2 if x0 == 0 else x0
            pygame.draw.rect(screen, theme['wall_o'], (edge_x, 0, 2, H))

    def _draw_hud(self, screen, theme):
        hud = pygame.Surface((145, 80), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 115))
        screen.blit(hud, (5, 5))

        sc = self.fonts['md'].render(f'Floor {self.score}', True, WHITE)
        screen.blit(sc, (12, 9))

        best = self.lb[0]['score'] if self.lb else 0
        bt   = self.fonts['xs'].render(f'Best: {best}', True, (128, 222, 234))
        screen.blit(bt, (12, 38))

        th_name = self.fonts['xs'].render(theme['name'], True, theme['wall_o'])
        screen.blit(th_name, (12, 52))

        t = (self.pl.speed_level / 100) if self.pl else 0
        pygame.draw.rect(screen, (20, 20, 50), (12, 66, 120, 6))
        if t > 0:
            col = (int(41 + 198 * t), int(182 - 99 * t), int(246 - 166 * t))
            pygame.draw.rect(screen, col, (12, 66, int(120 * t), 6))

        if self.combo > 1:
            alpha = min(255, self.c_timer * 255 // 45)
            sz    = min(14, self.combo - 1)
            cs    = self.fonts['combo'][sz].render(f'x{self.combo} COMBO!', True, YELLOW)
            cs.set_alpha(alpha)
            screen.blit(cs, (W // 2 - cs.get_width() // 2, 60))

    def _draw_title(self, screen):
        self.blink = (self.blink + 1) % 64

        pan = pygame.Surface((W - 30, 163), pygame.SRCALPHA)
        pan.fill((4, 18, 36, 237))
        screen.blit(pan, (15, 18))
        pygame.draw.rect(screen, CYAN, (15, 18, W - 30, 163), 2)

        t = self.fonts['title'].render('ICY TOWER', True, CYAN)
        screen.blit(t, (W // 2 - t.get_width() // 2, 26))

        for i, ln in enumerate([
            'Arrow keys / WASD  to  move',
            'Up / Space  to  jump',
            'Bounce walls to build speed',
        ]):
            s = self.fonts['xs'].render(ln, True, (179, 229, 252))
            screen.blit(s, (W // 2 - s.get_width() // 2, 88 + i * 16))

        bc = (128, 222, 234) if self.blink < 32 else CYAN
        bt = self.fonts['sm'].render('SPACE  or  UP  to  play', True, bc)
        screen.blit(bt, (W // 2 - bt.get_width() // 2, 152))

        lbp = pygame.Surface((W - 30, H - 207), pygame.SRCALPHA)
        lbp.fill((4, 18, 36, 230))
        screen.blit(lbp, (15, 193))
        pygame.draw.rect(screen, GOLD, (15, 193, W - 30, H - 207), 2)

        lbt = self.fonts['md'].render('LEADERBOARD', True, GOLD)
        screen.blit(lbt, (W // 2 - lbt.get_width() // 2, 198))

        if not self.lb:
            nt = self.fonts['sm'].render('No records yet - play first!', True, (84, 110, 122))
            screen.blit(nt, (W // 2 - nt.get_width() // 2, 278))
        else:
            medal = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]
            for i, e in enumerate(self.lb[:8]):
                y   = 232 + i * 34
                col = medal[i] if i < 3 else (207, 216, 220)
                fnt = self.fonts['lb_b'] if i < 3 else self.fonts['lb_r']
                row = fnt.render(f"{i+1}. {e['name']}  -  Floor {e['score']}", True, col)
                screen.blit(row, (W // 2 - row.get_width() // 2, y))

    def _draw_dead(self, screen):
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 210))
        screen.blit(ov, (0, 0))

        go = self.fonts['lg'].render('GAME OVER', True, RED_C)
        screen.blit(go, (W // 2 - go.get_width() // 2, 110))

        sc = self.fonts['md'].render(f'You reached Floor {self.score}', True, WHITE)
        screen.blit(sc, (W // 2 - sc.get_width() // 2, 158))

        best = self.lb[0]['score'] if self.lb else 0
        if self.score > 0 and self.score >= best:
            hs = self.fonts['sm'].render('NEW HIGH SCORE!', True, GOLD)
            screen.blit(hs, (W // 2 - hs.get_width() // 2, 190))

        pr = self.fonts['sm'].render('Enter your name:', True, (179, 229, 252))
        screen.blit(pr, (W // 2 - pr.get_width() // 2, 238))

        box = pygame.Rect(W // 2 - 115, 258, 230, 44)
        pygame.draw.rect(screen, (0, 18, 38), box)
        pygame.draw.rect(screen, CYAN, box, 2)

        cur = '|' if (pygame.time.get_ticks() // 500) % 2 == 0 else ' '
        if self.name_in:
            ni = self.fonts['ni'].render(self.name_in + cur, True, WHITE)
            screen.blit(ni, (W // 2 - ni.get_width() // 2, 267))
        else:
            ph = self.fonts['sm'].render('type your name...' + cur, True, (69, 90, 100))
            screen.blit(ph, (W // 2 - ph.get_width() // 2, 272))

        ht = self.fonts['sm'].render('ENTER to save score', True, (128, 222, 234))
        screen.blit(ht, (W // 2 - ht.get_width() // 2, 320))

    def submit_score(self):
        name = self.name_in.strip() or 'ANON'
        self.lb.append({'name': name, 'score': self.score})
        self.lb.sort(key=lambda x: -x['score'])
        self.lb = self.lb[:10]
        leaderboard.save(self.lb)
        self.state = TITLE
