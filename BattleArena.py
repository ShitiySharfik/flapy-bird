import pygame


TILE_SIZE = 16

# Типы клеток
WALKABLE = 1
SOLID = 2
INTERFACE = 3
WALKABLE3 = 4
SOLID3 = 5
class BattleArena:

    def __init__(self):
        self.arena_phase1 = [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2],
            [2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2],
            [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],

        ]
        self.arena_phase3 = [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
            [5, 4, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5],
            [5, 4, 5, 4, 4, 4, 4, 5, 4, 4, 4, 5],
            [5, 4, 4, 4, 5, 4, 4, 4, 4, 5, 4, 5],
            [5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 4, 5],
            [5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        ]


        self.arena = self.arena_phase1

        # Кирпич
        self.brick_images = {
            1: pygame.image.load(
                "assets/Sprites/ФОН/Кирпич_можно1.png"
            ).convert(),

            2: pygame.image.load(
                "assets/Sprites/ФОН/Кирпич_нельзя1.png"
            ).convert(),

            3: pygame.image.load(
                "assets/Sprites/ФОН/Кирпич_пустота.png"
            ).convert(),

            4: pygame.image.load(
                "assets/Sprites/ФОН/Кирпич_можно2.png"
            ).convert(),

            5: pygame.image.load(
                "assets/Sprites/ФОН/Кирпич_нельзя2.png"
            ).convert()
        }

        for tile_type in self.brick_images:
            self.brick_images[tile_type] = pygame.transform.scale(
                self.brick_images[tile_type],
                (TILE_SIZE, TILE_SIZE)
            )

    def is_blocked(self, x, y):

        tile_width = 800 / len(self.arena[0])
        tile_height = 600 / len(self.arena)

        tile_x = int(x // tile_width)
        tile_y = int(y // tile_height)

        if tile_x < 0 or tile_x >= len(self.arena[0]):
            return True

        if tile_y < 0 or tile_y >= len(self.arena):
            return True

        tile = self.arena[tile_y][tile_x]

        if tile == SOLID or tile == INTERFACE or tile == SOLID3:
            return True

        return False

    def is_blocked_rect(self, rect):

        tile_width = 800 / len(self.arena[0])
        tile_height = 600 / len(self.arena)

        # Клетки, которых касается прямоугольник
        left = int(rect.left // tile_width)
        right = int((rect.right - 1) // tile_width)

        top = int(rect.top // tile_height)
        bottom = int((rect.bottom - 1) // tile_height)

        # Проверяем все затронутые клетки
        for tile_y in range(top, bottom + 1):

            for tile_x in range(left, right + 1):

                # За пределами арены
                if tile_x < 0 or tile_x >= len(self.arena[0]):
                    return True

                if tile_y < 0 or tile_y >= len(self.arena):
                    return True

                tile = self.arena[tile_y][tile_x]

                if tile == SOLID or tile == INTERFACE:
                    return True

        return False

    def draw(self, surface):

        # Создаём маленькую поверхность арены
        arena_surface = pygame.Surface((192, 144))

        for row, line in enumerate(self.arena):

            for column, tile in enumerate(line):

                x = column * TILE_SIZE
                y = row * TILE_SIZE

                if tile in self.brick_images:
                    arena_surface.blit(
                        self.brick_images[tile],
                        (x, y)
                    )

        # Растягиваем арену на весь виртуальный экран
        arena_surface = pygame.transform.scale(
            arena_surface,
            (800, 600)
        )

        surface.blit(arena_surface, (0, 0))

    def set_phase3_arena(self):
        self.arena = self.arena_phase3


