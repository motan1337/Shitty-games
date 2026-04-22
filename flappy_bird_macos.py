import base64
import io
import os
import random
import sys

os.environ["SDL_HINT_RENDER_VSYNC"] = "1"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

WIDTH, HEIGHT = 400, 600
FPS = 60

BG_COLOR = (255, 182, 193)
GRAVITY = 0.5
FLAP_STRENGTH = -9
PIPE_SPEED = 3
PIPE_GAP = 160
PIPE_SPACING = 250
PIPE_WIDTH = 70

BIRD_SIZE = (56, 40)


BIRD_B64 = """
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
tikAAAAASUVORK5CYII=
"""

TOWERS_B64 = """
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
"""


def load_embedded_image(b64_string):
    """Decode a base64 string into a pygame Surface."""
    raw = base64.b64decode(b64_string.strip())
    return pygame.image.load(io.BytesIO(raw)).convert_alpha()


class Bird:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

    def draw(self, surface):
        angle = max(-25, min(-self.velocity * 3, 25))
        rotated = pygame.transform.rotate(self.image, angle)
        rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rect)


class PipePair:
    def __init__(self, x, tower_img):
        self.x = x
        self.passed = False
        self.gap_y = random.randint(80, HEIGHT - 80 - PIPE_GAP)
        self.tower_img = tower_img
        self.tower_img_flipped = pygame.transform.flip(tower_img, False, True)

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, surface):
        top_rect = self.tower_img_flipped.get_rect(
            bottomleft=(self.x, self.gap_y)
        )
        surface.blit(self.tower_img_flipped, top_rect)

        bottom_rect = self.tower_img.get_rect(
            topleft=(self.x, self.gap_y + PIPE_GAP)
        )
        surface.blit(self.tower_img, bottom_rect)

    def get_rects(self):
        top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        bottom = pygame.Rect(
            self.x, self.gap_y + PIPE_GAP,
            PIPE_WIDTH, HEIGHT - (self.gap_y + PIPE_GAP)
        )
        return top, bottom

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0


def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont("arial", size, bold=True)
    label = font.render(text, True, color)
    outline = font.render(text, True, (0, 0, 0))
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        surface.blit(outline, outline.get_rect(center=(x + dx, y + dy)))
    surface.blit(label, label.get_rect(center=(x, y)))


def run_game():
    pygame.init()
    try:
        screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.SCALED | pygame.DOUBLEBUF,
            vsync=1,
        )
    except pygame.error:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    pygame.display.set_caption("5PuNk fOr m1Lk!")
    clock = pygame.time.Clock()

    bird_raw = load_embedded_image(BIRD_B64)
    bird_img = pygame.transform.scale(bird_raw, BIRD_SIZE)

    tower_raw = load_embedded_image(TOWERS_B64)
    tower_img = pygame.transform.scale(tower_raw, (PIPE_WIDTH, HEIGHT))

    def new_game():
        return {
            "bird": Bird(bird_img),
            "pipes": [PipePair(WIDTH + i * PIPE_SPACING, tower_img)
                      for i in range(3)],
            "score": 0,
            "game_over": False,
            "started": False,
        }

    state = new_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE and not state["game_over"]:
                    state["started"] = True
                    state["bird"].flap()
                if event.key == pygame.K_r and state["game_over"]:
                    state = new_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not state["game_over"]:
                    state["started"] = True
                    state["bird"].flap()

        if state["started"] and not state["game_over"]:
            state["bird"].update()

            for pipe in state["pipes"]:
                pipe.update()

            if state["pipes"][0].off_screen():
                state["pipes"].pop(0)
                last_x = state["pipes"][-1].x
                state["pipes"].append(PipePair(last_x + PIPE_SPACING, tower_img))

            for pipe in state["pipes"]:
                if not pipe.passed and pipe.x + PIPE_WIDTH < state["bird"].rect.x:
                    pipe.passed = True
                    state["score"] += 1

            bird_rect = state["bird"].rect
            if bird_rect.top < 0 or bird_rect.bottom > HEIGHT:
                state["game_over"] = True

            for pipe in state["pipes"]:
                top, bottom = pipe.get_rects()
                if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                    state["game_over"] = True

        screen.fill(BG_COLOR)

        for pipe in state["pipes"]:
            pipe.draw(screen)

        state["bird"].draw(screen)

        draw_text(screen, str(state["score"]), 48, WIDTH // 2, 50)

        if not state["started"]:
            draw_text(screen, "Press space or just click...", 24, WIDTH // 2, HEIGHT // 2 + 80)

        if state["game_over"]:
            draw_text(screen, "YOU SUCK!", 48, WIDTH // 2, HEIGHT // 2 - 20)
            draw_text(screen, "Press R to restart", 22, WIDTH // 2, HEIGHT // 2 + 30)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    run_game()