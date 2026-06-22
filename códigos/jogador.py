import pygame
pygame.init()


# criação da classe do jogador (que será usada para criar o objeto "jogador" no main)
class jogador():

    # Atributos do jogador (coordenadas iniciais e velocidade)
    def __init__(self, x, y, largura_mapa, power_up = False, slow_down = False):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.largura_mapa = largura_mapa
        self.power_up = power_up
        self.slow_down = slow_down
        # se o power_up for True, a velocidade aumenta em 1 unidade
        if power_up:
            self.velocidade += 1
        # se o slow_down for True, a velocidade diminui em 1 unidade
        if slow_down:
            self.velocidade -= 1


    # Método (função) que controla o movimento do jogador (objeto)
    def movimento(self):

        teclas = pygame.key.get_pressed()   

        # Só é permitido movimentos laterais (porque a tela se move verticalmente)
        if teclas[pygame.K_LEFT] and x > self.velocidade:
            x -= self.velocidade
        if teclas[pygame.K_RIGHT] and x < self.largura_mapa:
            x += self.velocidade
