import pygame
pygame.init()


# criação da classe do jogador (que será usada para criar o objeto "jogador" no main)
class jogador():

    # Atributos do jogador (coordenadas iniciais e velocidade)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 5

    # Método (função) que controla o movimento do jogador (objeto)
    def movimento(self):

        teclas = pygame.key.get_pressed()   

        if teclas[pygame.K_LEFT]:
            x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            x += self.velocidade
        if teclas[pygame.K_UP]:
            y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            y += self.velocidade