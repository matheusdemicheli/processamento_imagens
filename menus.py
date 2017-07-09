#-*- coding: utf-8 -*-
from kivy.uix.dropdown import DropDown
from utils import LoadDialog, SaveDialog, MascaraDialog


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


class MenuImagem(Menu):
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


class MenuRealce(Menu):
    """
    Menu para o Realce.
    """

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

    def limpar(self, app):
        """
        Limpa a tela.
        """
        app.main_layout.limpar()



class MenuFiltros(Menu):
    """
    Menu dos filtros.
    """

    def aplicar_filtro(self, app, nome_filtro):
        """
        Aplica o filtro de correlação.
        """
        janela = MascaraDialog(nome_filtro=nome_filtro)
        janela.popup.open()


class MenuPassaAlta(MenuFiltros):
    """
    Menu Passa Alta.
    """
    pass


class MenuPassaBaixa(MenuFiltros):
    """
    Menu Passa Baixa.
    """
    pass


class MenuBorda(MenuFiltros):
    """
    Menu para técnicas de detecção de Borda.
    """

    def aplicar_filtro(self, app, nome_filtro, tecnica):
        """
        Aplica o filtro de correlação.
        """
        app.main_layout.aplicar_filtro(nome_filtro, tecnica=tecnica)


class MenuOperacoes(Menu):
    """
    Menu de operações.
    """

    def aplicar_operacao(self, app, operacao):
        """
        Aplica uma operação sobre a imagem.
        """
        if operacao == 'operador_not':
            app.main_layout.aplicar_operacao(operacao=operacao)
        else:
            janela = LoadDialog(origem='operacoes', operacao=operacao)
            janela.popup.open()
