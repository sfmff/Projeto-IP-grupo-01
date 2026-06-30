import pygame
pygame.init()
pygame.mixer.init()




# criação da classe do jogador (que será usada para criar o objeto "jogador" no main)
class Jogador(pygame.sprite.Sprite):


    # Atributos do jogador (coordenadas iniciais e velocidade)
    def __init__(self, x, y, largura_mapa, altura_mapa):
        super().__init__()


        self.spritesheet = pygame.image.load("assets/sprites_do_jogo/neymar_run_sheet.png").convert_alpha()
        largura_frame = self.spritesheet.get_width() // 5
        altura_frame = self.spritesheet.get_height() // 5
        self.lista_frames = []
        for linha in range (5):
            for coluna in range (5):
                a =  coluna * largura_frame
                b = linha * altura_frame
                area_de_corte = pygame.Rect(a, b, largura_frame, altura_frame)
                frame = self.spritesheet.subsurface(area_de_corte)
                self.lista_frames.append(frame)


        self.left = False
        self.right = True
        self.contador_movimento = 0
        self.velocidade_animaçao = 0.2
        self.indice = 0
        self.image = self.lista_frames[self.indice]
        self.image = pygame.transform.scale(self.image, (200, 220))

        self.largura_mapa = largura_mapa
        self.altura_mapa = altura_mapa
        self.rect = self.image.get_rect()
        self.efeito_invencibilidade = False
        self.fim_efeito = 0

        self.som_apito = pygame.mixer.Sound("assets/audios/som_apito.mp3")
        self.som_apito.set_volume(0.2)
        self.som_torcida = pygame.mixer.Sound("assets/audios/som_torcida_menor.mp3")
        self.som_torcida.set_volume(0.08)
        
        self.rect.x = x
        self.rect.y = y

        self.hitbox = pygame.Rect(0, 0, 60, 83)
        self.hitbox.center = self.rect.center
        self.hitbox.y -= 0

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


        self.indice += self.velocidade_animaçao
        if self.indice >= len(self.lista_frames) :
            self.indice = 0
        self.image = self.lista_frames[int(self.indice)]
        self.image = pygame.transform.scale(self.image, (200, 220))

        if self.left:
            self.image = pygame.transform.flip(self.image, True, False)


        teclas = pygame.key.get_pressed()   

       
        if teclas[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocidade
            self.left = True
            self.right = False
        if teclas[pygame.K_RIGHT] and self.rect.right < self.largura_mapa:
            self.rect.x += self.velocidade
            self.left = False
            self.right = True
        if teclas[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.bottom < self.altura_mapa:
            self.rect.y += self.velocidade
        self.hitbox.center = self.rect.center
        self.hitbox.y -= 0


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