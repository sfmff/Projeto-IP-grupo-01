import pygame
pygame.init()


# criação da classe do jogador (que será usada para criar o objeto "jogador" no main)
class jogador():

    # Atributos do jogador (coordenadas iniciais e velocidade)
    def __init__(self, x, y, largura_mapa):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.largura_mapa = largura_mapa


    # Método (função) que controla o movimento do jogador (objeto)
    def movimento(self):

        teclas = pygame.key.get_pressed()   

        # Só é permitido movimentos laterais (porque a tela se move verticalmente)
        if teclas[pygame.K_LEFT] and x > self.velocidade:
            x -= self.velocidade
        if teclas[pygame.K_RIGHT] and x < self.largura_mapa:
            x += self.velocidade
