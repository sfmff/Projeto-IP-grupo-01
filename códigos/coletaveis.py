import pygame
import random

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela, tipo):
        super().__init__()
        
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tipo = tipo
        
        # colocar imagens
        self.image = pygame.Surface((40, 40))
        
        # funcoes
        if self.tipo == 'bola_ouro':
            self.image.fill((255, 215, 0))
            self.pontos_ganhos = 500 
            self.multiplicador_bonus = 2.0 
            
        elif self.tipo == 'isotonico':
            self.image.fill((0, 191, 255)) 
            self.tempo_duracao = 5000 
            self.da_invencibilidade = True
            
        elif self.tipo == 'caneleira':
            self.image.fill((169, 169, 169)) 
            self.concede_escudo = True
            
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-10, -10)
        
        self.rect.y = -100
        self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
        
        # velocidade descida
        self.velocidade_y = random.randint(4, 7)

    def update(self):
        self.rect.y += self.velocidade_y
        
        self.hitbox.center = self.rect.center
        
        # se sair da tela some
        if self.rect.top > self.altura_tela:
            self.kill()