#-*- coding: utf-8 -*-
"""
Funcionalidades específicas.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


class Janela(FloatLayout):
    """
    Janela base para popups da aplicação.
    """
    titulo = ''

    def __init__(self, *args, **kwargs):
        """
        Configura o Popup.
        """
        super(Janela, self).__init__(*args, **kwargs)
        self.popup = Popup(
            title=self.titulo,
            content=self,
            size_hint=(0.9, 0.9)
        )

    def fechar(self):
        """
        Fecha a janela.
        """
        self.popup.dismiss()


class LoadDialog(Janela):
    """
    Carrega uma imagem.
    """
    titulo = u'Carregar Imagem'

    def carregar(self, app, caminho_arquivo):
        """
        Carrega a imagem em tela.
        """
        app.main_layout.carregar_imagem(caminho_arquivo[0])
        self.fechar()


class SaveDialog(Janela):
    """
    Salva uma imagem.
    """
    titulo = 'Salvar Imagem'

    def salvar(self, app, diretorio, nome):
        """
        Salva uma imagem no disco.
        """
        app.main_layout.salvar_imagem('%s/%s' % (diretorio, nome))
        self.fechar()


class MascaraDialog(Janela):
    """
    Define a máscara que será aplicada sobre a imagem.
    """

    area_mascara = ObjectProperty()
    input_dimensao_mascara = ObjectProperty()
    titulo = u'Defina a máscara para ser aplicada'

    def __init__(self, nome_filtro, *args, **kwargs):
        """
        Guarda o nome do filtro que será aplicado.
        """
        super(MascaraDialog, self).__init__(*args, **kwargs)
        self.nome_filtro = nome_filtro
        self.inputs_matriz_mascara = []
        self.input_dimensao_mascara.bind(text=self._change_dimensao)

    def _change_dimensao(self, instancia, valor):
        """
        Callback para alteração de change no campo da dimensão da máscara.
        Adiciona novos inputs para informar os valores da máscara.
        """
        for input_matriz in self.inputs_matriz_mascara:
            self.area_mascara.remove_widget(input_matriz)

        valor = int(valor) if valor else 0
        if valor and valor > 0:
            self.area_mascara.cols = valor
            for _ in range(valor*valor):
                text_input = TextInput(
                    text="0",
                    #input_filter='float',
                    write_tab=False
                )
                self.inputs_matriz_mascara.append(text_input)
                self.area_mascara.add_widget(text_input)

    def aplicar_mascara(self, app):
        """
        Aplica uma máscara para um determinado filtro.
        """
        self.fechar()

        mascara = Mascara()
        dimensao = int(self.input_dimensao_mascara.text)

        linha = []
        for indice, input_text in enumerate(self.inputs_matriz_mascara, 1):
            linha.append(eval(input_text.text))
            if indice % dimensao == 0:
                mascara.append(linha)
                linha = []

        app.main_layout.aplicar_filtro(
            nome_filtro=self.nome_filtro,
            mascara=mascara
        )



class MatrizAux(object):
    """
    Matriz que imita o comportamento da matriz de pixels do PIL (PixelAccess).
    """

    def __init__(self, *args, **kwargs):
        """
        Definição do dicionário.
        """
        self._dicionario = {}
        super(MatrizAux, self).__init__(*args, **kwargs)

    def __getitem__(self, xy):
        """
        Acessa uma posição da matriz na forma
        matriz[x, y].
        """
        x = xy[0]
        y = xy[1]
        return self._dicionario[x][y]

    def __setitem__(self, xy, valor):
        """
        Seta um valor para a matriz na forma
        matriz[x, y] = valor.
        """
        x = xy[0]
        y = xy[1]

        if x not in self._dicionario:
            self._dicionario[x] = {}
        self._dicionario[x][y] = valor


class PixelAccessAux(MatrizAux):
    """
    Matriz que imita o comportamento da matriz de pixels do PIL (PixelAccess).
    """

    def __init__(self, imagem, mascara, *args, **kwargs):
        """
        Retorna uma matriz de pixels auxiliar a imagem original.
        Pré popula a matriz com os valores dos pixels das bordas (pixels que
        não serão aplicados as filtragens).
        """
        super(PixelAccessAux, self).__init__(*args, **kwargs)

        ultima_linha = imagem.imagem.width - 1
        ultima_coluna = imagem.imagem.height - 1

        for y in range(imagem.imagem.height):
            for x in mascara.range_tamanho_borda:
                self[x, y] = imagem.pixels[x, y]
                self[ultima_linha-x, y] = imagem.pixels[ultima_linha-x, y]

        for x in range(imagem.imagem.width):
            for y in mascara.range_tamanho_borda:
                self[x, y] = imagem.pixels[x, y]
                self[x, ultima_coluna-y] = imagem.pixels[x, ultima_coluna-y]


class Mascara(list):
    """
    Mascara para ser aplicada nos filtros.
    """

    def __init__(self, *args, **kwargs):
        """
        Inicialização da classe.
        """
        self._cache = False
        super(Mascara, self).__init__(*args, **kwargs)

    def __getattr__(self, atributo):
        """
        Calcula valores para serem utilizados.
        """
        if not self._cache:
            self._cache = True
            self.dimensao = len(self)
            self.tamanho_borda = self.dimensao / 2
            self.range_tamanho_borda = range(self.dimensao)
            self.tamanho_mascara = self.dimensao * self.dimensao
        return self.__getattribute__(atributo)
