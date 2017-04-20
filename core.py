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


class MatrizAux(dict):

    _dicionario = {}

    def __setitem__(self, xy, valor):
        x = xy[0]
        y = xy[1]

        if x not in self._dicionario:
            self._dicionario[x] = {}
        self._dicionario[x][y] = valor

    def __getitem__(self, xy):
        x = xy[0]
        y = xy[1]
        return self._dicionario[x][y]


class Filtros(object):
    """
    Filtros que podem ser aplicados na imagem.
    """

    # matriz_filtro = [
    #     [1.5/18, 2.0/18, 1.5/18],
    #     [2.0/18, 4.0/18, 2.0/18],
    #     [1.5/18, 2.0/18, 1.5/18],
    # ]

    # matriz_filtro = [
    #     [1.0/94, 2.0/94, 4.0/94, 2.0/94, 1.0/94],
    #     [2.0/94, 4.0/94, 8.0/94, 4.0/94, 2.0/94],
    #     [4.0/94, 8.0/94, 10.0/94, 8.0/94, 4.0/94],
    #     [2.0/94, 4.0/94, 8.0/94, 4.0/94, 2.0/94],
    #     [1.0/94, 2.0/94, 4.0/94, 2.0/94, 1.0/94],
    # ]

    matriz_filtro = [
        [ 0, -1,  0],
        [-1,  4, -1],
        [ 0, -1,  0],
    ]

    # matriz_filtro = [
    #     [-1, -1, -1, -1, -1],
    #     [-1,  1,  1,  1, -1],
    #     [-1,  1,  8,  1, -1],
    #     [-1,  1,  1,  1, -1],
    #     [-1, -1, -1, -1, -1],
    # ]

    def __init__(self, imagem, matriz_filtro=None):
        """
        """
        self.imagem = imagem
        self.dimensao_matriz_filtro = len(self.matriz_filtro)

    def _get_matriz_aux(self):
        """
        """
        matriz = MatrizAux()
        ultima_linha = self.imagem.imagem.width
        ultima_coluna = self.imagem.imagem.height

        for y in range(ultima_coluna):
            matriz[0, y] = self.imagem.pixels[0, y]
            matriz[ultima_linha-1, y] = self.imagem.pixels[ultima_linha-1, y]

        for x in range(ultima_linha):
            matriz[x, 0] = self.imagem.pixels[x, 0]
            matriz[x, ultima_coluna-1] = self.imagem.pixels[x, ultima_coluna-1]

        return matriz

    def _get_novo_valor(self,
                        matriz_imagem=None,
                        inverter_indice_filtro=False,
                        sentido_percorrer_matriz='horizontal'):
        """
        """
        matriz_imagem = matriz_imagem or self.imagem.pixels

        # Define a ordem que os indices da matriz de filtro serão acessados.
        indice_matriz_filtro = range(self.dimensao_matriz_filtro)
        if inverter_indice_filtro:
            indice_matriz_filtro.reverse()

        # Limita a aplicação da técnica para pontos que possuem vizinhos.
        # (Desconsidera pixels nas bordas).
        # Ex: 7 / 2 = 3.
        # 3 é a quantidade de pixels da borda da matriz até o centro.
        tamanho_borda = self.dimensao_matriz_filtro / 2

        # Busca os pares de pontos (x, y) da imagem, exceto os das bordas.
        pontos_matriz = self.imagem._get_xy(
            x_inicio=tamanho_borda,
            y_inicio=tamanho_borda,
            x_final=5,
            y_final=3,
            #x_final=self.imagem.imagem.width - tamanho_borda,
            #y_final=self.imagem.imagem.height - tamanho_borda,
            sentido=sentido_percorrer_matriz
        )

        # Percorre os pixels da imagem.
        for x, y in pontos_matriz:
            soma = 0
            # Percorre os vizinhos do pixel no eixo x.
            for indice_i in range(self.dimensao_matriz_filtro):
                # Percorre os vizinhos do pixels no eixo y.
                for indice_j in indice_matriz_filtro:

                    if sentido_percorrer_matriz == 'vertical':
                        i = indice_j
                        j = indice_i
                    else:
                        i = indice_i
                        j = indice_j

                    x_pixel = x - tamanho_borda + i
                    y_pixel = y - tamanho_borda + j

                    # Pega um vizinho do pixel (x, y).
                    pixels = matriz_imagem[x_pixel, y_pixel]

                    # Faz a multiplicação do pixel vizinho pelo indice da
                    # matriz filtro.
                    print 'Pixel: (%s, %s) - Vizinho: (%s, %s) - matriz_filtro: (%s, %s) = %s' % (
                        x, y, x_pixel, y_pixel, i, j, self.matriz_filtro[i][j]
                    )

                    soma += pixels[0] * self.matriz_filtro[i][j]

            soma = int(soma)
            if soma < 0:
                soma = 0
            elif soma > 255:
                soma = 255
            yield (x, y, int(soma))

    def correlacao(self):
        """
        Aplica o filtro de correlação.
        """
        for x, y, valor in self._get_novo_valor():
            self.imagem.pixels[x, y] = (valor, valor, valor)

    def convolucao(self):
        """
        Aplica o filtro de convolução.
        """
        valores = self._get_novo_valor(matriz, inverter_indice_filtro=True)
        for x, y, valor in valores:
            self.imagem.pixels[x, y] = (valor, valor, valor)

    def passa_alta(self):
        """
        Aplica o filtro de passa alta.
        """
        # Cria uma matriz auxiliar para ser utilizada como cópia da imagem.
        #matriz = self._get_matriz_aux()
        matriz = MatrizAux()
        matriz[0,0] = 10
        matriz[0,1] = 10
        matriz[0,2] = 10
        matriz[0,3] = 10
        matriz[0,4] = 10
        matriz[0,5] = 10
        matriz[1,0] = 10
        matriz[1,1] = 0
        matriz[1,2] = 10
        matriz[1,3] = 20
        matriz[1,4] = 10
        matriz[2,0] = 10
        matriz[2,1] = 10
        matriz[2,2] = 10
        matriz[2,3] = 10
        matriz[2,4] = 10

        #http://www.dpi.inpe.br/~carlos/Academicos/Cursos/Pdi/pdi_filtros.htm
        # Faz a passada horizontalmente.
        for x, y, valor in self._get_novo_valor(matriz_imagem=matriz):
            matriz[x, y] = (valor, valor, valor)

        from IPython import embed; embed()
        # Faz a passada verticalmente.
        valores = self._get_novo_valor(
            matriz_imagem=matriz,
            sentido_percorrer_matriz='vertical'
        )
        for x, y, valor in valores:
            self.imagem.pixels[x, y] = (valor, valor, valor)
