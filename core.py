#-*- coding: utf-8 -*-
from collections import defaultdict
from decimal import Decimal
from PIL import Image


class Imagem(object):
    """
    Abstração de uma Imagem.
    """

    def __init__(self, caminho_imagem, *args, **kwargs):
        """
        Inicialização da classe.
        """
        self.caminho_imagem = caminho_imagem
        self.imagem = Image.open(caminho_imagem).convert("RGB")
        self.pixels = self.imagem.load()
        self.filtros = Filtros(imagem=self)

        try:
            self.imagem.width, self.imagem.height = self.imagem.size
        except AttributeError:
            pass

        self.quantidade_pixels = (
            Decimal(self.imagem.height * self.imagem.width)
        )
        super(Imagem, self).__init__(*args, **kwargs)

    def _get_xy(self, x_inicio=0, y_inicio=0, x_final=None, y_final=None):
        """
        Retorna um generator das coordenadas (x, y) da imagem.
        """
        x_final = x_final or self.imagem.width
        y_final = y_final or self.imagem.height

        for x in range(x_inicio, x_final):
            for y in range(y_inicio, y_final):
                yield (x, y)

    def _get_probabilidades(self, histograma):
        """
        Retorna as probabilidades para cada nível de cinza do histograma da
        imagem original.
        """
        probabilidades = defaultdict(lambda: 0)
        for tom_cinza, quantidade in histograma.iteritems():
            probabilidades[tom_cinza] = quantidade / self.quantidade_pixels
        return probabilidades

    def _get_novos_tons_cinza(self, probabilidades):
        """
        :return: Um dicionário do tipo: {tom_cinza: novo_tom_cinza}

        Retorna os novos tons de cinza que devem ser aplicados.
        """
        g = defaultdict(lambda: 0)
        probabilidade_acumulada = 0
        for tom_cinza, probabilidade in probabilidades.items():
            probabilidade_acumulada += probabilidade
            novo_tom_cinza = probabilidade_acumulada * 255
            g[tom_cinza] = int(Decimal(novo_tom_cinza).quantize(0))
        return g

    def salvar(self, novo_caminho_imagem=None):
        """
        Salva a imagem.
        """
        caminho_imagem = novo_caminho_imagem or self.caminho_imagem
        self.imagem.save(caminho_imagem)

    def converter_escala_cinza(self):
        """
        Converte uma imagem para escala de cinza.
        """
        for x, y in self._get_xy():
            pixel = self.pixels[x, y]
            r, g, b = self.pixels[x, y]
            tom_cinza = int(0.3 * r + 0.59 * g + 0.11 * b)
            self.pixels[x, y] = (tom_cinza, tom_cinza, tom_cinza)
        return self.pixels

    def get_histograma(self):
        """
        :return: {tom_cinza: quantidade_pixels, ...}

        Retorna o histograma da imagem.
        """
        histograma = defaultdict(lambda: 0)
        for x, y in self._get_xy():
            r, g, b = self.pixels[x, y]
            histograma[r] += 1
        return histograma

    def equalizar_imagem(self):
        """
        Equaliza a imagem em escala de cinza.
        """
        histograma = self.get_histograma()
        probabilidades = self._get_probabilidades(histograma)
        novos_tons = self._get_novos_tons_cinza(probabilidades)

        for x, y in self._get_xy():
            r, g, b = self.pixels[x, y]
            tom_cinza = novos_tons[r]
            self.pixels[x, y] = (tom_cinza, tom_cinza, tom_cinza)

    def aplicar_filtro(self, nome_filtro, *args, **kwargs):
        """
        Aplica um filtro na imagem.
        """
        getattr(self.filtros, nome_filtro)(*args, **kwargs)


class Filtros(object):
    """
    Filtros que podem ser aplicados na imagem.
    """

    matriz_filtro = [
        [1.5/18, 2.0/18, 1.5/18],
        [2.0/18, 4.0/18, 2.0/18],
        [1.5/18, 2.0/18, 1.5/18],
    ]

    # matriz_filtro = [
    #     [1.0/94, 2.0/94, 4.0/94, 2.0/94, 1.0/94],
    #     [2.0/94, 4.0/94, 8.0/94, 4.0/94, 2.0/94],
    #     [4.0/94, 8.0/94, 10.0/94, 8.0/94, 4.0/94],
    #     [2.0/94, 4.0/94, 8.0/94, 4.0/94, 2.0/94],
    #     [1.0/94, 2.0/94, 4.0/94, 2.0/94, 1.0/94],
    # ]

    def __init__(self, imagem):
        """
        """
        self.imagem = imagem

    def correlacao(self, rotacionar_matriz_180=False):
        """
        Aplica o filtro de correlação.
        """
        # Limita a aplicação da técnica para pontos que possuem vizinhos.
        qtd_linhas_espaco = len(self.matriz_filtro) - 2
        generator = self.imagem._get_xy(
            x_inicio=qtd_linhas_espaco,
            y_inicio=qtd_linhas_espaco,
            x_final=self.imagem.imagem.width - qtd_linhas_espaco,
            y_final=self.imagem.imagem.height - qtd_linhas_espaco,
        )

        j = (0, 1, 2)
        if rotacionar_matriz_180:
            j = (2, 1, 0)

        for x, y in generator:
            soma = 0
            for i in range(0, 3):
                soma += self.imagem.pixels[x-1+i, y-1][0] * self.matriz_filtro[i][j[0]]
                soma += self.imagem.pixels[x-1+i, y][0] * self.matriz_filtro[i][j[1]]
                soma += self.imagem.pixels[x-1+i, y+1][0] * self.matriz_filtro[i][j[2]]
            soma = int(soma)
            self.imagem.pixels[x, y] = (soma, soma, soma)

    def convolucao(self):
        """
        Aplica o filtro de convolução.
        """
        self.correlacao(rotacionar_matriz_180=True)
