import pygame
pygame.init()
pygame.mixer.init()



# criação da classe do jogador (que será usada para criar o objeto "jogador" no main)
class Jogador(pygame.sprite.Sprite):


    # Atributos do jogador (coordenadas iniciais e velocidade)
    def __init__(self, x, y, largura_mapa, altura_mapa):
        super().__init__()

        self.largura_mapa = largura_mapa
        self.altura_mapa = altura_mapa
        self.image = pygame.image.load("assets/sprites_do_jogo/neymar.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 180))
        self.rect = self.image.get_rect()
        self.efeito_invencibilidade = False
        self.fim_efeito = 0

        self.som_apito = pygame.mixer.Sound("assets/audios/som_apito.mp3")
        self.som_torcida = pygame.mixer.Sound("assets/audios/som_torcida_menor.mp3")
        
        self.rect.x = x
        self.rect.y = y

        self.hitbox = pygame.Rect(0, 0, 50, 80)
        self.hitbox.center = self.rect.center

        self.velocidade = 10
        self.vidas = 5
        self.pontuaçao = 0
        self.multiplicador_pont = 1

        #coletáveis
        self.bolas_de_ouro = 0
        self.gatorade = 0
        self.caneleira = 0
        self.efeito_invencibilidade = False
        self.fim_efeito = 0

    # Método (função) que controla o movimento do jogador (objeto)
    def movimento(self):

        if self.efeito_invencibilidade and (pygame.time.get_ticks() >= self.fim_efeito): # Se o efeito está ativado e passou o tempo dele
            self.efeito_invencibilidade = False

        teclas = pygame.key.get_pressed()   

       
        if teclas[pygame.K_LEFT] and self.rect.x > self.velocidade:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < self.largura_mapa:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] and self.rect.y > self.velocidade:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.bottom < self.altura_mapa:
            self.rect.y += self.velocidade
        self.hitbox.center = self.rect.center


    # Método (função) que recebe o evento (colisão) e atualiza os atributos do jogador
    def atualizaçao(self, evento, valor=1):

        if evento == "dano":
            if not self.efeito_invencibilidade:
                self.som_apito.play()
                self.vidas -= valor

        elif evento == "bola_ouro":
            self.som_torcida.play()
            self.multiplicador_pont += 1
            self.bolas_de_ouro += 1

        elif evento == "isotonico":
            self.som_torcida.play()
            self.gatorade += 1
            self.efeito_invencibilidade = True
            self.fim_efeito = pygame.time.get_ticks() + 3000

        elif evento == "caneleira":
            self.som_torcida.play()
            self.caneleira += 1
            self.vidas += 1