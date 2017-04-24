#-*- coding: utf-8 -*-
"""
Funcionalidades específicas.
"""
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout


class Janela(FloatLayout):
    """
    Janela base para carregar/salvar uma imagem.
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
    titulo = u'Máscara'


class MatrizAux(object):
    """
    Matriz que imita o comportamento da matriz de pixels do PIL (PixelAccess).
    """

    def __init__(self):
        """
        Definição do dicionário.
        """
        self._dicionario = {}

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
