#-*- coding: utf-8 -*-
import kivy
#kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.core.window import Window
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from core import Imagem, Operacoes
from menus import (
    MenuImagem, MenuPassaAlta, MenuPassaBaixa,
    MenuOperacoes, MenuRealce, MenuBorda
)


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
        self.menu_imagem = MenuImagem()
        self.menu_passa_alta = MenuPassaAlta()
        self.menu_passa_baixa = MenuPassaBaixa()
        self.menu_operacoes = MenuOperacoes()
        self.menu_realce = MenuRealce()
        self.menu_borda = MenuBorda()
        self.imagem_core = None
        self.widgets_dinamicos = []
        self.carregar_imagem('imagens/1.jpg')

    def recarregar_imagem(self):
        """
        Recarrega a imagem em tela.
        """
        self.salvar_imagem(caminho_imagem=self.caminho_temp)
        self.carregar_imagem(caminho_imagem=self.caminho_temp)

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
        Remove os widgets adicionados dinâmicamente.
        """
        for widget in self.widgets_dinamicos:
            self.remove_widget(widget)

    def mostrar_imagem_cinza(self):
        """
        Mostra a imagem em escala de cinza.
        """
        self.imagem_core.converter_escala_cinza()
        self.recarregar_imagem()

    def mostrar_imagem_equalizada(self):
        """
        Mostra a imagem equalizada.
        """
        self.imagem_core.equalizar_imagem()
        self.recarregar_imagem()

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

    def aplicar_filtro(self, nome_filtro, mascara=None, tecnica=None):
        """
        Aplica um filtro na imagem.
        """
        if tecnica:
	    self.imagem_core.aplicar_filtro(
	        nome_filtro=nome_filtro,
                tecnica=tecnica
	    )
        else:
	    self.imagem_core.aplicar_filtro(
	        nome_filtro=nome_filtro,
   	        mascara=mascara,
	    )
        self.recarregar_imagem()

    def aplicar_operacao(self, operacao, imagem=None):
        """
        Aplica uma operação sobre a imagem.
        """
        operacoes = Operacoes(self.imagem_core)
        metodo_operacao = getattr(operacoes, operacao, None)
        if metodo_operacao:
            metodo_operacao(imagem)
        self.recarregar_imagem()


class MainApp(App):
    """
    Aplicação.
    """

    def build(self):
        """
        Carrega a imagem na tela.
        """
        self.title = 'Processamento Digital de Imagens'
        self.main_layout = MainLayout()
        return self.main_layout


if __name__ == '__main__':
    MainApp().run()
