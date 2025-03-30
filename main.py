import random
import sys
import pygame
import os
from const import WIDTH, HEIGHT, BACKGROUND, FONTE, HAND, BUZZ, CLAP, RECORD, TIMER, MUSIC

class Buzz(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(BUZZ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

class Hand(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.image.load(HAND).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound(CLAP)
        self.game = game

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        self.sound.play()
        collisions = pygame.sprite.spritecollide(self, self.game.group_buzz, False)
        self.game.pontos += len(collisions)
        for collision in collisions:
            collision.kill()
            self.game.group_buzz.add(Buzz(random.randrange(0, WIDTH), random.randrange(0, HEIGHT)))

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('BuzzKill Game')
        self.background = pygame.image.load(BACKGROUND).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONTE, 25)
        self.running = True
        self.paused = False
        self.pontos = 0
        self.record = RECORD
        self.timer = TIMER
        self.group_buzz = pygame.sprite.Group()
        for _ in range(25):
            self.group_buzz.add(Buzz(random.randrange(0, WIDTH), random.randrange(0, HEIGHT)))
        self.hand = Hand(self)
        self.hand_group = pygame.sprite.Group(self.hand)
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load(os.path.abspath(MUSIC))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.paused = not self.paused
            if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                self.hand.shoot()

    def update(self):
        if not self.paused:
            self.timer -= 1
            if self.timer < 0:
                self.timer = TIMER
                if self.pontos > self.record:
                    self.record = self.pontos
                self.pontos = 0
                self.paused = True
            self.hand_group.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if not self.paused:
            self.group_buzz.draw(self.screen)
            self.hand_group.draw(self.screen)
            score = self.font.render(f'Points: {self.pontos}', True, (0, 0, 0))
            self.screen.blit(score, (30, 30))
            time_text = self.font.render(f'Time: {self.timer / 60:.1f} s', True, (0, 0, 0))
            self.screen.blit(time_text, (30, 70))
        else:
            self.screen.fill((30, 155, 255))
            pygame.mouse.set_visible(True)
            points_text = self.font.render(f'RECORDE: {self.record}', True, (255, 255, 255))
            pause_text = self.font.render('PRESSIONE ENTER PARA INICIAR', True, (255, 255, 255))
            points_rect = points_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            self.screen.blit(points_text, points_rect)
            self.screen.blit(pause_text, pause_rect)
        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
