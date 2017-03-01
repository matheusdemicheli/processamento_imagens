#-*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.image import Image

from utils import salvar_imagem_outro_nome


class MainApp(App):
    """
    Aplicação.
    """

    def __init__(self):
        """
        Definição de atributos.
        """
        self.caminho_imagem_original = 'imagens/1.jpg'
        self.caminho_imagem_alterada = 'imagens/2.jpg'
        super(MainApp, self).__init__()

    def build(self):
        """
        Carrega a imagem na tela.
        """
        salvar_imagem_outro_nome(
            nome_original=self.caminho_imagem_original, 
            nome_alterado=self.caminho_imagem_alterada
        )
        return Image(source=self.caminho_imagem_original)


if __name__ == '__main__':
    MainApp().run()
