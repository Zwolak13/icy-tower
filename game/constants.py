W, H    = 400, 600
FPS     = 60
WALL_W  = 18

WHITE   = (255, 255, 255)
GOLD    = (255, 215,  64)
CYAN    = ( 41, 182, 246)
RED_C   = (239,  83,  80)
BLUE_C  = ( 25, 118, 210)
DK_BLUE = ( 13,  71, 161)
SKIN    = (255, 204, 188)
YELLOW  = (255, 235,  59)

GRAVITY = 0.45
JUMP_F  = -13.5
ACCEL   = 0.55
FRIC    = 0.80
MAX_V   = 6.5

SPIN_THRESHOLD = 55

TITLE, PLAY, DEAD = 0, 1, 2

THEMES = [
    dict(name='Ice',
         top=(128, 222, 234), bot=(  0, 151, 167), shine=(180, 240, 248),
         wall_o=( 90, 210, 235), wall_i=( 30, 120, 170),
         bg_top=(  4,  12,  24), bg_bot=( 12,  42,  66)),

    dict(name='Cave',
         top=(158, 158, 158), bot=( 90,  90,  90), shine=(205, 205, 205),
         wall_o=(130, 130, 130), wall_i=( 55,  55,  55),
         bg_top=( 15,  10,   8), bg_bot=( 40,  28,  20)),

    dict(name='Inferno',
         top=(255, 152,   0), bot=(183,  28,  28), shine=(255, 210, 120),
         wall_o=(220,  90,  20), wall_i=(120,  22,   5),
         bg_top=( 35,   5,   0), bg_bot=( 90,  15,   5)),

    dict(name='Cyber',
         top=(206, 147, 216), bot=(106,  27, 154), shine=(240, 200, 255),
         wall_o=(175,  85, 205), wall_i=( 65,   0, 125),
         bg_top=(  8,   0,  18), bg_bot=( 25,   0,  55)),

    dict(name='Desert',
         top=(255, 213,  79), bot=(230, 162,   0), shine=(255, 245, 180),
         wall_o=(235, 185,  45), wall_i=(165, 118,  12),
         bg_top=( 28,  18,   0), bg_bot=( 75,  50,   5)),

    dict(name='Ocean',
         top=(100, 181, 246), bot=( 13,  71, 161), shine=(190, 230, 255),
         wall_o=( 60, 140, 220), wall_i=(  8,  52, 128),
         bg_top=(  0,   5,  18), bg_bot=(  0,  15,  55)),

    dict(name='Forest',
         top=(129, 199, 132), bot=( 46, 125,  50), shine=(200, 240, 200),
         wall_o=( 95, 165,  95), wall_i=( 33,  90,  33),
         bg_top=(  3,  12,   3), bg_bot=(  8,  35,   8)),

    dict(name='Space',
         top=( 96, 125, 139), bot=( 38,  50,  56), shine=(160, 180, 190),
         wall_o=( 52,  72,  84), wall_i=( 20,  30,  36),
         bg_top=(  2,   2,   8), bg_bot=(  5,   5,  20)),

    dict(name='Candy',
         top=(255, 128, 171), bot=(173,  20,  87), shine=(255, 210, 230),
         wall_o=(235,  85, 145), wall_i=(145,   6,  60),
         bg_top=( 25,   0,  12), bg_bot=( 70,   5,  35)),

    dict(name='Ancient',
         top=(188, 170, 164), bot=(109,  76,  65), shine=(220, 200, 195),
         wall_o=(155, 135, 115), wall_i=( 90,  65,  50),
         bg_top=( 18,  12,   8), bg_bot=( 50,  35,  20)),
]
