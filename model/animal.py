from sqlalchemy import Column, String, Integer, Float
from datetime import datetime
from typing import Union

from  model import Base


class Animal(Base):
    __tablename__ = 'animal'

    id = Column("pk_animal", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    vida = Column(Integer)
    velocidade = Column(Integer)
    tamanho = Column(Float)
    peso = Column(Float)
    imagem = Column(String)

    def __init__(self, nome:str, vida:int, velocidade:int, tamanho:float, peso:float, imagem:str):
        """
        Cria um Animal

        Arguments:
            nome: nome do animal.
            valor: valor esperado para o animal
        """
        self.nome = nome
        self.vida = vida
        self.velocidade = velocidade
        self.tamanho = tamanho
        self.peso = peso
        self.imagem = imagem


