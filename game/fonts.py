import pygame


def create():
    return {
        'title': pygame.font.SysFont('Courier New', 40, bold=True),
        'lg':    pygame.font.SysFont('Courier New', 32, bold=True),
        'md':    pygame.font.SysFont('Courier New', 20, bold=True),
        'sm':    pygame.font.SysFont('Courier New', 14),
        'xs':    pygame.font.SysFont('Courier New', 11),
        'lb_b':  pygame.font.SysFont('Courier New', 15, bold=True),
        'lb_r':  pygame.font.SysFont('Courier New', 15),
        'ni':    pygame.font.SysFont('Courier New', 20, bold=True),
        'combo': [pygame.font.SysFont('Courier New', 14 + i, bold=True) for i in range(15)],
    }
