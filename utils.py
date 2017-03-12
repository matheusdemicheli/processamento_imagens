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
        self.quantidade_pixels = (
            Decimal(self.imagem.height * self.imagem.width)
        )
        super(Imagem, self).__init__(*args, **kwargs)

    def _get_xy(self):
        """
        Retorna um generator das coordenadas (x, y) da imagem.
        """
        for x in range(self.imagem.width):
            for y in range(self.imagem.height):
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

    def get_histograma(self, equalizar=False):
        """
        :return: {tom_cinza: quantidade_pixels, ...}

        Monta o histograma da imagem.
        """
        histograma = defaultdict(lambda: 0)
        for x, y in self._get_xy():
            r, g, b = self.pixels[x, y]
            histograma[r] += 1

        if equalizar:
            histograma_equalizado = {}
            probabilidades = self._get_probabilidades(histograma)
            novos_tons = self._get_novos_tons_cinza(probabilidades)

            for tom_cinza, novo_tom_cinza in novos_tons.items():
                histograma_equalizado[novo_tom_cinza] = histograma[tom_cinza]
            histograma = histograma_equalizado

        return histograma

    def equalizar_escala_cinza(self):
        """
        Equaliza a escala de cinza da imagem através do histograma.
        """
        histograma = self.get_histograma()
        probabilidades = self._get_probabilidades(histograma)
        novos_tons = self._get_novos_tons_cinza(probabilidades)

        for x, y in self._get_xy():
            r, g, b = self.pixels[x, y]
            tom_cinza = novos_tons[r]
            self.pixels[x, y] = (tom_cinza, tom_cinza, tom_cinza)