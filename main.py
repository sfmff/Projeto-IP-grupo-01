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
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except Exception:
    print("Aviso: Música de menu não encontrada.")

class FundoJogo:
    def __init__(self):
            try:
                self.imagem = pygame.image.load("assets/sprites_do_jogo/cenario.png").convert()
                self.imagem = pygame.transform.scale(self.imagem, (LARGURA, ALTURA))
            except Exception:
                print("Aviso: Imagem cenario.png não encontrada. Usando fundo verde reserva.")
                self.imagem = pygame.Surface((LARGURA, ALTURA))
                self.imagem.fill((34, 139, 34))

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

        # Eventos Customizados para Spawn
        self.SPAWN_OBSTACULO = pygame.USEREVENT + 1
        self.SPAWN_COLETAVEL = pygame.USEREVENT + 2
        
        pygame.time.set_timer(self.SPAWN_OBSTACULO, 1500) 
        pygame.time.set_timer(self.SPAWN_COLETAVEL, 4000) 


    def gerenciar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.app.voltar_ao_menu()
            
        if evento.type == self.SPAWN_OBSTACULO:
            tipos = ('zagueiro', 'cone', 'cartão')
            obs = Obstaculo(LARGURA, ALTURA, random.choice(tipos))
            self.obstaculos.add(obs)
            self.todas_sprites.add(obs)
            
        if evento.type == self.SPAWN_COLETAVEL:
            tipos = ('bola_ouro', 'isotonico', 'caneleira')
            item = Coletavel(LARGURA, ALTURA, random.choice(tipos))
            self.coletaveis.add(item)
            self.todas_sprites.add(item)


    def atualizar(self, variacao_tempo):
        self.jogador.movimento()
        self.todas_sprites.update()
        
        self.jogador.pontuaçao += 1 * self.jogador.multiplicador_pont

        for obs in self.obstaculos:
            if self.jogador.hitbox.colliderect(obs.hitbox):
                self.jogador.atualizaçao("dano")
                obs.kill()
                if self.jogador.vidas <= 0:
                    self.app.game_over()
        
        for item in self.coletaveis:
            if self.jogador.hitbox.colliderect(item.hitbox):
                self.jogador.atualizaçao(item.tipo)
                item.kill()
                    
                self.jogador.atualizaçao(item.tipo)
                item.kill()


    def desenhar(self, tela):
        velocidade_campo = 8 if self.jogador.efeito_invencibilidade else 4
        self.fundo.desenhar(tela, velocidade=velocidade_campo)
        
        self.todas_sprites.draw(tela)
        
        contagem_vidas = FONTE_UI.render(f"Contagem de Vidas: {self.jogador.vidas}", True, BRANCO)
        contagem_pontos = FONTE_UI.render(f"Pontuação: {self.jogador.pontuaçao}", True, BRANCO)
        contagem_bolas_ouro = FONTE_UI.render(f"Bolas de Ouro: {self.jogador.bolas_de_ouro}", True, BRANCO)
        contagem_caneleiras = FONTE_UI.render(f"Caneleiras: {self.jogador.caneleira}", True, BRANCO)
        contagem_gatorade = FONTE_UI.render(f"Isotônicos: {self.jogador.gatorade}", True, BRANCO)
        
        fundo_placar = pygame.Surface((300, 80))
        fundo_placar.set_alpha(128) 
        fundo_placar.fill(PRETO)
        tela.blit(fundo_placar, (20, 20))

        fundo_coletaveis = pygame.Surface((280, 110))
        fundo_coletaveis.set_alpha(128) 
        fundo_coletaveis.fill(PRETO)
        tela.blit(fundo_coletaveis, (500, 20))

        tela.blit(contagem_vidas, (30, 30))
        tela.blit(contagem_pontos, (30, 60))
        tela.blit(contagem_bolas_ouro, (520, 30))
        tela.blit(contagem_caneleiras, (520, 60))
        tela.blit(contagem_gatorade, (520, 90))
        
        if self.jogador.efeito_invencibilidade:
            texto_turbo = FONTE_UI.render("TURBO ATIVADO!", True, AMARELO)
            tela.blit(texto_turbo, (LARGURA // 2 - 80, 40))


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


    def iniciar_jogo(self):
        self.jogo = Game(self)
        self.estado_atual = App.ESTADO_JOGO


    def game_over(self):
        self.tela_game_over = GameOver(self)
        self.estado_atual = App.ESTADO_GAME_OVER


    def voltar_ao_menu(self):
        self.estado_atual = App.ESTADO_MENU


    def sair(self):
        self.rodando = False


    def gerenciar_evento(self, evento):
        if evento.type == pygame.QUIT:
            self.rodando = False
            return
        
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