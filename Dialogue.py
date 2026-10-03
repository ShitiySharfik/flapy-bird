import pygame


class Dialogue:

    def __init__(self, lines):
        self.lines = lines
        self.current_line = 0
        self.finished = False

        self.font = pygame.font.Font(
            "assets/Fonts/determinationmonorusbylyajk.otf",
            32
        )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_z:

                self.current_line += 1

                if self.current_line >= len(self.lines):
                    self.finished = True

    def draw(self, surface):

        if self.finished:
            return

        # Затемнение
        overlay = pygame.Surface(
            (800, 600),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 100))

        surface.blit(
            overlay,
            (0, 0)
        )

        # Окно диалога
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (50, 430, 700, 120)
        )

        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (50, 430, 700, 120),
            3
        )

        speaker, text = self.lines[self.current_line]

        # Имя
        name = self.font.render(
            speaker,
            True,
            (255, 255, 0)
        )

        surface.blit(
            name,
            (70, 445)
        )

        # Текст
        message = self.font.render(
            text,
            True,
            (255, 255, 255)
        )

        surface.blit(
            message,
            (70, 485)
        )
