import pygame
import os
from PIL import Image
import math
from Sounds import sounds
SPRITE_PATH = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "Sprites",
    "ERAM"
)
SPRITE_SCALE = 1

def load_gif(file_name):

    path = os.path.join(SPRITE_PATH, file_name)

    gif = Image.open(path)

    frames = []

    for frame_number in range(gif.n_frames):

        gif.seek(frame_number)

        frame = gif.convert("RGBA")

        frame = pygame.image.fromstring(
            frame.tobytes(),
            frame.size,
            "RGBA"
        )

        width = frame.get_width() * SPRITE_SCALE
        height = frame.get_height() * SPRITE_SCALE

        frame = pygame.transform.scale(
            frame,
            (width, height)
        )

        frames.append(frame)

    return frames

# ============================================================
# ЗАГРУЗКА АНИМАЦИЙ
# ============================================================

eram_laugh = load_gif("Shadow_Mantle_holder_battle_laughing.gif")
eram_static = load_gif("Shadow_Mantle_holder_battle_idle.gif")
eram_blyat = load_gif("Shadow_Mantle_holder_battle_shooting.gif")
eram_fly = load_gif("Shadow_Mantle_holder_battle_deploy.gif")
eram_fire = load_gif("Shadow_Mantle_holder_battle_flames.gif")

# ============================================================
# ДЛЯ КЛОНОВ
# ============================================================

def make_orange_animation(animation):
    orange_animation = []

    for frame in animation:

        new_frame = frame.copy()

        for x in range(new_frame.get_width()):
            for y in range(new_frame.get_height()):

                color = new_frame.get_at((x, y))

                if color.a > 0:
                    brightness = max(color.r, color.g, color.b)

                    new_color = (
                        min(255, brightness),
                        min(180, int(brightness * 0.55)),
                        0,
                        color.a
                    )

                    new_frame.set_at(
                        (x, y),
                        new_color
                    )

        orange_animation.append(new_frame)

    return orange_animation

class Eram:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.move_time = 0
        self.move_center_x = x
        self.move_center_y = y

        self.infinity_width = 280
        self.infinity_height = 200
        self.moving = False

        # Начальная анимация
        self.animation = eram_static

        self.frame = 0

        self.animation_speed = 90  # миллисекунд на кадр
        self.animation_timer = 0

        # ХП
        self.max_hp = 30
        self.hp = 30

        #Клоны
        self.is_clone = False

    def update(self, dt):

        if self.moving:
            self.move_infinity(dt)

        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame += 1

            if self.frame >= len(self.animation):
                self.frame = 0

    def draw(self, surface):

        if not self.animation:
            return

        image = self.animation[self.frame]

        surface.blit(
            image,
            (self.x, self.y)
        )

    def set_animation(self, animation):
        self.animation = animation
        self.frame = 0
        self.animation_timer = 0

    def get_hitbox(self):
        return pygame.Rect(
            self.x,
            self.y,
            100,
            100
        )

    def take_damage(self, damage):
        self.hp -= damage
        sounds["md"].play()
        if self.hp < 0:
            self.hp = 0

    def move_infinity(self, dt):

        self.move_time += dt * 0.001

        self.x = (
                self.move_center_x
                + math.sin(self.move_time) * self.infinity_width
        )

        self.y = (
                self.move_center_y
                + math.sin(self.move_time * 2) * self.infinity_height
        )
class Projectile:

    def __init__(self, x, y, angle, speed=4, damage=1):

        self.x = x
        self.y = y

        self.angle = angle
        self.speed = speed
        self.damage = damage

        self.size = 24
        self.damage_cooldown = 0
    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

    def draw(self, surface):

        pygame.draw.circle(
            surface,
            (255, 120, 0),
            (int(self.x), int(self.y)),
            self.size // 2
        )

    def get_hitbox(self):

        return pygame.Rect(
            int(self.x - self.size // 2),
            int(self.y - self.size // 2),
            self.size,
            self.size
        )
