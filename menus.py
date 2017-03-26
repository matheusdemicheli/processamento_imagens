#-*- coding: utf-8 -*-
from kivy.uix.dropdown import DropDown
from utils import LoadDialog, SaveDialog


class MenuImagemDropDown(DropDown):
    """
    Menu de Imagem.
    """

    def select(self, opcao, *args, **kwargs):
        """
        Executa a função de callback.
        """
        getattr(self, opcao)(*args, **kwargs)
        self.dismiss()

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
