#https://itch.io/game-assets

import random
import pygame

WIDTH = 600
HEIGHT = 600

clock = pygame.time.Clock()
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load("back.jpg")
bg = pygame.transform.scale(bg, (1200, HEIGHT))
ground = pygame.image.load("ground.png")
ground = pygame.transform.scale(ground, (WIDTH + 200, 100))

flying = False
game_over = False

pipe_gap = 200
pipe_frequence = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequence

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.image = pygame.transform.scale(self.image, (100, 400))
        if position == "top":
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(x, y - pipe_gap // 2))
        elif position == "bottom":
            self.rect = self.image.get_rect(topleft=(x, y + pipe_gap // 2))
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 13):
            img = pygame.image.load("bird/%s.png" % num)
            self.images.append(img)
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0
        self.clicked = False

    def update(self):
        global last_pipe
        if flying == True:
            self.velocity += 1
            if self.rect.bottom < 568:
                self.rect.y += self.velocity
            if self.velocity > 8:
                self.velocity = 8
        if game_over == False and flying == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequence:
                pipe_height = random.randint(-100, 100)
                bottom_pipe = Pipe(WIDTH, HEIGHT // 2 + pipe_height, "bottom")
                top_pipe = Pipe(WIDTH, HEIGHT // 2 + pipe_height, "top")
                pipe_group.add(bottom_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * 3)
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.image = pygame.transform.flip(self.image, True, False)

ground_scroll = 0
scroll_speed = 3
score = 0
pass_pipe = False

bird = Bird(100, HEIGHT // 2)
bird_group = pygame.sprite.Group()
bird_group.add(bird)
pipe_group = pygame.sprite.Group()

running = True

def show_text(label, x, y):
    f1 = pygame.font.Font(None, 36)
    text = f1.render(label, True, (180, 0, 0))
    screen.blit(text, (x, y))

while running:
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    screen.blit(ground, (ground_scroll, 500))
    bird_group.draw(screen)
    bird_group.update()
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
        game_over = True
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left:
            if bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right:
                if pass_pipe == False:
                    pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    show_text("Очки: %s" % score, 500, 10)


    if bird.rect.bottom > 568:
        game_over = True
        flying = False
    if game_over == False:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 46:
            ground_scroll = 0
        pipe_group.update()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    clock.tick(FPS)
