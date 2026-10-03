import pygame
import random
import os
from PIL import Image
from Sounds import sounds


BASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "Sprites",
    "FRIEND"
)

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]



# ============================================================
# GIF ЗАГРУЗКА
# ============================================================

def load_gif(filename):

    path = os.path.join(BASE_PATH, filename)

    gif = Image.open(path)

    frames = []

    for i in range(gif.n_frames):

        gif.seek(i)

        frame = gif.convert("RGBA")

        frame = pygame.image.fromstring(
            frame.tobytes(),
            frame.size,
            "RGBA"
        )

        frames.append(frame)

    return frames


# ============================================================
# СПРАЙТЫ
# ============================================================

friend_image = pygame.image.load(
    os.path.join(
        BASE_PATH,
        "FRIEND_battle_8bit.png"
    )
)


friend_hurt_image = pygame.image.load(
    os.path.join(
        BASE_PATH,
        "FRIEND_battle_8bit_hurt.png"
    )
)


appear_animation = load_gif(
    "FRIEND_battle_8bit_appear.gif"
)


death_animation = load_gif(
    "FRIEND_overworld_8bit_laugh.gif"
)


# ============================================================
# FRIEND
# ============================================================

class Friend:

    def __init__(self, x, y, arena):

        self.x = x
        self.y = y
        self.arena = arena
        self.width = friend_image.get_width()
        self.height = friend_image.get_height()

        # 1 удар = смерть
        self.hp = 0.1

        # Состояние
        self.state = "appear"

        # GIF
        self.frame = 0
        self.animation_timer = 0

        self.animation_speed = 80

        # Появление
        self.appear_finished = False

        # Получение урона
        self.hurt_timer = 0

        # Смерть
        self.dead = False

        # Движение
        self.direction_x, self.direction_y = random.choice(directions)

        self.change_direction_timer = random.randint(
            500,
            1500
        )

        self.speed = 4

        # Нанесение урона
        self.damage_cooldown = 0

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt, player):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

        # ----------------------------------------------------
        # ПОЯВЛЕНИЕ
        # ----------------------------------------------------

        if self.state == "appear":

            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:

                self.animation_timer = 0
                self.frame += 1

                if self.frame >= len(appear_animation):
                    self.frame = 0
                    self.state = "move"

            return

        # ----------------------------------------------------
        # ПОЛУЧИЛ УДАР
        # ----------------------------------------------------

        if self.state == "hurt":

            self.hurt_timer -= dt

            if self.hurt_timer <= 0:
                sounds["md"].play()
                self.state = "death"

                self.frame = 0
                self.animation_timer = 0

            return

        # ----------------------------------------------------
        # СМЕРТЬ
        # ----------------------------------------------------

        if self.state == "death":

            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:

                self.animation_timer = 0
                self.frame += 1

                if self.frame >= len(death_animation):

                    self.dead = True

            return

        # ----------------------------------------------------
        # ДВИЖЕНИЕ
        # ----------------------------------------------------

        if self.state == "move":

            self.change_direction_timer -= dt

            if self.change_direction_timer <= 0:
                self.direction_x = random.choice([-1, 0, 1])
                self.direction_y = random.choice([-1, 0, 1])

                self.change_direction_timer = random.randint(
                    500,
                    1500
                )

            new_x = self.x + self.direction_x * self.speed
            new_y = self.y + self.direction_y * self.speed

            test_rect = pygame.Rect(
                int(new_x),
                int(new_y),
                self.width,
                self.height
            )

            if not self.arena.is_blocked_rect(test_rect):

                self.x = new_x
                self.y = new_y

            else:

                self.direction_x, self.direction_y = random.choice([
                    (-1, 0),
                    (1, 0),
                    (0, -1),
                    (0, 1)
                ])

            # УРОН
            if self.damage_cooldown <= 0:

                if self.get_hitbox().colliderect(
                        player.get_hitbox()
                ):
                    player.take_damage(1)
                    self.damage_cooldown = 500

    # ========================================================
    # УРОН
    # ========================================================

    def take_damage(self):

        if self.state in (
            "hurt",
            "death"
        ):
            return

        self.hp -= 1

        if self.hp <= 0:

            self.state = "hurt"

            self.hurt_timer = 100

            self.frame = 0
            self.animation_timer = 0

    # ========================================================
    # HITBOX
    # ========================================================

    def get_hitbox(self):

        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):

        if self.state == "appear":

            image = appear_animation[
                min(
                    self.frame,
                    len(appear_animation) - 1
                )
            ]

        elif self.state == "hurt":

            image = friend_hurt_image

        elif self.state == "death":

            image = death_animation[
                min(
                    self.frame,
                    len(death_animation) - 1
                )
            ]

        else:

            image = friend_image

        surface.blit(
            image,
            (
                int(self.x),
                int(self.y)
            )
        )

    # ========================================================
    # КОНФЕТА
    # ========================================================

    def should_drop_candy(self):

        return random.random() < 0.33
