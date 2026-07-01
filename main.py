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

PRETO = (20, 20, 20)
BRANCO = (245, 245, 245)
AMARELO = (255, 215, 0)

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Desafio do Drible Infinito")
TELA = pygame.display.set_mode((LARGURA, ALTURA))
RELOGIO = pygame.time.Clock()


def carregar_fonte(tamanho):
    try:
        return pygame.font.SysFont("couriernew", tamanho, bold=True)
    except Exception:
        return pygame.font.Font(None, tamanho)


FONTE_UI = carregar_fonte(24)

try:
    pygame.mixer.music.load("assets/audios/musica_menu.mp3") 
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
except Exception:
    print("Aviso: Música de menu não encontrada.")

class FundoJogo:
    def __init__(self):
            try:
                self.imagem = pygame.image.load("assets/sprites_do_jogo/cenario.png").convert()
                self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
            except Exception:
                print("Aviso: Imagem cenario.png não encontrada.")

            self.y1 = 0
            self.y2 = -ALTURA


    def desenhar(self, tela, velocidade=2):
            self.y1 += velocidade
            self.y2 += velocidade

            if self.y1 >= ALTURA:
                self.y1 = -ALTURA
                
            if self.y2 >= ALTURA:
                self.y2 = -ALTURA

            tela.blit(self.imagem, (0, self.y1))
            tela.blit(self.imagem, (0, self.y2))


class Game:
    def __init__(self, app):
        self.app = app
        self.fundo = FundoJogo()
        
        self.todas_sprites = pygame.sprite.Group()
        self.obstaculos = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()

        self.jogador = Jogador(LARGURA // 2, ALTURA - 200, LARGURA, ALTURA)
        self.todas_sprites.add(self.jogador)

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

        self.SPAWN_OBSTACULO = pygame.USEREVENT + 1
        self.SPAWN_COLETAVEL = pygame.USEREVENT + 2
        
        self.tempo_jogo = 0.0

        self.INTERVALO_OBS_INICIAL = 1.5
        self.INTERVALO_COL_INICIAL = 4.0

        self.FATOR_FREQUENCIA_MAX_OBS = 4.0
        self.FATOR_FREQUENCIA_MAX_COL = 2.0
        self.TEMPO_PARA_DIFICULDADE_MAX = 150

        self.timer_spawn_obstaculo = 0.0
        self.timer_spawn_coletavel = 0.0


    def atualizar_dificuldade(self):
        progresso = min(self.tempo_jogo / self.TEMPO_PARA_DIFICULDADE_MAX, 1.0)

        fator_freq_obs = 1.0 + (self.FATOR_FREQUENCIA_MAX_OBS - 1.0) * progresso
        fator_freq_col = 1.0 + (self.FATOR_FREQUENCIA_MAX_COL - 1.0) * progresso

        intervalo_obs = self.INTERVALO_OBS_INICIAL / fator_freq_obs
        intervalo_col = self.INTERVALO_COL_INICIAL / fator_freq_col
        return intervalo_obs, intervalo_col


    def gerenciar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.app.voltar_ao_menu()


    def atualizar(self, variacao_tempo):
        self.tempo_jogo += variacao_tempo

        intervalo_obs, intervalo_col = self.atualizar_dificuldade()

        self.timer_spawn_obstaculo += variacao_tempo
        if self.timer_spawn_obstaculo >= intervalo_obs:
            self.timer_spawn_obstaculo -= intervalo_obs
            tipos = ('zagueiro', 'cone', 'cartão_amarelo', 'cartão_vermelho')
            obs = Obstaculo(LARGURA, ALTURA, random.choice(tipos))
            self.obstaculos.add(obs)
            self.todas_sprites.add(obs)

        self.timer_spawn_coletavel += variacao_tempo
        if self.timer_spawn_coletavel >= intervalo_col:
            self.timer_spawn_coletavel -= intervalo_col
            tipos = ('bola_ouro', 'isotonico', 'caneleira')
            item = Coletavel(LARGURA, ALTURA, random.choice(tipos))
            self.coletaveis.add(item)
            self.todas_sprites.add(item)

        self.jogador.movimento()
        self.todas_sprites.update()
        
        self.jogador.pontuaçao += 1 * self.jogador.multiplicador_pont

        for obs in self.obstaculos:
            if self.jogador.hitbox.colliderect(obs.hitbox):
                self.jogador.atualizaçao("dano", obs.dano)
                obs.kill()
                if self.jogador.vidas <= 0:
                    self.app.game_over(self.jogador.pontuaçao)
        
        for item in self.coletaveis:
            if self.jogador.hitbox.colliderect(item.hitbox):
                self.jogador.atualizaçao(item.tipo)
                item.kill()


    def desenhar(self, tela):
        velocidade_campo = 8 if self.jogador.efeito_invencibilidade else 4
        self.fundo.desenhar(tela, velocidade=velocidade_campo)
        
        self.todas_sprites.draw(tela)
        
        contagem_vidas = FONTE_UI.render(f"x {self.jogador.vidas}", True, BRANCO)
        contagem_pontos = FONTE_UI.render(f": {self.jogador.pontuaçao}", True, BRANCO)
        contagem_bolas_ouro = FONTE_UI.render(f"x {self.jogador.bolas_de_ouro}", True, BRANCO)
        contagem_caneleiras = FONTE_UI.render(f"x {self.jogador.caneleira}", True, BRANCO)
        contagem_gatorade = FONTE_UI.render(f"x {self.jogador.gatorade}", True, BRANCO)
        
        fundo_placar = pygame.Surface((250, 115))
        fundo_placar.set_alpha(128)
        fundo_placar.fill(PRETO)
        tela.blit(fundo_placar, (20, 20))

        fundo_coletaveis = pygame.Surface((290, 60))
        fundo_coletaveis.set_alpha(128) 
        fundo_coletaveis.fill(PRETO)
        tela.blit(fundo_coletaveis, (500, 20))

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
        
        if self.jogador.efeito_invencibilidade:
            tempo_atual = pygame.time.get_ticks()

            if (tempo_atual // 400) % 2 == 0:
                imagem_turbo = self.imagem_turbo
            else:
                imagem_turbo = self.imagem_turbo_apagado

            imagem_turbo.set_alpha(200)
            tela.blit(imagem_turbo, (250, 10))
            pygame.draw.circle(tela, (135, 206, 235), self.jogador.hitbox.center, 50, 2)


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


    def iniciar_jogo(self):
        self.jogo = Game(self)
        self.estado_atual = App.ESTADO_JOGO


    def game_over(self, pontuacao=0):
        self.tela_game_over = GameOver(self, pontuacao)
        self.estado_atual = App.ESTADO_GAME_OVER


    def voltar_ao_menu(self):
        self.estado_atual = App.ESTADO_MENU


    def sair(self):
        self.rodando = False


    def gerenciar_evento(self, evento):
        if evento.type == pygame.QUIT:
            self.rodando = False
            return
        
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
            self.tela_cheia = not self.tela_cheia
            if self.tela_cheia:
                pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN | pygame.SCALED)
            else:
                pygame.display.set_mode((LARGURA, ALTURA))

        if self.estado_atual == App.ESTADO_MENU:
            self.menu.gerenciar_evento(evento)
        elif self.estado_atual == App.ESTADO_JOGO:
            self.jogo.gerenciar_evento(evento)
        elif self.estado_atual == App.ESTADO_GAME_OVER:
            self.tela_game_over.gerenciar_evento(evento)


    def atualizar(self, variacao_tempo):
        if self.estado_atual == App.ESTADO_MENU:
            self.menu.atualizar(variacao_tempo)
        elif self.estado_atual == App.ESTADO_JOGO:
            self.jogo.atualizar(variacao_tempo)
        elif self.estado_atual == App.ESTADO_GAME_OVER:
            self.tela_game_over.atualizar(variacao_tempo)


    def desenhar(self):
        if self.estado_atual == App.ESTADO_MENU:
            self.menu.desenhar(TELA)
        elif self.estado_atual == App.ESTADO_JOGO:
            self.jogo.desenhar(TELA)
        elif self.estado_atual == App.ESTADO_GAME_OVER:
            self.tela_game_over.desenhar(TELA)
            
        pygame.display.flip()


    def rodar(self):
        while self.rodando:
            variacao_tempo = RELOGIO.tick(FPS) / 1000.0
            
            for evento in pygame.event.get():
                self.gerenciar_evento(evento)

            self.atualizar(variacao_tempo)
            self.desenhar()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    aplicativo = App()
    aplicativo.rodar()