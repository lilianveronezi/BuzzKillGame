import random
import sys
import pygame
import os
from const import WIDTH, HEIGHT, BACKGROUND, FONTE, HAND, BUZZ, CLAP, RECORD, TIMER, MUSIC


class Buzz(pygame.sprite.Sprite):
    # Classe que representa um mosquito na tela.
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(BUZZ).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))


class Hand(pygame.sprite.Sprite):
    # Classe que representa a mão do jogador, controlada pelo mouse.
    def __init__(self, game):
        super().__init__()
        self.image = pygame.image.load(HAND).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound(CLAP)
        self.game = game

    def update(self):
        # Atualiza a posição da mão para seguir o mouse.
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        # Executa o ataque da mão e verifica colisões com os mosquitos.
        self.sound.play()
        mosquitos_acertados = pygame.sprite.spritecollide(self, self.game.group_buzz, True)
        self.game.pontos += len(mosquitos_acertados)

        # Adiciona novos mosquitos após cada acerto
        for _ in mosquitos_acertados:
            self.game.group_buzz.add(Buzz(random.randint(0, WIDTH), random.randint(0, HEIGHT)))


class Game:
    # Classe principal que gerencia o jogo.
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Configuração da tela
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('BuzzKill Game')

        # Configuração de assets
        self.background = pygame.image.load(BACKGROUND).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.font = pygame.font.Font(FONTE, 25)

        # Variáveis de controle
        self.running = True
        self.paused = False
        self.pontos = 0
        self.record = RECORD
        self.timer = TIMER

        # Grupos de sprites
        self.group_buzz = pygame.sprite.Group()
        for _ in range(25):
            self.group_buzz.add(Buzz(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

        self.hand = Hand(self)
        self.hand_group = pygame.sprite.Group(self.hand)

        # Esconde o cursor do mouse
        pygame.mouse.set_visible(False)

        # Configuração de música
        pygame.mixer.music.load(os.path.abspath(MUSIC))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        # Configuração do relógio
        self.clock = pygame.time.Clock()

    def run(self):
        # Loop principal do jogo.
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        # Gerencia os eventos do jogo.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.paused = not self.paused
                    if not self.paused:
                        pygame.mouse.set_visible(False)  # Garante que o cursor permaneça invisível ao reiniciar o jogo
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                self.hand.shoot()

    def update(self):
        # Atualiza o estado do jogo se não estiver pausado.
        if not self.paused:
            self.timer -= 1
            if self.timer < 0:
                self.reset_game()
            self.hand_group.update()

    def reset_game(self):
        # Reinicia os parâmetros do jogo quando o tempo acaba.
        self.timer = TIMER
        if self.pontos > self.record:
            self.record = self.pontos
        self.pontos = 0
        self.paused = True
        pygame.mouse.set_visible(True)

    def draw(self):
        # Desenha os elementos na tela.
        self.screen.blit(self.background, (0, 0))

        if not self.paused:
            self.group_buzz.draw(self.screen)
            self.hand_group.draw(self.screen)

            # Exibe pontuação e tempo
            score_text = self.font.render(f'Pontos: {self.pontos}', True, (0, 0, 0))
            time_text = self.font.render(f'Tempo: {self.timer / 60:.1f} s', True, (0, 0, 0))
            self.screen.blit(score_text, (30, 30))
            self.screen.blit(time_text, (30, 70))
        else:
            # Tela de pausa
            self.screen.fill((30, 155, 255))
            record_text = self.font.render(f'RECORDE: {self.record}', True, (255, 255, 255))
            pause_text = self.font.render('PRESSIONE ENTER PARA INICIAR', True, (255, 255, 255))

            self.screen.blit(record_text, record_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            self.screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
