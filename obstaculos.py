import pygame
import random

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela, tipo):
        super().__init__()
    
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tipo = tipo

        # Criando os obstáculos zagueiro, cone e cartão
        if tipo == 'zagueiro':
            self.image = pygame.image.load('assets/sprites_do_jogo/zagueiro.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 160))
            self.velocidade_y = random.randint(3, 5)
            self.velocidade_x = random.randint(-9, -6)
            self.dano = 2

        elif tipo == 'cone':
            self.image = pygame.image.load('assets/sprites_do_jogo/cone.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 60))
            self.velocidade_y = random.randint(3, 5)
            self.velocidade_x = 0
            self.dano = 1

        elif tipo == 'cartão_amarelo':
            self.image = pygame.image.load('assets/sprites_do_jogo/cartão_amarelo.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 50))
            self.velocidade_y = random.randint(6, 9)
            self.velocidade_x = random.choice([-3, 3])
            self.dano = 1

        elif tipo == 'cartão_vermelho':
            self.image = pygame.image.load('assets/sprites_do_jogo/cartão_vermelho.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 50))
            self.velocidade_y = random.randint(8, 11)
            self.velocidade_x = random.choice([-4, 4])
            self.dano = 3

        # Hitbox dos obstáculos
        self.rect = self.image.get_rect()

        if self.tipo == 'zagueiro':
            # Hitbox menor e mais "justa" que a imagem, já que o sprite
            # do zagueiro tem muito espaço vazio nas bordas
            self.hitbox = self.rect.inflate(-30, -110)
        else:
            self.hitbox = self.rect.inflate(-10, -10)

        # Spawn dos obstáculos
        if self.tipo == 'zagueiro':
            self.rect.y = random.randint(-50, self.altura_tela // 2)
            self.rect.x = self.largura_tela + 10
        else:
            self.rect.y = -100
            self.rect.x = random.randint(60, self.largura_tela - self.rect.width - 60)
        
        self.hitbox.center = self.rect.center

    # Movimentação dos obstáculos
    def update(self):
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x
        self.hitbox.center = self.rect.center

        # Lógica do cartão: quando ele bater na parede do mapa ele inverter a direção do movimento
        if self.tipo == 'cartão_amarelo' or self.tipo == 'cartão_vermelho':
            if self.rect.right >= self.largura_tela or self.rect.left <= 0:
                self.velocidade_x *= -1
        
        # Removendo o obstáculo assim que o jogador passa por ele
        saiu_pelo_fundo = self.rect.top > self.altura_tela
        saiu_pelo_lado = self.rect.right < 0

        if saiu_pelo_fundo or saiu_pelo_lado:
            self.kill()