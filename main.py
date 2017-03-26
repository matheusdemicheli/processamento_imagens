#-*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.image import Image
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from core import Imagem
from menus import MenuImagemDropDown


class MainLayout(BoxLayout):
    """
    Layout principal da aplicação.
    """

    caminho_temp = 'imagens/temp.jpg'
    imagem = ObjectProperty()

    def __init__(self, *args, **kwargs):
        """
        Definição de atributos.
        """
        super(MainLayout, self).__init__(*args, **kwargs)
        self.widgets_dinamicos = []
        self.imagem_core = None
        self.menu_imagem = MenuImagemDropDown()

    def carregar_imagem(self, caminho_imagem):
        """
        Carrega uma imagem.
        """
        self.imagem.source = caminho_imagem
        self.imagem_core = Imagem(caminho_imagem)
        self.imagem.reload()

    def salvar_imagem(self, caminho_imagem):
        """
        Salva a imagem.
        """
        self.imagem_core.salvar(novo_caminho_imagem=caminho_imagem)

    def limpar(self):
        """
        Remove os widgets adicionados dinâmicamente e remove a imagem.
        """
        for widget in self.widgets_dinamicos:
            self.remove_widget(widget)
        self.imagem.source = ''
        self.imagem.reload()
        self.imagem_core = None

    def mostrar_imagem_cinza(self):
        """
        Mostra a imagem em escala de cinza.
        """
        self.imagem_core.converter_escala_cinza()
        self.salvar_imagem(self.caminho_temp)
        self.carregar_imagem(self.caminho_temp)

    def mostrar_imagem_equalizada(self):
        """
        Mostra a imagem equalizada.
        """
        self.imagem_core.equalizar_imagem()
        self.salvar_imagem(self.caminho_temp)
        self.carregar_imagem(self.caminho_temp)

    def mostrar_histograma(self):
        """
        Mostra o histograma da imagem.
        """
        histograma = self.imagem_core.get_histograma()

        graph = Graph(
            xlabel='Tom de Cinza',
            ylabel='Quantidade de tons',
            padding=5,
            xmin=0,
            xmax=max(histograma.keys()),
            ymin=0,
            ymax=max(histograma.values())
        )
        plot = MeshLinePlot()
        plot.points = histograma.items()
        graph.add_plot(plot)
        self.widgets_dinamicos.append(graph)
        self.add_widget(graph)


class MainApp(App):
    """
    Aplicação.
    """

    def build(self):
        """
        Carrega a imagem na tela.
        """
        self.main_layout = MainLayout()
        return self.main_layout


if __name__ == '__main__':
    MainApp().run()
