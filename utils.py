#-*- coding: utf-8 -*-
from PIL import Image


def salvar_imagem_outro_nome(nome_original, nome_alterado):
    """
    Salva uma imagem com outro nome.
    """
    imagem = Image.open(nome_original)
    imagem.save(nome_alterado)
    imagem.close()

