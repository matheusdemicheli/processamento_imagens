#-*- coding: utf-8 -*-
"""
Tratamento de uma imagem.
"""
from collections import defaultdict
from decimal import Decimal
from PIL import Image
from utils import MatrizAux


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

    def _get_xy(self, x_inicio=0, y_inicio=0, x_final=None, y_final=None,
                sentido='horizontal'):
        """
        Retorna um generator das coordenadas (x, y) da imagem.
        """
        x_final = x_final or self.imagem.width
        y_final = y_final or self.imagem.height

        if sentido == 'horizontal':
            for x in range(x_inicio, x_final):
                for y in range(y_inicio, y_final):
                    yield (x, y)
        else:
            for y in range(y_inicio, y_final):
                for x in range(x_inicio, x_final):
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

    # mascara = [
    #     [1.5/18, 2.0/18, 1.5/18],
    #     [2.0/18, 4.0/18, 2.0/18],
    #     [1.5/18, 2.0/18, 1.5/18],
    # ]

    # mascara = [
    #     [ 0, -1,  0],
    #     [-1,  4, -1],
    #     [ 0, -1,  0],
    # ]

    mascara = [
        [-1, -1, -1, -1, -1],
        [-1,  1,  1,  1, -1],
        [-1,  1,  8,  1, -1],
        [-1,  1,  1,  1, -1],
        [-1, -1, -1, -1, -1],
    ]

    def __init__(self, imagem):
        """
        Inicialização da classe.
        """
        self.imagem = imagem
        self.dimensao_mascara = len(self.mascara)

    def __get_matriz_aux(self):
        """
        Retorna uma matriz de pixels auxiliar a imagem original.
        Pré popula a matriz com os valores dos pixels das bordas (pixels que
        não serão aplicados as filtragens).
        """
        matriz = MatrizAux()

        ultima_linha = self.imagem.imagem.width - 1
        ultima_coluna = self.imagem.imagem.height - 1
        tamanho_borda = self.dimensao_mascara / 2

        for y in range(self.imagem.imagem.height):
            for x in range(tamanho_borda):
                matriz[x, y] = self.imagem.pixels[x, y]
                matriz[ultima_linha-x, y] = self.imagem.pixels[ultima_linha-x, y]

        for x in range(self.imagem.imagem.width):
            for y in range(tamanho_borda):
                matriz[x, y] = self.imagem.pixels[x, y]
                matriz[x, ultima_coluna-y] = self.imagem.pixels[x, ultima_coluna-y]

        return matriz

    def _get_indices_mascara(self, sentido):
        """
        Retorna os indices de acesso da matriz de filtro.
        """
        indices = []

        # Define a ordem que os indices da matriz de filtro serão acessados.
        indice_mascara = range(self.dimensao_mascara)

        if sentido == 'horizontal':
            for i in range(self.dimensao_mascara):
                for j in indice_mascara:
                    indices.append((i, j))
        else:
            for j in indice_mascara:
                for i in range(self.dimensao_mascara):
                    indices.append((i, j))
        return indices

    def _aplicar_mascara(self,
                         matriz_imagem=None,
                         inverter_indice_filtro=False,
                         sentido_percorrer_matriz='horizontal'):
        """
        Aplica a máscara do filtro para a imagem.
        """
        if matriz_imagem is None:
            matriz_imagem = self.imagem.pixels

        # Limita a aplicação da técnica para pontos que possuem vizinhos.
        # (Desconsidera pixels nas bordas).
        # Ex: 7 / 2 = 3.
        # 3 é a quantidade de pixels da borda da matriz até o centro.
        tamanho_borda = self.dimensao_mascara / 2

        # Busca os pares de pontos (x, y) da imagem, exceto os das bordas.
        pontos_matriz = self.imagem._get_xy(
            x_inicio=tamanho_borda,
            y_inicio=tamanho_borda,
            x_final=self.imagem.imagem.width - tamanho_borda,
            y_final=self.imagem.imagem.height - tamanho_borda,
            sentido=sentido_percorrer_matriz
        )

        indice_mascara = self._get_indices_mascara(sentido_percorrer_matriz)
        if inverter_indice_filtro:
            indice_mascara.reverse()

        # Percorre os pixels da imagem.
        for x, y in pontos_matriz:
            soma = 0
            for x_filtro, y_filtro in indice_mascara:
                # Pega o valor que deve ser aplicado da matriz de filtro.
                valor_mascara = self.mascara[x_filtro][y_filtro]
                # Pega um vizinho do pixel (x, y).
                x_vizinho = x - tamanho_borda + x_filtro
                y_vizinho = y - tamanho_borda + y_filtro
                pixel_vizinho = matriz_imagem[x_vizinho, y_vizinho][0]
                # Multiplica o valor do pixel vizinho pelo valor do filtro.
                soma += pixel_vizinho * valor_mascara

            soma = int(soma)
            if soma < 0:
                soma = 0
            elif soma > 255:
                soma = 255
            yield (x, y, soma)

    def correlacao(self):
        """
        Aplica o filtro de correlação.
        """
        for x, y, valor in self._aplicar_mascara():
            self.imagem.pixels[x, y] = (valor, valor, valor)

    def convolucao(self):
        """
        Aplica o filtro de convolução.
        """
        valores = self._aplicar_mascara(inverter_indice_filtro=True)
        for x, y, valor in valores:
            self.imagem.pixels[x, y] = (valor, valor, valor)

    def passa_alta(self):
        """
        Aplica o filtro de passa alta.
        """
        # Aplica a máscara horizontalmente.
        matriz = self.__get_matriz_aux()
        for x, y, valor in self._aplicar_mascara():
            matriz[x, y] = (valor, valor, valor)

        # Aplica a máscara verticalmente.
        valores = self._aplicar_mascara(
            matriz_imagem=matriz,
            sentido_percorrer_matriz='vertical'
        )
        for x, y, valor in valores:
            self.imagem.pixels[x, y] = (valor, valor, valor)
