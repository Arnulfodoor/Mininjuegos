import pygame
import random
import time

pygame.init()

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquiva bloques")

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Rectangle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = random.randint(20, 80)
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.width)
        self.rect.y = -self.height
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
rectangles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

score = 0
start_time = time.time()
current_time = start_time
game_over = False

def mostrar_puntaje():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Puntaje: {score}", True, WHITE)
    window.blit(text, (10, 10))

def mostrar_game_over():
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(text, text_rect)

running = True
while running:

    clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        all_sprites.update()

        if random.randint(0, 100) < 5:
            rectangle = Rectangle()
            all_sprites.add(rectangle)
            rectangles.add(rectangle)

        if pygame.sprite.spritecollide(player, rectangles, True):
            game_over = True
            start_time = time.time()

        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= 5:
            for rectangle in rectangles:
                rectangle.speed += 1
            start_time = current_time

        if elapsed_time >= 5:
            score += 1
            start_time = current_time

    window.fill(BLACK)

    all_sprites.draw(window)
    mostrar_puntaje()

    if game_over:
        mostrar_game_over()
        if time.time() - start_time >= 5:
            game_over = False
            score = 0
            start_time = time.time()

    pygame.display.flip()

pygame.quit()
