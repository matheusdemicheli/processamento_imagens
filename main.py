#-*- coding: utf-8 -*-
import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.image import Image
from kivy.garden.graph import Graph, MeshLinePlot

from utils import Imagem


class MainApp(App):
    """
    Aplicação.
    """

    caminho_imagem = 'imagens/teste.jpg'

    def __init__(self, *args, **kwargs):
        """
        Definição de atributos.
        """
        self.imagem = Imagem(self.caminho_imagem)
        super(MainApp, self).__init__(*args, **kwargs)

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
        self.imagem.equalizar_histograma()
        self.imagem.salvar('imagens/equalizado.jpg')
        return Image(source='imagens/equalizado.jpg')

    def mostrar_histograma(self):
        """
        Mostra o histograma da imagem.
        """
        histograma = self.imagem.get_histograma(equalizar=True)
        #self.imagem.salvar('imagens/2.jpg')

        graph = Graph(
            xlabel='Tom de Cinza',
            ylabel='Quantidade de tons',
            #x_ticks_minor=5,
            #x_ticks_major=25,
            #y_ticks_major=25,
            #y_grid_label=True,
            #x_grid_label=True,
            padding=5,
            #x_grid=False,
            #y_grid=True,
            xmin=0,
            xmax=max(histograma.keys()),
            ymin=0,
            ymax=max(histograma.values())
        )
        plot = MeshLinePlot() #color=[1, 0, 0, 1])
        plot.points = histograma.items()
        graph.add_plot(plot)
        return graph

    def build(self):
        """
        Carrega a imagem na tela.
        """
        #return self.mostrar_imagem_cinza()
        #return self.mostrar_imagem_equalizada()
        return self.mostrar_histograma()


if __name__ == '__main__':
    MainApp().run()
