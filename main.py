#-*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty

from utils import Imagem


class MenuDropDown(DropDown):
    """
    Menu.
    """
    def select(self, id_botao, *args, **kwargs):
        from IPython import embed; embed()
        pass

class MainLayout(BoxLayout):
    """
    Layout principal da aplicação.
    """

    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        self.menu = MenuDropDown()
        self.imagem = Image()

    def mostrar_imagem_cinza(self):
        """
        Mostra a imagem e escala de cinza.
        """
        self.imagem.converter_escala_cinza()
        self.imagem.salvar('imagens/cinza.jpg')
        return Image(source='imagens/cinza.jpg')

    def mostrar_imagem_equalizada(self):
        """
        Mostra a imagem equalizada.
        """
        self.imagem.converter_escala_cinza()
        self.imagem.equalizar_escala_cinza()
        self.imagem.salvar('imagens/equalizado.jpg')
        return Image(source='imagens/equalizado.jpg')

    def mostrar_histograma(self):
        """
        Mostra o histograma da imagem.
        """
        histograma = self.imagem.get_histograma(equalizar=True)

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
        return graph


class MainApp(App):
    """
    Aplicação.
    """
    def build(self):
        """
        Carrega a imagem na tela.
        """
        return MainLayout()


if __name__ == '__main__':
    MainApp().run()
