import random

from ..constants import W, WALL_W
from ..entities.platform import Platform


def new_platform(prev, fl):
    t   = min(fl / 200.0, 1.0)
    gap = int(62 + t * 58)
    y   = prev.y - gap

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
