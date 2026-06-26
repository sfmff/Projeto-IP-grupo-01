import pygame
import random

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela, tipo):
        super().__init__()
    
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tipo = tipo

        # Criando os obstáculos zagueiro, cone e cartão (o úncico com a mecânica de andar em diagonais)
        if tipo == 'zagueiro':
            self.image = pygame.image.load('assets/cenário e jogadores/zagueiro.png').convert_alpha()
            self.velocidade_y = random.randint(3, 5)
            self.velocidade_x = random.randint(-9, -6)
        
        elif tipo == 'cone':
            self.image = pygame.image.load('assets/cenário e jogadores/cone.png').convert_alpha()
            self.velocidade_y = random.randint(3, 5)
            self.velocidade_x = 0
        
        elif tipo == 'cartão':
            self.image = pygame.image.load('assets/cenário e jogadores/cartão.png').convert_alpha()
            self.velocidade_y = random.randint(6, 9)
            self.velocidade_x = random.choice([-3, 3])
        
        # Hitbox dos obstáculos
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-10, -10)

        # Spawn dos obstáculos
        if self.tipo == 'zagueiro':
            self.rect.y = random.randint(-50, self.altura_tela // 2)
            self.rect.x = self.largura_tela + 10
        else:
            self.rect.y = -100
            self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
            
    # Movimentação dos obstáculos
    def update(self):
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x

        # Lógica do cartão: quando ele bater na parede do mapa ele inverter a direção do movimento
        if self.tipo == 'cartão':
            if self.rect.right >= self.largura_tela or self.rect.left <= 0:
                self.velocidade_x *= -1
        
        # Removendo o obstáculo assim que o jogador passa por ele
        saiu_pelo_fundo = self.rect.top > self.altura_tela
        saiu_pelo_lado = self.rect.right < 0

        if saiu_pelo_fundo or saiu_pelo_lado:
            self.kill()
