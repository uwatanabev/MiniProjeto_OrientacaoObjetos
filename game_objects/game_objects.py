import pygame as pg
import sys  # Importando sys para usar sys.exit()
from random import randrange

vetor2 = pg.math.Vector2

class Cobra:
    def __init__(self, jogo):
        self.jogo = jogo
        self.tamanho = jogo.TAMANHO_TILE
        self.rect = pg.rect.Rect([0, 0, jogo.TAMANHO_TILE - 2, jogo.TAMANHO_TILE - 2])
        self.faixa = (self.tamanho // 2, self.jogo.TAMANHO_TELA - self.tamanho // 2, self.tamanho)
        self.rect.center = self.obter_posicao_aleatoria()
        self.direcao = vetor2(0, 0)
        self.atraso_passo = 100  # milissegundos
        self.tempo = 0
        self.comprimento = 1
        self.segmentos = []
        self.direcoes = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
        
    def controlar(self, evento):
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_w and self.direcoes[pg.K_w]:
                self.direcao = vetor2(0, -self.tamanho)
                self.direcoes[pg.K_w] = 1
                self.direcoes[pg.K_s] = 0
                self.direcoes[pg.K_a] = 1
                self.direcoes[pg.K_d] = 1

            if evento.key == pg.K_s and self.direcoes[pg.K_s]:
                self.direcao = vetor2(0, self.tamanho)
                self.direcoes[pg.K_w] = 0
                self.direcoes[pg.K_s] = 1
                self.direcoes[pg.K_a] = 1
                self.direcoes[pg.K_d] = 1

            if evento.key == pg.K_a and self.direcoes[pg.K_a]:
                self.direcao = vetor2(-self.tamanho, 0)
                self.direcoes[pg.K_w] = 1
                self.direcoes[pg.K_s] = 1
                self.direcoes[pg.K_a] = 1
                self.direcoes[pg.K_d] = 0

            if evento.key == pg.K_d and self.direcoes[pg.K_d]:
                self.direcao = vetor2(self.tamanho, 0)
                self.direcoes[pg.K_w] = 1
                self.direcoes[pg.K_s] = 1
                self.direcoes[pg.K_a] = 0
                self.direcoes[pg.K_d] = 1

    def delta_tempo(self):
        tempo_atual = pg.time.get_ticks()
        if tempo_atual - self.tempo > self.atraso_passo:
            self.tempo = tempo_atual
            return True
        return False

    def obter_posicao_aleatoria(self):
        return [randrange(*self.faixa), randrange(*self.faixa)]

    def verificar_bordas(self):
        if self.rect.left < 0 or self.rect.right > self.jogo.TAMANHO_TELA:
            self.jogo.novo_jogo()
        if self.rect.top < 0 or self.rect.bottom > self.jogo.TAMANHO_TELA:
            self.jogo.novo_jogo()

    def verificar_comida(self):
        if self.rect.center == self.jogo.comida.rect.center:
            self.jogo.comida.rect.center = self.obter_posicao_aleatoria()
            self.comprimento += 1

    def verificar_auto_ataque(self):
        if len(self.segmentos) != len(set(segmento.center for segmento in self.segmentos)):
            self.jogo.novo_jogo()

    def mover(self):
        if self.delta_tempo():
            self.rect.move_ip(self.direcao)
            self.segmentos.append(self.rect.copy())
            self.segmentos = self.segmentos[-self.comprimento:]

    def atualizar(self):
        self.verificar_auto_ataque()
        self.verificar_bordas()
        self.verificar_comida()
        self.mover()

    def desenhar(self):
        [pg.draw.rect(self.jogo.tela, 'green', segmento) for segmento in self.segmentos]


class Comida:
    def __init__(self, jogo):
        self.jogo = jogo
        self.tamanho = jogo.TAMANHO_TILE
        self.rect = pg.rect.Rect([0, 0, jogo.TAMANHO_TILE - 2, jogo.TAMANHO_TILE - 2])
        self.rect.center = self.jogo.cobra.obter_posicao_aleatoria()

    def desenhar(self):
        pg.draw.rect(self.jogo.tela, 'red', self.rect)


class Jogo:
    def __init__(self):
        pg.init()
        self.TAMANHO_TELA = 1000
        self.TAMANHO_TILE = 50
        self.tela = pg.display.set_mode([self.TAMANHO_TELA] * 2)
        self.relogio = pg.time.Clock()
        self.novo_jogo()

    def desenhar_grade(self):
        [pg.draw.line(self.tela, [50] * 3, (x, 0), (x, self.TAMANHO_TELA))
                                             for x in range(0, self.TAMANHO_TELA, self.TAMANHO_TILE)]
        [pg.draw.line(self.tela, [50] * 3, (0, y), (self.TAMANHO_TELA, y))
                                             for y in range(0, self.TAMANHO_TELA, self.TAMANHO_TILE)]

    def novo_jogo(self):
        self.cobra = Cobra(self)
        self.comida = Comida(self)

    def atualizar(self):
        self.cobra.atualizar()
        pg.display.flip()
        self.relogio.tick(60)

    def desenhar(self):
        self.tela.fill('black')
        self.desenhar_grade()
        self.comida.desenhar()
        self.cobra.desenhar()

    def verificar_evento(self):
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                pg.quit()
                sys.exit()  # Aqui usamos sys.exit() para encerrar o jogo
            # controle da cobra
            self.cobra.controlar(evento)

    def rodar(self):
        while True:
            self.verificar_evento()
            self.atualizar()
            self.desenhar()

# Execute o arquivo main.py para jogar!