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
