from flask import Blueprint, request, jsonify
from models import db, Categoria, Produto

# Cria um Blueprint chamado 'api'
api = Blueprint('api', __name__)

@api.route('/categorias', methods=['POST'])
def criar_categoria():
    # Recebe os dados em formato JSON 
    dados = request.get_json()
    
    # Cria o objeto Categoria
    nova_categoria = Categoria(nome=dados['nome'])
    
    # Adiciona e salva no banco de dados
    db.session.add(nova_categoria)
    db.session.commit()
    
    return jsonify({"mensagem": "Categoria criada!", "id": nova_categoria.id}), 201

@api.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    
    # Cria o objeto Produto vinculando à Categoria
    novo_produto = Produto(
        nome=dados['nome'],
        preco=dados['preco'],
        tamanhos_disponiveis=dados['tamanhos_disponiveis'],
        categoria_id=dados['categoria_id']
    )
    
    db.session.add(novo_produto)
    db.session.commit()
    
    return jsonify({"mensagem": "Produto cadastrado com sucesso!", "id": novo_produto.id}), 201