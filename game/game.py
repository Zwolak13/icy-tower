import pygame

from .constants import (W, H, GRAVITY, JUMP_F, ACCEL, FRIC, MAX_V,
                        WALL_W, THEMES, TITLE, PLAY, DEAD)
from .entities.platform import Platform
from .entities.player import Player
from .generate.platforms import new_platform
from .generate.background import make_bg, make_snow, draw_snow
from .draw.player import draw_player
from .draw.platform import draw_platform
from .draw.hud import draw_walls, draw_hud
from .draw.screens import draw_title, draw_dead
from . import leaderboard


class Game:
    def __init__(self, fonts):
        self.fonts   = fonts
        self.state   = TITLE
        self.lb      = leaderboard.load()
        self.tick    = 0
        self.blink   = 0
        self.snow    = make_snow()
        self._bgs    = [make_bg(t) for t in THEMES]
        self.pl      = None
        self.plats   = []
        self.cam_y   = 0.0
        self.score   = 0
        self.h_floor = 0
        self.combo   = 0
        self.c_timer = 0
        self.name_in = ''

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
        draw_snow(screen, self.snow)

        if self.state == TITLE:
            self.blink = (self.blink + 1) % 64
            draw_title(screen, self.fonts, self.lb, self.blink)
            return

        draw_walls(screen, theme, self.cam_y)

        for p in self.plats:
            p_theme = THEMES[(p.fl // 100) % len(THEMES)]
            draw_platform(screen, p, self.cam_y, self.fonts, p_theme)

        if self.pl:
            draw_player(screen, self.pl, self.cam_y, self.tick)

        draw_hud(screen, self.fonts, self.score, self.lb, theme, self.pl, self.combo, self.c_timer)

        if self.state == DEAD:
            draw_dead(screen, self.fonts, self.score, self.lb, self.name_in)

    def submit_score(self):
        name = self.name_in.strip() or 'ANON'
        self.lb.append({'name': name, 'score': self.score})
        self.lb.sort(key=lambda x: -x['score'])
        self.lb = self.lb[:10]
        leaderboard.save(self.lb)
        self.state = TITLE
