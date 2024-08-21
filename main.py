# Importação e inicialização
import pygame
from random import randint

pygame.init()

# Constantes de jogo
LARGURA_TELA = 500
ALTURA_TELA = 700
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Hashy Bird')

IMAGEM_CANO = pygame.transform.scale(pygame.image.load('Arquivos/Cano.png'), (32 * 4, 160 * 4))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load('Arquivos/base.png'))
IMAGEM_BG = pygame.transform.scale2x(pygame.image.load('Arquivos/bg.png'))
IMAGENS_PASSARO = [pygame.transform.scale2x(pygame.image.load('Arquivos/HashBird (1).png')),
                   pygame.transform.scale2x(pygame.image.load('Arquivos/HashBird (2).png')),
                   pygame.transform.scale2x(pygame.image.load('Arquivos/HashBird (3).png'))]

IMAGENS_PASSARO = [pygame.transform.scale2x(img) for img in IMAGENS_PASSARO]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('Console', 30, True)


class Passaro:
    # Atributos de classe do pássaro
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAX = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIM = 5

    # Construtor do pássaro
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.indice_imagem = 0
        self.imagem = self.IMGS[0]
    
    # Pular do pássaro
    def pular(self) -> None:
        self.velocidade = -3
        self.tempo = 0
        self.altura = self.y
    
    # Movimentar o pássaro
    def mover(self) -> None:
        self.tempo += 1
        deslocamento = self.velocidade * self.tempo + 0.25 * self.tempo ** 2
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento
        if deslocamento < 0 or self.y < self.altura + 50:
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
    
    # Desenhar o pássaro na tela
    def desenhar(self, superficie) -> None:
        self.indice_imagem += 1

        if self.indice_imagem < self.TEMPO_ANIM:
            self.imagem = self.IMGS[0]
        elif self.indice_imagem < self.TEMPO_ANIM * 2:
            self.imagem = self.IMGS[1]
        elif self.indice_imagem < self.TEMPO_ANIM * 3:
            self.imagem = self.IMGS[2]
        elif self.indice_imagem <= self.TEMPO_ANIM * 4:
            self.imagem = self.IMGS[1]
        elif self.indice_imagem > self.TEMPO_ANIM * 4:
            self.imagem = self.IMGS[0]
            self.indice_imagem = 0
        
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.indice_imagem = self.TEMPO_ANIM * 2
        
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_canto = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_canto)
        superficie.blit(imagem_rotacionada, retangulo.topleft)

    # Máscara de colisão
    def pegar_mascara(self) -> pygame.mask.Mask:
        return pygame.mask.from_surface(self.imagem)


class Cano:
    # Atributos de classe do cano
    DISTANCIA = 200
    VELOCIDADE = 5

    # Construtor do cano
    def __init__(self, x) -> None:
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.IMG_TOPO = IMAGEM_CANO
        self.IMG_BASE = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.passou = False
        self.definir_altura()
    
    # Definir as posições y do cano
    def definir_altura(self) -> None:
        self.altura = randint(25, 350)
        self.pos_base = self.altura - self.IMG_BASE.get_height()
        self.pos_topo = self.altura + self.DISTANCIA
    
    # Movimentar o cano
    def mover(self) -> None:
        self.x -= self.VELOCIDADE
    
    # Desenhar o cano na tela
    def desenhar(self, tela: pygame.Surface) -> None:
        tela.blit(self.IMG_TOPO, (self.x, self.pos_topo))
        tela.blit(self.IMG_BASE, (self.x, self.pos_base))
    
    # Colidir o cano com um pássaro
    def colidir(self, passaro: Passaro) -> bool:
        mascara_passaro = passaro.pegar_mascara()
        mascara_topo = pygame.mask.from_surface(self.IMG_TOPO)
        mascara_base = pygame.mask.from_surface(self.IMG_BASE)
        
        dist_topo = (self.x - passaro.x, self.pos_topo - int(passaro.y))
        dist_base = (self.x - passaro.x, self.pos_base - int(passaro.y))

        sobre_topo = mascara_passaro.overlap(mascara_topo, dist_topo)
        sobre_base = mascara_passaro.overlap(mascara_base, dist_base)
        return True if sobre_topo or sobre_base else False


class Chao:
    # Atributos de classe do chão
    VELOCIDADE = -5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    # Construtor do chão
    def __init__(self, y) -> None:
        self.y = y
        self.xchao1 = 0
        self.xchao2 = self.LARGURA
    
    # Movimentar o chão
    def mover(self) -> None:
        self.xchao1 += self.VELOCIDADE
        self.xchao2 += self.VELOCIDADE

        if self.xchao1 + self.LARGURA < 0:
            self.xchao1 = self.xchao2 + self.LARGURA
        if self.xchao2 + self.LARGURA < 0:
            self.xchao2 = self.xchao1 + self.LARGURA
    
    # Desenhar o chão na tela
    def desenhar(self, tela) -> None:
        tela.blit(self.IMAGEM, (self.xchao1, self.y))
        tela.blit(self.IMAGEM, (self.xchao2, self.y))


# Desenhar os objetos na tela
def desenhar_tela(tela, passaros, canos, chao, pontos) -> None:
    tela.blit(IMAGEM_BG, (0, -150))
    for passaro in passaros:
        passaro.desenhar(tela)
        # pygame.draw.rect(tela, (0, 0, 0), ((passaro.x, passaro.y), (passaro.imagem.get_width(), passaro.imagem.get_width())), 2)
    for cano in canos:
        cano.desenhar(tela)
        # pygame.draw.rect(tela, (0, 0, 0), ((cano.x, cano.pos_topo), (cano.IMG_TOPO.get_width(), cano.IMG_TOPO.get_height())), 2)
        # pygame.draw.rect(tela, (0, 0, 0), ((cano.x, cano.pos_base), (cano.IMG_BASE.get_width(), cano.IMG_BASE.get_height())), 2)
    chao.desenhar(tela)
    texto_pontuacao = FONTE_PONTOS.render(f'Pontuação: {pontos}', True, (255, 255, 255), (100, 100, 100))
    tela.blit(texto_pontuacao, (LARGURA_TELA - 5 - texto_pontuacao.get_width(), 10))
    pygame.display.flip()


# Áudio
musica = pygame.mixer.music.load('Arquivos/Música.wav')
pygame.mixer.music.set_volume(0.5)
som = pygame.mixer.Sound('Arquivos/moeda_som.wav')
som.set_volume(0.125)


# Função principal
def main() -> None:
    passaros = [Passaro(120, 250)]
    canos = [Cano(700)]
    chao = Chao(640)

    TQPS = 120
    relogio = pygame.time.Clock()

    pontos = 0

    pygame.mixer.music.play(-1)
    rodando = True
    # Loop principal
    while rodando:
        relogio.tick(TQPS)
        # Checagem de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or len(passaros) == 0:
                rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                for passaro in passaros:
                    passaro.pular()
        
        # Mover os objetos
        for passaro in passaros:
            passaro.mover()
        
        canos_removidos = list()
        adicionar_cano = False

        chao.mover()

        for cano in canos:
            for passaro in passaros:
                if cano.colidir(passaro):
                    passaros.remove(passaro)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.IMG_BASE.get_width() < 0:
                canos_removidos.append(cano)
        if adicionar_cano:
            pontos += 1
            som.play()
            canos.append(Cano(700))
        for cano in canos_removidos:
            canos.remove(cano)
        
        for passaro in passaros:
            if passaro.y + passaro.imagem.get_height() > chao.y or passaro.y < 0:
                passaros.remove(passaro)
    
        desenhar_tela(tela, passaros, canos, chao, pontos)
    
    pygame.time.delay(1000)


# Execução e finalização do programa
try:
    if __name__ == '__main__':
        main()
except Exception as exc:
    print(f'Uma exceção ocorreu! Classe: {exc.__class__}')
finally:
    pygame.quit()
