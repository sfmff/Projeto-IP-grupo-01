import pygame
pygame.init()


# criação da classe do jogador (que será usada para criar o objeto "jogador" no main)
class jogador():

    # Atributos do jogador (coordenadas iniciais e velocidade)
    def __init__(self, x, y, largura_mapa, bateu_no_obstaculo = False,):

        self.image = pygame.image.load("assets/cenário e jogadores/neymar.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 180))
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-10, -10)

        self.rect.x = x
        self.rect.y = y
        self.velocidade = 10
        self.largura_mapa = largura_mapa
        self.bateu_no_obstaculo = bateu_no_obstaculo
        self.vidas = 5

        #coletáveis
        self.bolas_de_ouro = 0
        self.gatorade = 0
        self.caneleira = 0

        # se o power_up for True, a velocidade aumenta em 1 unidade
        if self.bolas_de_ouro >= 1:
            self.velocidade += self.bolas_de_ouro

        # se o bateu_no_obstaculo for True
        if bateu_no_obstaculo:
            self.vidas -= 1


    # Método (função) que controla o movimento do jogador (objeto)
    def movimento(self):

        teclas = pygame.key.get_pressed()   

        # Só é permitido movimentos laterais (porque a tela se move verticalmente)
        if teclas[pygame.K_LEFT] and self.rect.x > self.velocidade:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < self.largura_mapa:
            self.rect.x += self.velocidade
        self.hitbox.center = self.rect.center
