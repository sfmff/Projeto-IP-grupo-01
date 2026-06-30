import pygame

# CONFIGURAÇÕES GERAIS
LARGURA, ALTURA = 800, 600

VERDE_CAMPO_1 = (34, 139, 34)
VERDE_CAMPO_2 = (30, 120, 30)
BRANCO = (245, 245, 245)
PRETO = (20, 20, 20)
VERMELHO = (200, 30, 30)
VERDE_BOTAO = (46, 160, 67)
VERDE_BOTAO_HOVER = (76, 200, 97)
VERDE_BOTAO_CLICK = (26, 120, 47)


TELA = pygame.display.get_surface()


if not pygame.mixer.get_init():
    pygame.mixer.init()

# Carregamento do som de hover dos botões
try:
    SOM_HOVER = pygame.mixer.Sound("Projeto-IP-grupo-01/assets/audios/passar_cima_botao.mp3")
    SOM_HOVER.set_volume(0.1)
except Exception:
    try:
        SOM_HOVER = pygame.mixer.Sound("assets/audios/passar_cima_botao.mp3")
        SOM_HOVER.set_volume(0.1)
    except Exception:
        print("Aviso: O arquivo 'passar_cima_botao.mp3' não foi encontrado.")
        SOM_HOVER = None

# Carregamento do som de clique
try:
    SOM_CLIQUE = pygame.mixer.Sound("Projeto-IP-grupo-01/assets/audios/clique_botao.mp3")
    SOM_CLIQUE.set_volume(0.7)
except Exception:
    try:
        SOM_CLIQUE = pygame.mixer.Sound("assets/audios/clique_botao.mp3")
        SOM_CLIQUE.set_volume(0.7)
    except Exception:
        print("Aviso: O arquivo 'clique_botao.mp3' não foi encontrado.")
        SOM_CLIQUE = None


def carregar_fonte(tamanho):
    try:
        return pygame.font.SysFont("couriernew", tamanho, bold=True)
    except Exception:
        return pygame.font.Font(None, tamanho)


FONTE_TITULO = carregar_fonte(54)
FONTE_BOTAO = carregar_fonte(32)
FONTE_PONTUACAO = carregar_fonte(28)


# Classe Botão (botão com efeito sonoro no hover e clique)
class Botao:

    def __init__(self, x, y, largura, altura, texto, acao_clique,
                 cor_normal=VERDE_BOTAO, cor_hover=VERDE_BOTAO_HOVER, cor_click=VERDE_BOTAO_CLICK):
        self.retangulo_base = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.acao_clique = acao_clique

        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_click = cor_click

        self.mouse_por_cima = False
        self.pressionado = False
        self.escala_atual = 1.0
        self.escala_alvo = 1.0
        self.opacidade_flash = 0

    def gerenciar_evento(self, evento):
        posicao_mouse = pygame.mouse.get_pos()
        estava_por_cima = self.mouse_por_cima
        self.mouse_por_cima = self.retangulo_base.collidepoint(posicao_mouse)

        if self.mouse_por_cima and not estava_por_cima:
            if SOM_HOVER:
                SOM_HOVER.play()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.mouse_por_cima:
                self.pressionado = True
                self.escala_alvo = 0.90
                self.opacidade_flash = 180

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.pressionado and self.mouse_por_cima:
                if SOM_CLIQUE:
                    SOM_CLIQUE.play()
                self.acao_clique()
            self.pressionado = False

    def atualizar(self, variacao_tempo):
        if self.pressionado:
            self.escala_alvo = 0.90
        elif self.mouse_por_cima:
            self.escala_alvo = 1.08
        else:
            self.escala_alvo = 1.0

        self.escala_atual += (self.escala_alvo - self.escala_atual) * min(1, variacao_tempo * 12)

        if self.opacidade_flash > 0:
            self.opacidade_flash = max(0, self.opacidade_flash - variacao_tempo * 400)

    def desenhar(self, tela):
        largura_redimensionada = int(self.retangulo_base.width * self.escala_atual)
        altura_redimensionada = int(self.retangulo_base.height * self.escala_atual)
        retangulo_render = pygame.Rect(0, 0, largura_redimensionada, altura_redimensionada)
        retangulo_render.center = self.retangulo_base.center

        if self.pressionado:
            cor_atual = self.cor_click
        elif self.mouse_por_cima:
            cor_atual = self.cor_hover
        else:
            cor_atual = self.cor_normal

        retangulo_sombra = retangulo_render.copy()
        retangulo_sombra.move_ip(0, 6)
        pygame.draw.rect(tela, (15, 60, 25), retangulo_sombra, border_radius=6)

        pygame.draw.rect(tela, cor_atual, retangulo_render, border_radius=6)
        pygame.draw.rect(tela, PRETO, retangulo_render, width=4, border_radius=6)

        borda_interna = retangulo_render.inflate(-8, -8)
        pygame.draw.rect(tela, (255, 255, 255, 60), borda_interna, width=2, border_radius=4)

        if self.opacidade_flash > 0:
            superficie_flash = pygame.Surface((retangulo_render.width, retangulo_render.height), pygame.SRCALPHA)
            pygame.draw.rect(superficie_flash, (255, 255, 255, int(self.opacidade_flash)), superficie_flash.get_rect(), border_radius=6)
            tela.blit(superficie_flash, retangulo_render.topleft)

        superficie_texto_sombra = FONTE_BOTAO.render(self.texto, True, PRETO)
        posicao_texto_sombra = superficie_texto_sombra.get_rect(center=(retangulo_render.centerx + 2, retangulo_render.centery + 2))
        tela.blit(superficie_texto_sombra, posicao_texto_sombra)

        superficie_texto_principal = FONTE_BOTAO.render(self.texto, True, BRANCO)
        posicao_texto_principal = superficie_texto_principal.get_rect(center=retangulo_render.center)
        tela.blit(superficie_texto_principal, posicao_texto_principal)


# Classe Fundo GameOver (campo escurecido para a tela de derrota)
class FundoGameOver:
    def __init__(self):
        self.faixa_altura = 40

    def atualizar(self, variacao_tempo):
        pass

    def desenhar(self, tela, tempo_decorrido):
        num_faixas = ALTURA // self.faixa_altura + 1
        for i in range(num_faixas):
            cor = VERDE_CAMPO_1 if i % 2 == 0 else VERDE_CAMPO_2
            pygame.draw.rect(
                tela, cor,
                (0, i * self.faixa_altura, LARGURA, self.faixa_altura)
            )

        espessura = 6
        pygame.draw.rect(tela, BRANCO, (20, 20, LARGURA - 40, ALTURA - 40), espessura)
        pygame.draw.line(tela, BRANCO, (20, ALTURA // 2), (LARGURA - 20, ALTURA // 2), espessura)
        pygame.draw.circle(tela, BRANCO, (LARGURA // 2, ALTURA // 2), 55, espessura)
        pygame.draw.circle(tela, BRANCO, (LARGURA // 2, ALTURA // 2), 4)
        pygame.draw.rect(tela, BRANCO, (LARGURA // 2 - 110, 20, 220, 70), espessura)
        pygame.draw.rect(tela, BRANCO, (LARGURA // 2 - 110, ALTURA - 90, 220, 70), espessura)

        # Camada escura
        velatura = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        velatura.fill((0, 0, 0, 160))
        tela.blit(velatura, (0, 0))


# Classe Titulo Game Over
class TituloGameOver:

    def __init__(self, texto_linha1, texto_linha2, posicao_y):
        self.linha1 = texto_linha1
        self.linha2 = texto_linha2
        self.posicao_y = posicao_y

    def atualizar(self, variacao_tempo):
        pass

    def _render_linha(self, texto, fonte, posicao_y, tela):
        superficie_base = fonte.render(texto, True, VERMELHO)
        superficie_contorno = fonte.render(texto, True, PRETO)
        retangulo_texto = superficie_base.get_rect(center=(LARGURA // 2, posicao_y))

        for deslocamento_x, deslocamento_y in [(-3, 0), (3, 0), (0, -3), (0, 3), (-3, -3), (3, 3), (-3, 3), (3, -3)]:
            tela.blit(superficie_contorno, retangulo_texto.move(deslocamento_x, deslocamento_y))
        tela.blit(superficie_base, retangulo_texto)

    def desenhar(self, tela):
        self._render_linha(self.linha1, FONTE_TITULO, self.posicao_y, tela)
        self._render_linha(self.linha2, FONTE_TITULO, self.posicao_y + 56, tela)


# Classe Game Over (Tela exibida quando o jogador perde)
class GameOver:

    def __init__(self, app, pontuacao=0):
        self.app = app
        self.pontuacao = pontuacao
        self.background = FundoGameOver()
        self.titulo = TituloGameOver("GAME", "OVER", 160)

        largura_botao, altura_botao = 260, 64
        x_centro = LARGURA // 2 - largura_botao // 2

        self.botao_tentar_novamente = Botao(
            x_centro, 340, largura_botao, altura_botao,
            "REINICIAR", self.clicou_tentar_novamente,
            cor_normal=VERDE_BOTAO, cor_hover=VERDE_BOTAO_HOVER, cor_click=VERDE_BOTAO_CLICK
        )

        self.botao_sair = Botao(
            x_centro, 430, largura_botao, altura_botao,
            "SAIR", self.clicou_sair,
            cor_normal=(160, 40, 40), cor_hover=(210, 60, 60), cor_click=(110, 25, 25)
        )

        self.cronometro = 0.0

    def clicou_tentar_novamente(self):
        pygame.time.delay(200)
        self.app.iniciar_jogo()

    def clicou_sair(self):
        pygame.time.delay(200)
        self.app.sair()

    def gerenciar_evento(self, evento):
        self.botao_tentar_novamente.gerenciar_evento(evento)
        self.botao_sair.gerenciar_evento(evento)

    def atualizar(self, variacao_tempo):
        self.cronometro += variacao_tempo
        self.background.atualizar(variacao_tempo)
        self.titulo.atualizar(variacao_tempo)
        self.botao_tentar_novamente.atualizar(variacao_tempo)
        self.botao_sair.atualizar(variacao_tempo)

    def desenhar(self, tela):
        self.background.desenhar(tela, self.cronometro)
        self.titulo.desenhar(tela)

        texto_pontuacao = FONTE_PONTUACAO.render(f"Pontuação: {self.pontuacao}", True, BRANCO)
        contorno_pontuacao = FONTE_PONTUACAO.render(f"Pontuação: {self.pontuacao}", True, PRETO)
        retangulo_pontuacao = texto_pontuacao.get_rect(center=(LARGURA // 2, 280))

        for deslocamento_x, deslocamento_y in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            tela.blit(contorno_pontuacao, retangulo_pontuacao.move(deslocamento_x, deslocamento_y))
        tela.blit(texto_pontuacao, retangulo_pontuacao)

        self.botao_tentar_novamente.desenhar(tela)
        self.botao_sair.desenhar(tela)