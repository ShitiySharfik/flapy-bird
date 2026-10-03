import pygame
import os
from Sounds import sounds

# ============================================================
# НАСТРОЙКИ АНИМАЦИИ
# ============================================================

SPRITE_PATH = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "Sprites",
    "HERO_SWORD"
)
SPRITE_SCALE = 4

def load_animation(folder_name):

    folder = os.path.join(SPRITE_PATH, folder_name)

    files = [
        file for file in os.listdir(folder)
        if file.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    files.sort()

    frames = []

    for file in files:

        image = pygame.image.load(
            os.path.join(folder, file)
        )

        width = image.get_width() * SPRITE_SCALE
        height = image.get_height() * SPRITE_SCALE

        image = pygame.transform.scale(
            image,
            (width, height)
        )

        frames.append(image)

    return frames



# ============================================================
# ЗАГРУЗКА АНИМАЦИЙ
# ============================================================

walk_down = load_animation(
    "spr_board_kris_walk_down"
)

walk_left = load_animation(
    "spr_board_kris_walk_left"
)

walk_right = load_animation(
    "spr_board_kris_walk_right"
)

walk_up = load_animation(
    "spr_board_kris_walk_up"
)


strike_down = load_animation(
    "spr_board_kris_strike_down"
)

strike_left = load_animation(
    "spr_board_kris_strike_left"
)

strike_right = load_animation(
    "spr_board_kris_strike_right"
)

strike_up = load_animation(
    "spr_board_kris_strike_up"
)


hurt = load_animation(
    "spr_board_kris_hurt"
)


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.width = 32
        self.height = 32
        self.hitbox_width = 20
        self.hitbox_height = 16
        self.speed = 3.8

        #для атак
        self.state = "attack"

        # Направление, в котором игрок смотрит
        self.direction = "down"

        #ХП
        self.max_hp = 6
        self.hp = 6

        # УРОН
        self.damage = 0.5

        # Состояние анимации
        self.state = "idle"

        self.frame = 0
        self.animation_timer = 0

        # Скорость смены кадров
        self.animation_speed = 12
        self.attack_speed = 6

        #Для атак
        self.attack_hit = False
        #Кадры ОБСОЛЮТНОГО БЕЗСМЕРТИЯ
        self.invincibility_timer = 0
        self.invincibility_duration = 500

    # ========================================================
    # ПОЛУЧИТЬ ХИТБОКС
    # ========================================================

    def take_damage(self, damage):

        if self.invincibility_timer > 0:
            return

        sounds["kd"].play()

        self.hp -= damage

        self.invincibility_timer = self.invincibility_duration

        if self.hp < 0:
            self.hp = 0

    # ========================================================
    # ПОЛУЧИТЬ ХИТБОКС
    # ========================================================

    def get_hitbox(self):

        return pygame.Rect(
            self.x + 22,
            self.y + 40,
            self.hitbox_width,
            self.hitbox_height
        )



    # ========================================================
    # ПОЛУЧИТЬ ТЕКУЩУЮ АНИМАЦИЮ
    # ========================================================

    def get_animation(self):

        if self.state == "walk":

            if self.direction == "down":
                return walk_down

            if self.direction == "up":
                return walk_up

            if self.direction == "left":
                return walk_left

            if self.direction == "right":
                return walk_right


        if self.state == "attack":

            if self.direction == "down":
                return strike_down

            if self.direction == "up":
                return strike_up

            if self.direction == "left":
                return strike_left

            if self.direction == "right":
                return strike_right


        if self.state == "hurt":

            return hurt


        # IDLE
        # Берём первый кадр walk-анимации

        if self.direction == "down":
            return walk_down

        if self.direction == "up":
            return walk_up

        if self.direction == "left":
            return walk_left

        if self.direction == "right":
            return walk_right


    # ========================================================
    # АТАКА
    # ========================================================

    def attack(self):
        # Нельзя начать новую атаку во время старой
        if self.state == "attack":
            return

        self.state = "attack"
        self.frame = 0
        self.animation_timer = 0
        self.attack_hit = False

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, arena):

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 16

        if self.state == "attack":
            animation = self.get_animation()

            self.animation_timer += 1

            if self.animation_timer >= self.attack_speed:
                self.animation_timer = 0
                self.frame += 1

            if self.frame >= len(animation):
                self.frame = 0
                self.state = "idle"

            return

        keys = pygame.key.get_pressed()

        new_x = self.x
        new_y = self.y

        moving = False


        if keys[pygame.K_LEFT]:

            new_x -= self.speed

            self.direction = "left"

            moving = True


        if keys[pygame.K_RIGHT]:

            new_x += self.speed

            self.direction = "right"

            moving = True


        if keys[pygame.K_UP]:

            new_y -= self.speed

            self.direction = "up"

            moving = True


        if keys[pygame.K_DOWN]:

            new_y += self.speed

            self.direction = "down"

            moving = True


        # Проверяем столкновение с ареной

        new_hitbox = pygame.Rect(
            new_x + 22,
            new_y + 40,
            self.hitbox_width,
            self.hitbox_height
        )

        if not arena.is_blocked_rect(new_hitbox):
            self.x = new_x
            self.y = new_y

        # Состояние

        if moving:

            self.state = "walk"

        else:

            self.state = "idle"


        # ====================================================
        # АНИМАЦИЯ
        # ====================================================

        if moving:

            self.animation_timer += 1

            if self.animation_timer >= self.animation_speed:

                self.animation_timer = 0

                self.frame += 1

        else:

            self.frame = 0
            self.animation_timer = 0


        animation = self.get_animation()


        if self.frame >= len(animation):

            self.frame = 0


    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):

        if self.invincibility_timer > 0:

            if (self.invincibility_timer // 3) % 2 == 0:
                return

        animation = self.get_animation()

        # Если это idle — всегда первый кадр
        if self.state == "idle":

            frame = animation[0]

        else:

            frame = animation[self.frame]

        draw_x = self.x
        draw_y = self.y

        if self.state == "attack":
            if self.direction == "left":
                draw_x -= frame.get_width() - 64

            if self.direction == "up":
                draw_y -= frame.get_height() - 64

            if self.direction == "down":
                pass

            if self.direction == "right":
                pass

        surface.blit(
            frame,
            (draw_x, draw_y)
        )

    def get_attack_hitbox(self):

            if self.state != "attack":
                return None

            if self.direction == "up":
                return pygame.Rect(
                    self.x + 15,
                    self.y - 20,
                    35,
                    40
                )

            if self.direction == "down":
                return pygame.Rect(
                    self.x + 15,
                    self.y + 55,
                    35,
                    40
                )

            if self.direction == "left":
                return pygame.Rect(
                    self.x - 20,
                    self.y + 20,
                    40,
                    35
                )

            if self.direction == "right":
                return pygame.Rect(
                    self.x + 55,
                    self.y + 20,
                    40,
                    35
                )

            return None
