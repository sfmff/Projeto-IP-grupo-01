import pygame
import random

class Coletavel(pygame.sprite.Sprite):
    def __init__(self, largura_tela, altura_tela, tipo):
        super().__init__()
        
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tipo = tipo
        
        if self.tipo == 'bola_ouro':
            self.image = pygame.image.load('assets/sprites_do_jogo/bola_de_ouro.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40)) 
            
            self.pontos_ganhos = 500 
            self.multiplicador_bonus = 2.0 
            
        elif self.tipo == 'isotonico':
            self.image = pygame.image.load('assets/sprites_do_jogo/isotonico.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40)) 
            
            self.tempo_duracao = 5000 
            self.da_invencibilidade = True
            
        elif self.tipo == 'caneleira':
            self.image = pygame.image.load('assets/sprites_do_jogo/caneleira_aco.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40)) 
            
            self.concede_escudo = True
            
        # hitbox e posicionamento na tela
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-10, -10)
        
        self.rect.y = -100
        self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
        
        self.velocidade_y = random.randint(4, 7)

    def update(self):
        self.rect.y += self.velocidade_y
        
        # ajustar hitbox
        self.hitbox.center = self.rect.center
        
        # se sair da tela é excluido
        if self.rect.top > self.altura_tela:
            self.kill()