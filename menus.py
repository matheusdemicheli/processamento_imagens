#-*- coding: utf-8 -*-
from kivy.uix.dropdown import DropDown
from utils import LoadDialog, SaveDialog


class Menu(DropDown):
    """
    Classe base de Menus.
    """

    def select(self, opcao, *args, **kwargs):
        """
        Executa a função de callback.
        """
        getattr(self, opcao)(*args, **kwargs)
        self.dismiss()


class MenuImagemDropDown(Menu):
    """
    Menu de Imagem.
    """

    def carregar_imagem(self):
        """
        Abre o popup para a escolha de uma nova imagem.
        """
        janela = LoadDialog()
        janela.popup.open()

    def salvar_imagem(self):
        """
        Abre o popup para a escolha do caminho para salvar a imagem.
        """
        janela = SaveDialog()
        janela.popup.open()

    def limpar(self, app):
        """
        Limpa a tela.
        """
        app.main_layout.limpar()

    def mostrar_imagem_cinza(self, app):
        """
        Mostra a imagem em escala de cinza.
        """
        app.main_layout.mostrar_imagem_cinza()

    def mostrar_imagem_equalizada(self, app):
        """
        Mostra a imagem equalizada.
        """
        app.main_layout.mostrar_imagem_equalizada()

    def mostrar_histograma(self, app):
        """
        Mostra o histograma da imagem.
        """
        app.main_layout.mostrar_histograma()


class MenuFiltros(Menu):
    """
    Menu dos filtros.
    """

    def aplicar_filtro(self, app, nome_filtro):
        """
        Aplica o filtro de correlação.
        """
        app.main_layout.aplicar_filtro(nome_filtro=nome_filtro)
