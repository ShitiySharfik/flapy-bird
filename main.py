import pygame
from random import randint
pygame.init()

from Sounds import sounds
from BattleArena import BattleArena
from HERO_SWORD import Player
from MANTLE_HOLDER import Eram, eram_laugh, eram_static, eram_fire, eram_fly, eram_blyat, Projectile
from Dialogue import Dialogue
import math

pygame.init()
from Attacks import AttackManager
pygame.mouse.set_visible(False)

sounds["mm"].play(-1)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("MANTLE")

# Виртуальный экран игры
game_screen = pygame.Surface((800, 600))
arena = BattleArena()
attack_manager = AttackManager(arena)
player = Player(80, 50)
filter_surface = pygame.Surface((800, 600), pygame.SRCALPHA)

for y in range(0, 600, 4):
    pygame.draw.line(
        filter_surface,
        (0, 0, 0, 35),
        (0, y),
        (800, y)
    )
def apply_filter():
    game_screen.blit(filter_surface, (0, 0))

fullscreen = False

clock = pygame.time.Clock()
menu_image = pygame.image.load(
    "assets/Sprites/ФОН/МЕНЮ.png"
).convert()

menu_image = pygame.transform.scale(menu_image, (800, 600))

friend = pygame.image.load(
    "assets/Sprites/OTHERS/FRIEND_overworld_8bit_eyes.png"

).convert()
friend = pygame.transform.scale(friend, (800, 600))
buttons = [
    "НАЧАТЬ",
    "НАСТРОЙКИ",
    "ВЫЙТИ",
    "ПОЛ.ЭКРАН"
]
swing_sounds = [
    sounds["s1"],
    sounds["s2"],
    sounds["s3"]
]

eram_dialogue = Dialogue([
    ("Ерам", "Приветствую вас!"),
    ("Ерам", "..."),
    ("Ерам", "А ты, я вижу, даже не старался."),
    ("Ерам", "Да-да-да. Я сейчас про тебя, АРТЁМ."),
    ("Ерам", "Ты понимаешь, насколько это тупо?"),
    ("Ерам", "Делать битву со МНОЙ!"),
    ("Ерам", "Добавлять все эти реплики..."),
    ("Ерам", "А для чего?"),
    ("Ерам", "Чтобы люди только и смогли поржать над тобою?"),
    ("Ерам", "САМИ ГЛАЗА РАЗУЙТЕ!"),
    ("Ерам", "Ему ещё и ИИ помогал вместо того, чтоб думать своей башкой..."),
    ("Ерам", "Он сделал бесполезные счётчики"),
    ("Ерам", "А вместо целой игры..."),
    ("Ерам", "ОН СДЕЛАЛ ЛИШЬ БОССФАЙТ СО МНОЙ!"),
    ("Ерам", "..."),
    ("Ерам", "Зачем тебе это?"),
    ("Ерам", "Ты настолько хочешь ещё раз со мной подраться?"),
    ("Ерам", "Ну тогда давай..."),
    ("Ерам", "ДЕРИСЬ!"),
])

button_positions = [
    (150, 400),
    (500, 400),
    (150, 500),
    (500, 500)
]

selected_x = 0
selected_y = 0

fullscreen = False

running = True

while running:
    dt = clock.tick(60)

    def start_game():
        sounds["mm"].stop()

        game_screen.fill((0, 0, 0))
        show_game_screen()
        pygame.time.delay(1000)
        sounds["ed"].play(-1)
        player = Player(370, 450)
        player.direction = "up"
        eram = Eram(370, 250)
        projectiles = []
        attack_manager = AttackManager(arena)
        attack_manager.start_attack("phase1")
        def spawn_projectiles():

            for i in range(6):
                angle = math.radians(i * 60)

                projectiles.append(
                    Projectile(
                        eram.x + 50,
                        eram.y + 50,
                        angle
                    )
                )

        dialogue = Dialogue([
            ("Ерам", "Приветствую вас!"),
            ("Ерам", "..."),
            ("Ерам", "А ты, я вижу, даже не старался."),
            ("Ерам", "Да-да-да. Я сейчас про тебя, АРТЁМ."),
            ("Ерам", "Ты понимаешь, насколько это тупо?"),
            ("Ерам", "Делать битву со МНОЙ!"),
            ("Ерам", "Добавлять все эти реплики..."),
            ("Ерам", "А для чего?"),
            ("Ерам", "Чтобы люди только и смогли..."),
            ("Ерам", "поржать над тобою..."),
            ("Ерам", "САМИ ГЛАЗА РАЗУЙТЕ!"),
            ("Ерам", "Ему ещё и ИИ помогал..."),
            ("Ерам","вместо того, чтоб думать своей башкой..."),
            ("Ерам", "Он сделал бесполезные счётчики."),
            ("Ерам", "А вместо целой игры..."),
            ("Ерам", "ОН СДЕЛАЛ ЛИШЬ БОССФАЙТ СО МНОЙ!"),
            ("Ерам", "..."),
            ("Ерам", "Зачем тебе это?"),
            ("Ерам", "Ты настолько хочешь со мной подраться?"),
            ("Ерам", "Ну тогда давай..."),
            ("Ерам", "ДЕРИСЬ!")
        ])

        game_state = "dialogue"
        current_phase = 1
        taunt_timer = 0
        taunt_started = False
        game_running = True

        while game_running:

            dt = clock.get_time()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if game_state == "dialogue":

                    dialogue.handle_event(event)

                    if dialogue.finished:
                        game_state = "taunt"
                        taunt_timer = 0

                        eram.set_animation(eram_laugh)
                        sounds["el"].play()

                elif game_state == "battle":

                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:
                            game_running = False

                        if event.key == pygame.K_z:
                            player.attack()
                            swing_sounds[
                                randint(0, len(swing_sounds) - 1)
                            ].play()

            if game_state == "taunt":

                taunt_timer += dt

                if taunt_timer >= 2000:
                    game_state = "battle"

                    sounds["el"].stop()
                    sounds["ed"].stop()
                    sounds["eb"].play(-1)
                    eram.set_animation(eram_static)
            game_screen.fill((0, 0, 0))

            arena.draw(game_screen)

            if game_state == "battle":

                player.update(arena)

                if current_phase == 1:
                    eram.moving = True

                if current_phase == 1 and eram.hp <= 22:
                    current_phase = 2

                    attack_manager.start_attack("phase2")

                    eram.moving = False
                    eram.set_animation(eram_fly)

                    print("🔥 ФАЗА 2 НАЧАЛАСЬ!")

                for projectile in projectiles:

                    projectile.update(dt)

                    if projectile.get_hitbox().colliderect(
                            player.get_hitbox()
                    ):
                        player.take_damage(projectile.damage)
                        projectile.damage_cooldown = 500

                attack_hitbox = player.get_attack_hitbox()

                if attack_hitbox and not player.attack_hit:
                    if attack_hitbox.colliderect(eram.get_hitbox()):
                        eram.take_damage(0.5)
                        player.attack_hit = True

                    for friend in attack_manager.friends:

                        if (
                                attack_hitbox
                                and attack_hitbox.colliderect(
                            friend.get_hitbox()
                        )
                        ):
                            friend.take_damage()
                            player.attack_hit = True

                            break

                if eram.hp <= 0:
                    pygame.quit()
                    raise SystemExit

            eram.update(dt)

            if game_state == "battle":
                attack_manager.update(
                    dt,
                    player,
                    eram
                )

            player.draw(game_screen)
            draw_player_hp(game_screen, player)

            eram.draw(game_screen)

            attack_manager.draw(
                game_screen
            )

            for projectile in projectiles:
                projectile.draw(game_screen)

            if game_state == "dialogue":
                dialogue.draw(game_screen)

            apply_filter()

            # масштабирование game_screen
            scale = min(
                screen.get_width() / 800,
                screen.get_height() / 600
            )

            new_width = int(800 * scale)
            new_height = int(600 * scale)

            scaled = pygame.transform.scale(
                game_screen,
                (new_width, new_height)
            )

            x = (screen.get_width() - new_width) // 2
            y = (screen.get_height() - new_height) // 2

            screen.fill((0, 0, 0))
            screen.blit(scaled, (x, y))

            pygame.display.flip()
            dt = clock.tick(60)


    def draw_player_hp(surface, player):

        font = pygame.font.Font(
            "assets/Fonts/determinationmonorusbylyajk.otf",
            40
        )

        text = font.render(
            f"HP: {player.hp}/{player.max_hp}",
            True,
            (255, 255, 255)
        )

        surface.blit(text, (15, 15))

        textlvl = font.render(
            "LVL: MAX",
            True,
            (255, 255, 255)
        )

        surface.blit(textlvl, (625, 15))

        textur = font.render(
            "DAMAGE: MAX",
            True,
            (255, 255, 255)
        )

        surface.blit(textur, (280, 15))
    def show_game_screen():
        apply_filter()

        scale = min(
            screen.get_width() / 800,
            screen.get_height() / 600
        )

        new_width = int(800 * scale)
        new_height = int(600 * scale)

        scaled = pygame.transform.scale(
            game_screen,
            (new_width, new_height)
        )

        x = (screen.get_width() - new_width) // 2
        y = (screen.get_height() - new_height) // 2

        screen.fill((0, 0, 0))
        screen.blit(scaled, (x, y))

        pygame.display.flip()


    def fake_settings():
        sounds["mm"].stop()

        game_screen.fill((0, 0, 0))
        show_game_screen()

        pygame.time.delay(1000)

        sounds["mf"].play()

        game_screen.fill((0, 0, 0))
        apply_filter()
        game_screen.blit(DOLL, (100, 300))
        show_game_screen()

        pygame.time.delay(30000)
        sounds["mfr"].play()
        game_screen.fill((0, 0, 0))
        apply_filter()
        game_screen.blit(friend, (0, 0))
        show_game_screen()

        pygame.time.delay(800)

        pygame.quit()
        raise SystemExit


    # Текущая выбранная кнопка
    selected = selected_y * 2 + selected_x

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_RIGHT:
                sounds["m"].play()
                selected_x = 1

            if event.key == pygame.K_LEFT:
                sounds["m"].play()
                selected_x = 0

            if event.key == pygame.K_DOWN:
                sounds["m"].play()
                selected_y = 1

            if event.key == pygame.K_UP:
                sounds["m"].play()
                selected_y = 0

            if event.key == pygame.K_z:

                sounds["s"].play()
                #НАЧАТЬ
                if selected == 0:
                    start_game()

                # НАСТРОЙКИ
                if selected == 1:
                    fake_settings()

                # ВЫЙТИ
                if selected == 2:
                    running = False

                # ПОЛ.ЭКРАН
                if selected == 3:

                    fullscreen = not fullscreen

                    if fullscreen:
                        screen = pygame.display.set_mode(
                            (0, 0),
                            pygame.FULLSCREEN
                        )
                    else:
                        screen = pygame.display.set_mode(
                            (800, 600)
                        )

    game_screen.blit(menu_image, (0, 0))

    font = pygame.font.Font(
        "assets/Fonts/determinationmonorusbylyajk.otf",
        40
    )
    DOLL = font.render("ТВОИ ДЕЙСТВИЯ НИЧЕГО НЕ РЕШАЮТ", True, (255, 255, 255))

    for i, position in enumerate(button_positions):

        color = (255, 255, 255)

        if i == selected:
            color = (255, 255, 0)

        text = font.render(
            buttons[i],
            True,
            color
        )

        game_screen.blit(text, position)
    apply_filter()

    # Масштабируем виртуальный экран 800x600
    scale = min(
        screen.get_width() / 800,
        screen.get_height() / 600
    )

    new_width = int(800 * scale)
    new_height = int(600 * scale)

    scaled = pygame.transform.scale(
        game_screen,
        (new_width, new_height)
    )

    x = (screen.get_width() - new_width) // 2
    y = (screen.get_height() - new_height) // 2

    screen.fill((0, 0, 0))
    screen.blit(scaled, (x, y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

