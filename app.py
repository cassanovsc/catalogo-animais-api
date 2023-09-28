from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Animal
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Catálogo de Animais API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Documentação Swagger")
animal_tag = Tag(name="Animal", description="Visualização dos animais")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi/swagger, tela de documentação em Swagger.
    """
    return redirect('/openapi/swagger')


@app.get('/animais', tags=[animal_tag],
         responses={"200": ListagemAnimaisSchema, "404": ErrorSchema})
def get_animais():
    """Faz a busca por todos os animais cadastrados

    Retorna uma representação da listagem de animais.
    """
    logger.debug(f"Coletando animais ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    animais = session.query(Animal).all()

    if not animais:
        # se não há animais cadastrados
        return {"animais": []}, 200
    else:
        logger.debug(f"%d animais econtrados" % len(animais))
        # retorna a representação de animal
        return apresenta_animais(animais), 200


@app.get('/animal', tags=[animal_tag],
         responses={"200": AnimalViewSchema, "404": ErrorSchema})
def get_animal(query: AnimalBuscaSchema):
    """Faz a busca por um animal a partir do seu nome

    Retorna uma representação dos animais.
    """
    animal_nome = unquote(unquote(query.nome))
    logger.debug(f"Coletando dados sobre animal {animal_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    animal = session.query(Animal).filter(Animal.nome == animal_nome).first()

    if not animal:
        # se o animal não foi encontrado
        error_msg = "Animal não encontrado na base :/"
        logger.warning(f"Erro ao buscar animal '{animal_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Animal econtrado: '{animal.nome}'")
        # retorna a representação de animal
        return apresenta_animal(animal), 200

