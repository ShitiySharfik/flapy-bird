import random
import pygame
import math
from MANTLE_HOLDER import Eram, eram_laugh, eram_static, eram_fire, eram_fly, eram_blyat, Projectile
from Sounds import sounds
from FRIEND import Friend

fire_image = pygame.image.load("assets/Sprites/OTHERS/spr_board_fire/spr_board_fire_0.png")
fire_image = pygame.transform.scale(
    fire_image,
    (32, 32)
)
bomb_images = []

for i in range(2):

    image = pygame.image.load(
        f"assets/Sprites/OTHERS/spr_board_bomb_generic/"
        f"spr_board_bomb_generic_{i}.png"
    )

    image = pygame.transform.scale(
        image,
        (32, 32)
    )

    bomb_images.append(image)

candy_image = pygame.image.load(
    "assets/Sprites/OTHERS/spr_board_candy.png"
)

candy_image = pygame.transform.scale(
    candy_image,
    (64, 64)
)
class Bomb:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.timer = 0
        self.exploded = False

        self.damage_cooldown = 0
        self.explosion_timer = 0
        self.dead = False

        self.fire_duration = 800

        self.fire_length = 5
        self.fire_size = 32

        self.size = 64

        # Анимация бомбы
        self.animation_timer = 0
        self.animation_frame = 0

    def update(self, dt):

        # Кулдаун урона
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

        # Пока бомба НЕ взорвалась
        if not self.exploded:

            self.timer += dt

            # Анимация бомбы
            self.animation_timer += dt

            if self.animation_timer >= 300:
                self.animation_timer = 0
                self.animation_frame += 1

                if self.animation_frame >= len(bomb_images):
                    self.animation_frame = 0

            # 1.5 секунды → взрыв
            if self.timer >= 1500:
                self.exploded = True
                self.explosion_timer = 0

        # После взрыва
        else:

            self.explosion_timer += dt

            if self.explosion_timer >= self.fire_duration:
                self.dead = True

    def draw(self, surface):

        # -------------------------
        # БОМБА
        # -------------------------

        if not self.exploded:

            bomb_image = bomb_images[self.animation_frame]

            surface.blit(
                bomb_image,
                (
                    int(self.x - bomb_image.get_width() // 2),
                    int(self.y - bomb_image.get_height() // 2)
                )
            )

        # -------------------------
        # ОГОНЬ
        # -------------------------

        else:

            center_x = int(self.x)
            center_y = int(self.y)

            # Центральный огонь
            surface.blit(
                fire_image,
                (
                    center_x - fire_image.get_width() // 2,
                    center_y - fire_image.get_height() // 2
                )
            )

            # Вверх / вниз
            for i in range(1, self.fire_length + 1):

                # Вверх
                surface.blit(
                    fire_image,
                    (
                        center_x - fire_image.get_width() // 2,
                        center_y
                        - i * self.fire_size
                        - fire_image.get_height() // 2
                    )
                )

                # Вниз
                surface.blit(
                    fire_image,
                    (
                        center_x - fire_image.get_width() // 2,
                        center_y
                        + i * self.fire_size
                        - fire_image.get_height() // 2
                    )
                )

            # Влево / вправо
            for i in range(1, self.fire_length + 1):

                # Влево
                surface.blit(
                    fire_image,
                    (
                        center_x
                        - i * self.fire_size
                        - fire_image.get_width() // 2,
                        center_y - fire_image.get_height() // 2
                    )
                )

                # Вправо
                surface.blit(
                    fire_image,
                    (
                        center_x
                        + i * self.fire_size
                        - fire_image.get_width() // 2,
                        center_y - fire_image.get_height() // 2
                    )
                )

    def get_fire_hitboxes(self):

        if not self.exploded:
            return []

        hitboxes = []

        center_x = int(self.x)
        center_y = int(self.y)

        # Центр
        hitboxes.append(
            pygame.Rect(
                center_x - self.fire_size // 2,
                center_y - self.fire_size // 2,
                self.fire_size,
                self.fire_size
            )
        )

        # Вверх / вниз
        for i in range(1, self.fire_length + 1):

            hitboxes.append(
                pygame.Rect(
                    center_x - self.fire_size // 2,
                    center_y
                    - i * self.fire_size
                    - self.fire_size // 2,
                    self.fire_size,
                    self.fire_size
                )
            )

            hitboxes.append(
                pygame.Rect(
                    center_x - self.fire_size // 2,
                    center_y
                    + i * self.fire_size
                    - self.fire_size // 2,
                    self.fire_size,
                    self.fire_size
                )
            )

        # Влево / вправо
        for i in range(1, self.fire_length + 1):

            hitboxes.append(
                pygame.Rect(
                    center_x
                    - i * self.fire_size
                    - self.fire_size // 2,
                    center_y - self.fire_size // 2,
                    self.fire_size,
                    self.fire_size
                )
            )

            hitboxes.append(
                pygame.Rect(
                    center_x
                    + i * self.fire_size
                    - self.fire_size // 2,
                    center_y - self.fire_size // 2,
                    self.fire_size,
                    self.fire_size
                )
            )

        return hitboxes

class Candy:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.size = 100

    def get_hitbox(self):

        return pygame.Rect(
            int(self.x - self.size // 2),
            int(self.y - self.size // 2),
            self.size,
            self.size
        )

    def draw(self, surface):
        surface.blit(
            candy_image,
            (
                int(self.x - candy_image.get_width() // 2),
                int(self.y - candy_image.get_height() // 2)
            )
        )

class ProjectileWall:

    def __init__(self, y, gap_x, speed=3):
        self.x = 800
        self.y = y

        # СКОРОСТЬ СТЕНЫ
        self.speed = speed

        self.width = 28

        # Центр прохода
        self.gap_x = gap_x

        # Ширина прохода
        self.gap_width = 130

        self.damage_cooldown = 0
        self.dead = False

    def update(self, dt, player):

        # ------------------------------------------
        # ДВИЖЕНИЕ СТЕНЫ
        # ------------------------------------------

        self.x -= self.speed * dt / 1000

        # ------------------------------------------
        # КУЛДАУН УРОНА
        # ------------------------------------------

        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

        # ------------------------------------------
        # ВЕРХНЯЯ ЧАСТЬ СТЕНЫ
        # ------------------------------------------

        top_height = self.gap_x - self.gap_width // 2

        top_rect = pygame.Rect(
            int(self.x),
            0,
            self.width,
            max(0, top_height)
        )

        # ------------------------------------------
        # НИЖНЯЯ ЧАСТЬ СТЕНЫ
        # ------------------------------------------

        bottom_y = self.gap_x + self.gap_width // 2

        bottom_rect = pygame.Rect(
            int(self.x),
            bottom_y,
            self.width,
            max(0, 600 - bottom_y)
        )

        # ------------------------------------------
        # ПРОВЕРКА УРОНА
        # ------------------------------------------

        if self.damage_cooldown <= 0:

            player_hitbox = player.get_hitbox()

            if (
                player_hitbox.colliderect(top_rect)
                or
                player_hitbox.colliderect(bottom_rect)
            ):

                player.take_damage(1)

                self.damage_cooldown = 500

        # ------------------------------------------
        # СТЕНА УШЛА ЗА ЭКРАН
        # ------------------------------------------

        if self.x < -self.width:
            self.dead = True

    def draw(self, surface):

        # ------------------------------------------
        # ВЕРХ
        # ------------------------------------------

        top_height = self.gap_x - self.gap_width // 2

        pygame.draw.rect(
            surface,
            (255, 120, 0),
            (
                int(self.x),
                0,
                self.width,
                max(0, top_height)
            )
        )

        # ------------------------------------------
        # НИЗ
        # ------------------------------------------

        bottom_y = self.gap_x + self.gap_width // 2

        pygame.draw.rect(
            surface,
            (255, 120, 0),
            (
                int(self.x),
                bottom_y,
                self.width,
                max(0, 600 - bottom_y)
            )
        )


class AttackManager:

    def __init__(self, arena):

        self.arena = arena

        self.current_attack = None
        self.attack_timer = 0
        self.finished = False
        self.candies = []
        self.bombs = []
        self.projectiles = []

        # Фаза 1
        self.phase1_step = 0
        self.phase1_timer = 0
        # Фаза 2
        self.phase2_step = 0
        self.phase2_timer = 0
        self.ram_count = 0
        self.ram_target_x = 0
        self.ram_target_y = 0
        self.ram_sound_played = False
        self.ram_damage_done = False
        self.ram_start_x = 350
        self.ram_start_y = 50
        self.ram_dx = 0
        self.ram_dy = 0
        self.ram_wait = 0
        self.summon_count = 0
        self.summon_target_x = 0
        self.summon_target_y = 0
        self.summon_wait = 0
        self.friends = []
        self.ram_count = 0
        self.ram_target_set = False
        # ФАЗА 3 — оригинальная 4-я фаза
        self.phase3_timer = 0
        self.phase3_step = 0
        self.phase3_angle = 0
        self.phase3_bomb_timer = 0
        self.walls = []
        self.wall_timer = 0
        self.wall_count = 0
        self.phase3_timer = 0
        self.phase3_bullet_timer = 0

    def spawn_wall(self):

        gap_x = random.randint(100, 500)

        wall = ProjectileWall(
            y=0,
            gap_x=gap_x,
            speed=300
        )

        self.walls.append(wall)

    # ========================================================
    # ЗАПУСК АТАКИ
    # ========================================================

    def start_attack(self, attack_name):

        self.current_attack = attack_name

        self.attack_timer = 0
        self.finished = False

        self.phase1_step = 0
        self.phase1_timer = 0

        self.bombs.clear()
        self.projectiles.clear()

        self.phase2_step = 0
        self.phase2_timer = 0
        self.ram_count = 0

        self.phase3_timer = 0
        self.phase3_step = 0
        self.phase3_angle = 0
        self.phase3_bomb_timer = 0
        self.phase3_timer = 0
        self.phase3_bullet_timer = 0

    # ========================================================
    # UPDATE
    # ========================================================

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt, player, eram):

        # ========================================================
        # ОБНОВЛЯЕМ СТЕНЫ
        # ========================================================

        for wall in self.walls:
            wall.update(dt, player)

        self.walls = [
            wall for wall in self.walls
            if not wall.dead
        ]

        # ========================================================
        # ПЕРЕКЛЮЧЕНИЕ НА ФАЗУ 3
        # ========================================================

        if eram.hp <= 4 and self.current_attack == "phase2":
            self.current_attack = "phase3"

            self.phase3_timer = 0
            self.phase3_step = 0
            self.phase3_angle = 0
            self.phase3_bomb_timer = 0
            self.arena.set_phase3_arena()
            self.projectiles.clear()
            self.bombs.clear()

            eram.x = 350
            eram.y = 250

            eram.moving = False
            eram.set_animation(eram_fire)

            sounds["bf"].stop()

            print("🔥 ФАЗА 3 НАЧАЛАСЬ!")

        # ========================================================
        # ВЫБОР АТАКИ
        # ========================================================

        if self.current_attack == "phase1":

            self.update_phase1(
                dt,
                player,
                eram
            )

        elif self.current_attack == "bombs":

            self.update_bombs(
                dt,
                player,
                eram
            )

        elif self.current_attack == "six_bullets":

            self.update_six_bullets(
                dt,
                player,
                eram
            )

        elif self.current_attack == "phase2":

            self.update_phase2(
                dt,
                player,
                eram
            )

        elif self.current_attack == "ram":

            self.update_ram(
                dt,
                player,
                eram
            )

        elif self.current_attack == "friends":

            self.update_friends(
                dt,
                player,
                eram
            )

        elif self.current_attack == "phase3":

            self.update_phase3(
                dt,
                player,
                eram
            )

    # ========================================================
    # ФАЗА 1
    # ========================================================

    def update_phase1(self, dt, player, eram):


        self.phase1_timer += dt

        # ----------------------------------------------------
        # ОБНОВЛЯЕМ ПУЛИ
        # ----------------------------------------------------

        for projectile in self.projectiles:

            projectile.update(dt)

            if projectile.damage_cooldown <= 0:

                if projectile.get_hitbox().colliderect(
                        player.get_hitbox()
                ):

                    player.take_damage(
                        projectile.damage
                    )

                    projectile.damage_cooldown = 500

        # ----------------------------------------------------
        # ОБНОВЛЯЕМ БОМБЫ
        # ----------------------------------------------------

        for bomb in self.bombs:

            bomb.update(dt)

            if not bomb.exploded:
                continue

            if bomb.damage_cooldown > 0:
                continue

            player_hitbox = player.get_hitbox()

            for fire_hitbox in bomb.get_fire_hitboxes():

                if player_hitbox.colliderect(
                        fire_hitbox
                ):

                    player.take_damage(1)

                    bomb.damage_cooldown = 500

                    break

        # ====================================================
        # ПАТТЕРН
        # ====================================================

        # ----------------------------------------------------
        # ШАГ 0
        # Ждём 1 секунду
        # ----------------------------------------------------

        if self.phase1_step == 0:

            if self.phase1_timer >= 1000:

                self.spawn_six_bullets(eram)
                sounds["bf"].play()
                self.phase1_timer = 0
                self.phase1_step = 1

        # ----------------------------------------------------
        # ШАГ 1
        # Ещё 1 секунда → второй залп
        # ----------------------------------------------------

        elif self.phase1_step == 1:

            if self.phase1_timer >= 1000:

                self.spawn_six_bullets(eram)
                sounds["bf"].play()
                self.phase1_timer = 0
                self.phase1_step = 2

        # ----------------------------------------------------
        # ШАГ 2
        # Ещё 1 секунда → третий залп
        # ----------------------------------------------------

        elif self.phase1_step == 2:

            if self.phase1_timer >= 1000:

                self.spawn_six_bullets(eram)
                sounds["bf"].play()
                self.phase1_timer = 0
                self.phase1_step = 3

        # ----------------------------------------------------
        # ШАГ 3
        # 3 секунды → бомбы
        # ----------------------------------------------------

        elif self.phase1_step == 3:

            if self.phase1_timer >= 3000:
                eram.set_animation(eram_blyat)

                self.spawn_bombs(player)
                sounds["bt"].play()
                self.phase1_timer = 0

                self.phase1_step = 4


        # ----------------------------------------------------
        # ШАГ 4
        # Бомбы ждут свои 1.5 секунды
        # ----------------------------------------------------

        elif self.phase1_step == 4:

            if self.phase1_timer >= 1500:

                eram.set_animation(eram_static)
                sounds["bf"].play(-1)
                self.phase1_timer = 0

                self.phase1_step = 5

        # ----------------------------------------------------
        # ШАГ 5
        # Ещё 2 секунды → новый цикл
        # ----------------------------------------------------

        elif self.phase1_step == 5:

            if self.phase1_timer >= 2000:

                self.phase1_timer = 0
                self.phase1_step = 0
                sounds["bf"].stop()
                # Старые бомбы убираем
                self.bombs.clear()

    # ========================================================
    # ШЕСТЬ ПУЛЬ
    # ========================================================

    def spawn_six_bullets(self, eram):

        for i in range(6):

            angle = math.radians(i * 60)

            projectile = Projectile(
                eram.x + 50,
                eram.y + 50,
                angle,
                speed=4,
                damage=1
            )

            self.projectiles.append(
                projectile
            )

    # ========================================================
    # БОМБЫ
    # ========================================================

    def spawn_bombs(self, player):

        walkable_tiles = []

        for y, row in enumerate(
                self.arena.arena
        ):

            for x, tile in enumerate(row):

                if tile == 1:

                    walkable_tiles.append(
                        (x, y)
                    )

        random.shuffle(
            walkable_tiles
        )

        for tile_x, tile_y in walkable_tiles:

            x = (
                tile_x + 0.5
            ) * (
                800 / len(
                    self.arena.arena[0]
                )
            )

            y = (
                tile_y + 0.5
            ) * (
                600 / len(
                    self.arena.arena
                )
            )

            distance = math.hypot(
                x - player.x,
                y - player.y
            )

            if distance < 100:
                continue

            self.bombs.append(
                Bomb(x, y)
            )

            if len(self.bombs) >= 3:
                break

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):

        # ПУЛИ

        for projectile in self.projectiles:

            projectile.draw(
                surface
            )

        # БОМБЫ

        for bomb in self.bombs:

            bomb.draw(
                surface
            )

        # ДРУЗЬЯ)

        for friend in self.friends:
            friend.draw(surface)

        # конфетки от взрослого дяденьки... его зовут Эпштейн...

        for candy in self.candies:
            candy.draw(surface)

        # ИНФЕРНАЛЬНО, АДСКИ САТАНИНСКАЯ СТЕНА
        for wall in self.walls:
            wall.draw(surface)

    def update_ram_attack(self, dt, player, eram):

        self.ram_timer += dt

        # ==========================================
        # 0 — возвращаем Eram в стартовую точку
        # ==========================================

        if self.ram_step == 0:

            target_x = 350
            target_y = 50

            dx = target_x - eram.x
            dy = target_y - eram.y

            distance = math.hypot(dx, dy)

            if distance > 5:
                eram.set_animation(eram_fly)

                eram.x += dx / distance * 5
                eram.y += dy / distance * 5

                return

            eram.x = target_x
            eram.y = target_y

            # Запоминаем позицию игрока
            dx = player.x - eram.x
            dy = player.y - eram.y

            distance = math.hypot(dx, dy)

            if distance > 0:
                self.ram_dx = dx / distance
                self.ram_dy = dy / distance

            self.ram_damage_done = False
            self.ram_timer = 0
            self.ram_step = 1

            return

        # ==========================================
        # 1 — небольшое прицеливание
        # ==========================================

        if self.ram_step == 1:

            eram.set_animation(eram_fire)

            if self.ram_timer >= 400:
                self.ram_timer = 0
                self.ram_step = 2

            return

        # ==========================================
        # 2 — ТАРАН
        # ==========================================

        if self.ram_step == 2:

            eram.set_animation(eram_fire)

            eram.x += self.ram_dx * 9
            eram.y += self.ram_dy * 9

            if not self.ram_damage_done:

                if eram.get_hitbox().colliderect(
                        player.get_hitbox()
                ):
                    player.take_damage(1)

                    self.ram_damage_done = True

            # Вылетел за пределы
            if (
                    eram.x < -150
                    or eram.x > 950
                    or eram.y < -150
                    or eram.y > 750
            ):

                self.ram_count += 1

                eram.x = 350
                eram.y = 50

                self.ram_timer = 0
                self.ram_step = 0

                if self.ram_count >= 3:
                    self.ram_count = 0
                    return True

        return False

    def update_phase2(self, dt, player, eram):
        self.phase2_timer += dt
        self.ram_wait -= dt
        for friend in self.friends:
            friend.update(dt, player)

        alive_friends = []

        for friend in self.friends:

            if friend.dead:
                sounds["mfr"].play()
                if friend.should_drop_candy():
                    self.candies.append(
                        Candy(
                            friend.x + 32,
                            friend.y + 32
                        )
                    )

            else:

                alive_friends.append(friend)

        self.friends = alive_friends

        for candy in self.candies:

            if candy.get_hitbox().colliderect(
                    player.get_hitbox()
            ):
                player.hp = min(player.hp + 1, 6)
                sounds["h"].play()
                self.candies.remove(candy)

                break

        # ==========================================
        # ШАГ 0 — НАСМЕШКА
        # ==========================================

        if self.phase2_step == 0:
            eram.moving = False
            sounds["bf"].stop()
            # Запускаем насмешку только один раз
            if self.phase2_timer == dt:
                eram.set_animation(eram_laugh)
                sounds["el"].play()

            # Ждём окончания насмешки
            if self.phase2_timer >= 1500:
                self.phase2_timer = 0
                self.phase2_step = 1

                eram.set_animation(eram_static)

        # ==========================================
        # ШАГ 1 — ЕРАМ ЛЕТИТ НАВЕРХ
        # ==========================================

        elif self.phase2_step == 1:

            target_x = 350

            target_y = 50

            dx = target_x - eram.x

            dy = target_y - eram.y

            distance = math.hypot(dx, dy)

            if distance <= 10:

                eram.x = target_x

                eram.y = target_y

                # СРАЗУ запоминаем позицию игрока

                self.ram_target_x = player.x

                self.ram_target_y = player.y

                dx = self.ram_target_x - eram.x

                dy = self.ram_target_y - eram.y

                distance = math.hypot(dx, dy)

                if distance > 0:
                    self.ram_dx = dx / distance

                    self.ram_dy = dy / distance

                self.ram_damage_done = False

                self.ram_sound_played = False

                self.phase2_step = 2


            else:

                speed = 5

                eram.x += dx / distance * speed

                eram.y += dy / distance * speed

        # ==========================================
        # ШАГ 2 — ЕРАМ ТАРАНИТ 1 РАЗ
        # ==========================================

        elif self.phase2_step == 2:

            if eram.animation != eram_fire:
                eram.set_animation(eram_fire)

            if not self.ram_sound_played:
                sounds["msd"].play()

                self.ram_sound_played = True

            print("RAM START", self.ram_dx, self.ram_dy)

            RAM_SPEED = 4

            eram.x += self.ram_dx * RAM_SPEED
            eram.y += self.ram_dy * RAM_SPEED

            if not self.ram_sound_played:
                sounds["msd"].play()

                self.ram_sound_played = True

            eram.x += self.ram_dx * RAM_SPEED
            eram.y += self.ram_dy * RAM_SPEED

            if not self.ram_damage_done:

                if eram.get_hitbox().colliderect(

                        player.get_hitbox()

                ):
                    player.take_damage(1)

                    self.ram_damage_done = True

            if (

                    eram.x < -120

                    or eram.x > 920

                    or eram.y < -120

                    or eram.y > 720

            ):

                eram.x = 350

                eram.y = 50

                self.ram_count += 1

                self.ram_target_set = False

                self.ram_damage_done = False

                self.ram_sound_played = False

                if self.ram_count >= 3:

                    self.phase2_step = 5

                    self.summon_count = 0

                    self.summon_wait = 0


                else:

                    self.ram_target_x = player.x

                    self.ram_target_y = player.y

                    dx = self.ram_target_x - eram.x

                    dy = self.ram_target_y - eram.y

                    distance = math.hypot(dx, dy)

                    if distance > 0:
                        self.ram_dx = dx / distance

                        self.ram_dy = dy / distance

                    self.phase2_step = 2
                self.ram_wait -= dt

        # ==========================================
        # ШАГ 3 — ЕРАМ ТАРАНИТ 2 РАЗ
        # ==========================================

        elif self.phase2_step == 3:
            self.ram_wait -= dt
            if self.ram_wait > 0:

                eram.set_animation(eram_static)
                return
            if not self.ram_target_set:

                self.ram_target_x = player.x
                self.ram_target_y = player.y
                dx = self.ram_target_x - eram.x
                dy = self.ram_target_y - eram.y
                distance = math.hypot(dx, dy)
                if distance > 0:

                    self.ram_dx = dx / distance
                    self.ram_dy = dy / distance
                self.ram_target_set = True
            if self.ram_count >= 3:

                self.phase2_step = 5
                self.summon_count = 0
                self.summon_wait = 0
                self.phase2_timer = 0
                return

            # дальше твой существующий код тарана

            if not self.ram_sound_played:
                sounds["msd"].play()

                self.ram_sound_played = True

            speed = 8

            eram.x += self.ram_dx * speed

            eram.y += self.ram_dy * speed

            if not self.ram_damage_done:

                if eram.get_hitbox().colliderect(

                        player.get_hitbox()

                ):
                    player.take_damage(1)

                    self.ram_damage_done = True

            if (
                    eram.x < -120 or
                    eram.x > 920 or
                    eram.y < -120 or
                    eram.y > 720
            ):

                self.ram_count += 1

                eram.x = self.ram_start_x
                eram.y = self.ram_start_y

                self.phase2_timer = 0
                self.ram_sound_played = False
                self.ram_damage_done = False

                if self.ram_count >= 3:

                    self.phase2_step = 5

                    self.summon_count = 0
                    self.summon_wait = 0

                else:

                    # Следующий таран
                    self.ram_wait -= 500
                    self.phase2_step = 3



        elif self.phase2_step == 5:

            eram.set_animation(eram_fly)

            if self.summon_count >= 5:
                self.phase2_step = 7

                self.phase2_timer = 0

                return

            if self.summon_wait == 0:

                valid_positions = []

                tile_width = 800 / len(self.arena.arena[0])

                tile_height = 600 / len(self.arena.arena)

                for y, row in enumerate(self.arena.arena):

                    for x, tile in enumerate(row):

                        if tile != 1:
                            continue

                        target_x = (x + 0.5) * tile_width - 32

                        target_y = (y + 0.5) * tile_height - 32

                        test_rect = pygame.Rect(

                            int(target_x),

                            int(target_y),

                            64,

                            64

                        )

                        if not self.arena.is_blocked_rect(test_rect):
                            valid_positions.append(

                                (target_x, target_y)

                            )

                if valid_positions:
                    self.summon_target_x, self.summon_target_y = random.choice(

                        valid_positions

                    )

                    self.summon_wait = 1

            # ДВИЖЕНИЕ ИМЕННО К ТОЧКЕ ПРИЗЫВА

            dx = self.summon_target_x - eram.x

            dy = self.summon_target_y - eram.y

            distance = math.hypot(dx, dy)

            if distance > 5:

                speed = 300

                eram.x += dx / distance * speed * dt / 1000

                eram.y += dy / distance * speed * dt / 1000


            else:

                eram.x = self.summon_target_x

                eram.y = self.summon_target_y

                self.phase2_timer = 0

                self.phase2_step = 6




        elif self.phase2_step == 6:

            if self.phase2_timer >= 500:
                self.friends.append(
                    Friend(
                        eram.x,
                        eram.y,
                        self.arena
                    )
                )
                self.summon_count += 1
                self.summon_wait = 0
                sounds["fa"].play()
                self.phase2_timer = 0
                self.phase2_step = 5


        elif self.phase2_step == 7:

            target_x = 700
            target_y = 50

            dx = target_x - eram.x
            dy = target_y - eram.y

            distance = math.hypot(dx, dy)

            if distance > 5:

                speed = 5

                eram.x += dx / distance * speed
                eram.y += dy / distance * speed

            else:

                eram.x = target_x
                eram.y = target_y

                eram.set_animation(eram_laugh)
                sounds["el"].play(-1)

                self.phase2_step = 8




        elif self.phase2_step == 8:

            if self.phase2_timer >= 9000:
                self.phase2_timer = 0
                sounds["el"].stop()
                self.ram_count = 0
                self.summon_count = 0
                self.summon_wait = 0
                self.ram_sound_played = False
                self.ram_damage_done = False
                self.ram_target_set = False
                eram.set_animation(eram_static)
                self.phase2_step = 9


        elif self.phase2_step == 9:
            eram.moving = True
            self.phase2_timer = 0
            self.phase2_step = 10
        # ----------------------------------------------------
        # ОБНОВЛЯЕМ ПУЛИ
        # ----------------------------------------------------

        for projectile in self.projectiles:

            projectile.update(dt)

            if projectile.damage_cooldown <= 0:

                if projectile.get_hitbox().colliderect(
                        player.get_hitbox()
                ):
                    player.take_damage(
                        projectile.damage
                    )

                    projectile.damage_cooldown = 500

        # ----------------------------------------------------
        # ОБНОВЛЯЕМ БОМБЫ
        # ----------------------------------------------------

        for bomb in self.bombs:

            bomb.update(dt)

            if not bomb.exploded:
                continue

            if bomb.damage_cooldown > 0:
                continue

            player_hitbox = player.get_hitbox()

            for fire_hitbox in bomb.get_fire_hitboxes():

                if player_hitbox.colliderect(
                        fire_hitbox
                ):
                    player.take_damage(1)

                    bomb.damage_cooldown = 500

                    break

        # ====================================================
        # ПАТТЕРН
        # ====================================================

        # ----------------------------------------------------
        # ШАГ 0
        # Ждём 1 секунду
        # ----------------------------------------------------

        if self.phase2_step == 10:
            if self.phase2_timer >= 1000:
                self.spawn_six_bullets(eram)
                sounds["bf"].play()
                self.phase2_timer = 0
                self.phase2_step = 11


        # ----------------------------------------------------
        # ШАГ 1
        # Ещё 1 секунда → второй залп
        # ----------------------------------------------------

        elif self.phase2_step == 11:
            if self.phase2_timer >= 1000:
                self.spawn_six_bullets(eram)
                sounds["bf"].play()
                self.phase2_timer = 0
                self.phase2_step = 12

        # ----------------------------------------------------
        # ШАГ 2
        # Ещё 1 секунда → третий залп
        # ----------------------------------------------------

        elif self.phase2_step == 12:
            if self.phase2_timer >= 1000:
                self.spawn_six_bullets(eram)
                sounds["bf"].play()
                self.phase2_timer = 0
                self.phase2_step = 13

        # ----------------------------------------------------
        # ШАГ 3
        # 3 секунды → бомбы
        # ----------------------------------------------------

        elif self.phase2_step == 13:
            if self.phase2_timer >= 3000:
                eram.set_animation(eram_blyat)
                self.spawn_bombs(player)
                sounds["bt"].play()
                self.phase2_timer = 0
                self.phase2_step = 14

        # ----------------------------------------------------
        # ШАГ 4
        # Бомбы ждут свои 1.5 секунды
        # ----------------------------------------------------

        elif self.phase2_step == 14:
            if self.phase2_timer >= 1500:
                eram.set_animation(eram_static)
                sounds["bf"].play(-1)
                self.phase2_timer = 0
                self.phase2_step = 15

        # ----------------------------------------------------
        # ШАГ 5
        # Ещё 2 секунды → новый цикл
        # ----------------------------------------------------

        elif self.phase2_step == 15:
            if self.phase2_timer >= 2000:
                sounds["bf"].stop()
                self.bombs.clear()
                self.phase2_timer = 0
                eram.moving = False
                # Снова тараны
                self.ram_count = 0
                self.ram_target_set = False
                self.ram_sound_played = False
                self.ram_damage_done = False
                self.phase2_step = 1

        # ========================================================
        # ШЕСТЬ ПУЛЬ
        # ========================================================

    def spawn_six_bullets(self, eram):

        for i in range(6):
            angle = math.radians(i * 60)

            projectile = Projectile(
                eram.x + 50,
                eram.y + 50,
                angle,
                speed=4,
                damage=1
            )

            self.projectiles.append(
                projectile
            )

        # ========================================================
        # БОМБЫ
        # ========================================================

    def spawn_bombs(self, player):

        walkable_tiles = []

        for y, row in enumerate(
                self.arena.arena
        ):

            for x, tile in enumerate(row):

                if tile == 1:
                    walkable_tiles.append(
                        (x, y)
                    )

        random.shuffle(
            walkable_tiles
        )

        for tile_x, tile_y in walkable_tiles:

            x = (
                        tile_x + 0.5
                ) * (
                        800 / len(
                    self.arena.arena[0]
                )
                )

            y = (
                        tile_y + 0.5
                ) * (
                        600 / len(
                    self.arena.arena
                )
                )

            distance = math.hypot(
                x - player.x,
                y - player.y
            )

            if distance < 100:
                continue

            self.bombs.append(
                Bomb(x, y)
            )

            if len(self.bombs) >= 3:
                break

    def update_phase3(self, dt, player, eram):

        self.phase3_timer += dt
        self.phase3_bullet_timer += dt

        # ========================================================
        # ОБНОВЛЯЕМ СНАРЯДЫ
        # ========================================================

        for projectile in self.projectiles:

            projectile.update(dt)

            if projectile.damage_cooldown <= 0:

                if projectile.get_hitbox().colliderect(
                        player.get_hitbox()
                ):
                    player.take_damage(
                        projectile.damage
                    )

                    projectile.damage_cooldown = 500

        # ========================================================
        # УДАЛЯЕМ УШЕДШИЕ СНАРЯДЫ
        # ========================================================

        self.projectiles = [
            projectile
            for projectile in self.projectiles
            if not getattr(projectile, "dead", False)
        ]

        # ========================================================
        # ОБНОВЛЯЕМ БОМБЫ
        # ========================================================

        for bomb in self.bombs:

            bomb.update(dt)

            if not bomb.exploded:
                continue

            if bomb.damage_cooldown > 0:
                continue

            for fire_hitbox in bomb.get_fire_hitboxes():

                if player.get_hitbox().colliderect(
                        fire_hitbox
                ):
                    player.take_damage(1)

                    bomb.damage_cooldown = 500

                    break

        self.bombs = [
            bomb for bomb in self.bombs
            if not bomb.dead
        ]

        # ========================================================
        # ШАГ 0
        # ТРИ ВРАЩАЮЩИХСЯ НАПРАВЛЕНИЯ
        # ========================================================

        if self.phase3_step == 0:

            # Общий таймер атаки — НЕ СБРАСЫВАЕМ
            # Он должен дойти до 10 секунд.

            # Отдельный таймер спавна пуль
            if self.phase3_bullet_timer >= 120:
                eram.set_animation(eram_static)
                self.phase3_bullet_timer = 0

                center_x = eram.x + 50
                center_y = eram.y + 50

                for i in range(3):
                    angle = (
                            self.phase3_angle
                            + math.radians(i * 120)
                    )

                    spawn_distance = 35

                    spawn_x = (
                            center_x
                            + math.cos(angle) * spawn_distance
                    )

                    spawn_y = (
                            center_y
                            + math.sin(angle) * spawn_distance
                    )

                    projectile = Projectile(
                        spawn_x,
                        spawn_y,
                        angle,
                        speed=3.5,
                        damage=1
                    )

                    self.projectiles.append(projectile)

            # Вращение
            self.phase3_angle -= 0.035

            # ЧЕРЕЗ 10 СЕКУНД ПЕРЕХОДИМ К ТАРАНАМ
            if self.phase3_timer >= 10000:
                self.phase3_timer = 0
                self.phase3_bullet_timer = 0

                self.projectiles.clear()

                self.ram_target_set = False
                self.ram_sound_played = False
                self.ram_damage_done = False

                self.phase3_step = 1

                eram.set_animation(eram_fly)


        # ========================================================
        # ШАГ 1
        # ЕРАМ ЛЕТИТ НА ПОЗИЦИЮ ДЛЯ ТАРАНА
        # ========================================================

        elif self.phase3_step == 1:

            target_x = 350
            target_y = 50

            dx = target_x - eram.x
            dy = target_y - eram.y

            distance = math.hypot(dx, dy)

            if distance > 5:

                speed = 5

                eram.x += dx / distance * speed
                eram.y += dy / distance * speed

            else:

                eram.x = target_x
                eram.y = target_y

                # Сбрасываем состояние тарана
                self.ram_target_set = False
                self.ram_sound_played = False
                self.ram_damage_done = False

                self.phase3_step = 2

        # ========================================================
        # ШАГ 2
        # БЕСКОНЕЧНЫЕ ТАРАНЫ
        # ========================================================

        elif self.phase3_step == 2:

            # ----------------------------------------------------
            # ВЫБИРАЕМ ЦЕЛЬ
            # ----------------------------------------------------

            if not self.ram_target_set:

                self.ram_target_x = player.x
                self.ram_target_y = player.y

                dx = (
                        self.ram_target_x
                        - eram.x
                )

                dy = (
                        self.ram_target_y
                        - eram.y
                )

                distance = math.hypot(
                    dx,
                    dy
                )

                if distance > 0:
                    self.ram_dx = (
                            dx / distance
                    )

                    self.ram_dy = (
                            dy / distance
                    )

                self.ram_target_set = True

            # ----------------------------------------------------
            # ЗВУК
            # ----------------------------------------------------

            if not self.ram_sound_played:
                sounds["msd"].play()
                eram.set_animation(eram_fire)
                self.ram_sound_played = True

            # ----------------------------------------------------
            # ТАРАН
            # ----------------------------------------------------

            RAM_SPEED = 8

            eram.x += (
                    self.ram_dx
                    * RAM_SPEED
            )

            eram.y += (
                    self.ram_dy
                    * RAM_SPEED
            )

            # ----------------------------------------------------
            # УРОН
            # ----------------------------------------------------

            if not self.ram_damage_done:

                if eram.get_hitbox().colliderect(
                        player.get_hitbox()
                ):
                    player.take_damage(1)

                    self.ram_damage_done = True

            # ----------------------------------------------------
            # ЕРАМ ВЫЛЕТЕЛ ЗА АРЕНУ
            # ----------------------------------------------------

            if (
                    eram.x < -120
                    or eram.x > 920
                    or eram.y < -120
                    or eram.y > 720
            ):
                # Возвращаем его наверх

                eram.x = 350
                eram.y = 50

                # Следующий таран снова целится в игрока

                self.ram_target_set = False
                self.ram_sound_played = False
                self.ram_damage_done = False
