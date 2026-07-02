import pygame
import sys
import random
from jogador import Jogador
from coletaveis import Coletavel
from obstaculos import Obstaculo
from menu_inicial import Menu
from game_over import GameOver


LARGURA, ALTURA = 800, 600
FPS = 60

# Cores utilizadas durante o código
AZUL = (135, 206, 235)
PRETO = (20, 20, 20)
BRANCO = (245, 245, 245)

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Desafio do Drible Infinito")
TELA = pygame.display.set_mode((LARGURA, ALTURA))
RELOGIO = pygame.time.Clock()

# Em caso da fonte selecionada não estar instalada
def carregar_fonte(tamanho):
    try:
        return pygame.font.SysFont("couriernew", tamanho, bold=True)
    except Exception:
        return pygame.font.Font(None, tamanho)

FONTE_UI = carregar_fonte(24)

# Tenta tocar a música de fundo
try:
    pygame.mixer.music.load("assets/audios/musica_menu.mp3") 
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
except Exception:
    print("Aviso: Música de menu não encontrada.")

# Classe que cria e faz o cenário "andar"
class FundoJogo:
    def __init__(self):
            try:
                self.imagem = pygame.image.load("assets/sprites_do_jogo/cenario.png").convert()
                self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
            except Exception:
                print("Aviso: Imagem cenario.png não encontrada.")

            # Cria duas cópias do cenário
            self.y1 = 0
            self.y2 = -ALTURA

    # Desenha o cenário
    def desenhar(self, tela, velocidade):
            # Faz o cenário rodar na velocidade específica
            self.y1 += velocidade
            self.y2 += velocidade

            if self.y1 >= ALTURA:
                self.y1 = -ALTURA
                
            if self.y2 >= ALTURA:
                self.y2 = -ALTURA

            tela.blit(self.imagem, (0, self.y1))
            tela.blit(self.imagem, (0, self.y2))

# Gerencia tudo que acontece durante o jogo
class Game:
    def __init__(self, app):
        self.app = app
        self.fundo = FundoJogo()
        
        # Agrupa todas as sprites
        self.todas_sprites = pygame.sprite.Group()
        self.obstaculos = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()

        # Carrega a classe do jogador
        self.jogador = Jogador(LARGURA // 2, ALTURA - 200, LARGURA, ALTURA)
        self.todas_sprites.add(self.jogador)

        # Carrega todas as imagens
        self.imagem_vida = pygame.image.load("assets/sprites_do_jogo/vida.png").convert_alpha()
        self.imagem_vida = pygame.transform.scale(self.imagem_vida, (45, 45))
        self.imagem_bola_ouro = pygame.image.load('assets/sprites_do_jogo/bola_de_ouro.png').convert_alpha()
        self.imagem_bola_ouro = pygame.transform.scale(self.imagem_bola_ouro, (40, 40))
        self.imagem_gatorade = pygame.image.load('assets/sprites_do_jogo/isotonico.png').convert_alpha()
        self.imagem_gatorade = pygame.transform.scale(self.imagem_gatorade, (40, 40))
        self.imagem_caneleira = pygame.image.load('assets/sprites_do_jogo/caneleira_aco.png').convert_alpha()
        self.imagem_caneleira = pygame.transform.scale(self.imagem_caneleira, (40, 40)) 
        self.imagem_pontuacao = pygame.image.load('assets/sprites_do_jogo/pontuacao.png').convert_alpha()
        self.imagem_pontuacao = pygame.transform.scale(self.imagem_pontuacao, (150, 120)) 
        self.imagem_turbo = pygame.image.load('assets/sprites_do_jogo/turbo.png').convert_alpha()
        self.imagem_turbo = pygame.transform.scale(self.imagem_turbo, (280, 230)) 
        self.imagem_turbo_apagado = pygame.image.load('assets/sprites_do_jogo/turbo(apagado).png').convert_alpha()
        self.imagem_turbo_apagado = pygame.transform.scale(self.imagem_turbo_apagado, (280, 230))
        
        self.tempo_jogo = 0.0

        # Intervalo de criação para consumíveis e obstáculos inicialmente
        self.INTERVALO_OBS_INICIAL = 1.5
        self.INTERVALO_COL_INICIAL = 4.0

        # Aumento máximo com o passar do tempo
        self.FATOR_FREQUENCIA_MAX_OBS = 4.0
        self.FATOR_FREQUENCIA_MAX_COL = 2.0
        self.TEMPO_PARA_DIFICULDADE_MAX = 150   # Tempo para atingir o aumento máximo

        self.timer_spawn_obstaculo = 0.0
        self.timer_spawn_coletavel = 0.0

        self.fundo_placar = pygame.Surface((250, 115))
        self.fundo_placar.set_alpha(128)
        self.fundo_placar.fill(PRETO)
        self.fundo_coletaveis = pygame.Surface((290, 60))
        self.fundo_coletaveis.set_alpha(128) 
        self.fundo_coletaveis.fill(PRETO)

    # Função que vai mudando a dificuldade com o passar do tempo
    def atualizar_dificuldade(self):
        progresso = min(self.tempo_jogo / self.TEMPO_PARA_DIFICULDADE_MAX, 1.0) # Calcula a porcentagem de quão difícil o jogo deve estar, de 0 a 100

        # Frequencia de spawn
        fator_freq_obs = 1.0 + (self.FATOR_FREQUENCIA_MAX_OBS - 1.0) * progresso
        fator_freq_col = 1.0 + (self.FATOR_FREQUENCIA_MAX_COL - 1.0) * progresso

        # Intervalo entre spawns
        intervalo_obs = self.INTERVALO_OBS_INICIAL / fator_freq_obs
        intervalo_col = self.INTERVALO_COL_INICIAL / fator_freq_col
        return intervalo_obs, intervalo_col

    # Pausar ou sair do jogo
    def gerenciar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.app.voltar_ao_menu()

    # Atualiza a criação de obstáculos e consumíveis a cada variação de tempo
    def atualizar(self, variacao_tempo):
        self.tempo_jogo += variacao_tempo

        intervalo_obs, intervalo_col = self.atualizar_dificuldade()

        self.timer_spawn_obstaculo += variacao_tempo
        if self.timer_spawn_obstaculo >= intervalo_obs: # Spawna um obstáculo aleatório
            self.timer_spawn_obstaculo -= intervalo_obs
            tipos = ('zagueiro', 'cone', 'cartão_amarelo', 'cartão_vermelho')
            obs = Obstaculo(LARGURA, ALTURA, random.choice(tipos))
            self.obstaculos.add(obs)
            self.todas_sprites.add(obs)

        self.timer_spawn_coletavel += variacao_tempo
        if self.timer_spawn_coletavel >= intervalo_col: # Spawna um consumível aleatório
            self.timer_spawn_coletavel -= intervalo_col
            tipos = ('bola_ouro', 'isotonico', 'caneleira')
            item = Coletavel(LARGURA, ALTURA, random.choice(tipos))
            self.coletaveis.add(item)
            self.todas_sprites.add(item)

        self.jogador.movimento()
        self.todas_sprites.update()
        
        self.jogador.pontuaçao += 1 * self.jogador.multiplicador_pont

        # Em caso de colisão com obstáculo
        for obs in self.obstaculos:
            if self.jogador.hitbox.colliderect(obs.hitbox):
                self.jogador.atualizaçao("dano", obs.dano)
                obs.kill()
                if self.jogador.vidas <= 0:
                    self.app.game_over(self.jogador.pontuaçao)
        
        # Em caso de colisão com consumível
        for item in self.coletaveis:
            if self.jogador.hitbox.colliderect(item.hitbox):
                self.jogador.atualizaçao(item.tipo)
                item.kill()

    # Desenha a tela, sendo o cenário e o HUD
    def desenhar(self, tela):
        velocidade_campo = 8 if self.jogador.efeito_invencibilidade else 4
        self.fundo.desenhar(tela, velocidade=velocidade_campo)
        self.todas_sprites.draw(tela)
        
        contagem_vidas = FONTE_UI.render(f"x {self.jogador.vidas}", True, BRANCO)
        contagem_pontos = FONTE_UI.render(f": {self.jogador.pontuaçao}", True, BRANCO)
        contagem_bolas_ouro = FONTE_UI.render(f"x {self.jogador.bolas_de_ouro}", True, BRANCO)
        contagem_caneleiras = FONTE_UI.render(f"x {self.jogador.caneleira}", True, BRANCO)
        contagem_gatorade = FONTE_UI.render(f"x {self.jogador.gatorade}", True, BRANCO)
        
        tela.blit(self.fundo_placar, (20, 20))
        tela.blit(self.fundo_coletaveis, (500, 20))

        tela.blit(self.imagem_pontuacao, (20, 0))
        tela.blit(self.imagem_vida, (30, 80))
        tela.blit(self.imagem_bola_ouro, (510, 30))
        tela.blit(self.imagem_caneleira, (600, 30))
        tela.blit(self.imagem_gatorade, (690, 30))

        tela.blit(contagem_pontos, (160, 45))
        tela.blit(contagem_vidas, (80, 90))
        tela.blit(contagem_bolas_ouro, (550, 38))
        tela.blit(contagem_caneleiras, (640, 38))
        tela.blit(contagem_gatorade, (730, 38))
        
        # Mostra o texto "TURBO ATIVADO!" quando invencível
        if self.jogador.efeito_invencibilidade:
            tempo_atual = pygame.time.get_ticks()

            if (tempo_atual // 400) % 2 == 0:
                imagem_turbo = self.imagem_turbo
            else:
                imagem_turbo = self.imagem_turbo_apagado

            imagem_turbo.set_alpha(200)
            tela.blit(imagem_turbo, (250, 10))
            pygame.draw.circle(tela, (AZUL), self.jogador.hitbox.center, 50, 2) # Cria uma bolha azul em volta do jogador

# Controla oque deve estar ativo: Menu inicial, Jogo ou Game Over
class App:
    ESTADO_MENU = "menu"
    ESTADO_JOGO = "jogo"
    ESTADO_GAME_OVER = "game_over"

    def __init__(self):
        self.estado_atual = App.ESTADO_MENU
        self.menu = Menu(self)
        self.tela_game_over = None 
        self.jogo = None
        self.rodando = True
        self.tela_cheia = False

    # Começa o jogo
    def iniciar_jogo(self):
        self.jogo = Game(self)
        self.estado_atual = App.ESTADO_JOGO

    # Leva pra tela final
    def game_over(self, pontuacao=0):
        self.tela_game_over = GameOver(self, pontuacao)
        self.estado_atual = App.ESTADO_GAME_OVER

    # Volta pra tela inicial
    def voltar_ao_menu(self):
        self.estado_atual = App.ESTADO_MENU

    # Sai do jogo
    def sair(self):
        self.rodando = False

    # Possíveis eventos para mudança de estado do jogo
    def gerenciar_evento(self, evento):
        if evento.type == pygame.QUIT:
            self.rodando = False
            return
        
        # Deixa o jogo em tela cheia
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
            self.tela_cheia = not self.tela_cheia
            if self.tela_cheia:
                pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN | pygame.SCALED)
            else:
                pygame.display.set_mode((LARGURA, ALTURA))

        # Leva para a função gerenciar_evento para mudar a tela do jogo
        if self.estado_atual == App.ESTADO_MENU:
            self.menu.gerenciar_evento(evento)
        elif self.estado_atual == App.ESTADO_JOGO:
            self.jogo.gerenciar_evento(evento)
        elif self.estado_atual == App.ESTADO_GAME_OVER:
            self.tela_game_over.gerenciar_evento(evento)

    # Atualiza o evento na classe Menu, no módulo menu_inicial.py
    def atualizar(self, variacao_tempo):
        if self.estado_atual == App.ESTADO_MENU:
            self.menu.atualizar(variacao_tempo)
        elif self.estado_atual == App.ESTADO_JOGO:
            self.jogo.atualizar(variacao_tempo)
        elif self.estado_atual == App.ESTADO_GAME_OVER:
            self.tela_game_over.atualizar(variacao_tempo)

    # Desenha os elementos do menu inicial
    def desenhar(self):
        if self.estado_atual == App.ESTADO_MENU:
            self.menu.desenhar(TELA)
        elif self.estado_atual == App.ESTADO_JOGO:
            self.jogo.desenhar(TELA)
        elif self.estado_atual == App.ESTADO_GAME_OVER:
            self.tela_game_over.desenhar(TELA)
            
        pygame.display.flip()

    # Começa a rodar o jogo
    def rodar(self):
        while self.rodando: # Roda a 60 vezes por segundo
            variacao_tempo = RELOGIO.tick(FPS) / 1000.0
            
            for evento in pygame.event.get():
                self.gerenciar_evento(evento)

            self.atualizar(variacao_tempo)
            self.desenhar()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    aplicativo = App()  # O aplicativo vira uma cópia da classe App, que depois é iniciada sua função rodar()
    aplicativo.rodar()