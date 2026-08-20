from flask import Blueprint, request, jsonify
from models import db, Categoria, Produto
import cloudinary.uploader
from models import ImagemProduto
from models import db, Categoria, Produto
from models import db, Categoria, Produto, Pedido, ItemPedido


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
@api.route('/produtos/<int:produto_id>/imagens', methods=['POST'])
def upload_imagens(produto_id):
    # Verifica se o produto existe no banco
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Verifica se a requisição trouxe arquivos (o Front-end vai mandar com o nome 'imagens')
    if 'imagens' not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    # Pega a lista de múltiplos arquivos
    arquivos = request.files.getlist('imagens')
    urls_salvas = []

    for arquivo in arquivos:
        if arquivo.filename != '':
            # 1. Faz o upload da imagem para a nuvem do Cloudinary
            resposta = cloudinary.uploader.upload(arquivo)
            url_imagem = resposta.get('secure_url')
            
            # 2. Salva o link da nuvem na nossa tabela do banco de dados
            nova_imagem = ImagemProduto(url_imagem=url_imagem, produto_id=produto.id)
            db.session.add(nova_imagem)
            
            urls_salvas.append(url_imagem)

    # Confirma as alterações no banco
    db.session.commit()
    
    return jsonify({
        "mensagem": "Imagens salvas com sucesso!", 
        "urls": urls_salvas
    }), 201
@api.route('/pedidos', methods=['POST'])
def criar_pedido():
    dados = request.get_json()

    # 1. Validação de segurança: o carrinho não pode estar vazio
    if not dados or 'itens' not in dados or len(dados['itens']) == 0:
        return jsonify({'erro': 'O carrinho está vazio ou dados inválidos'}), 400

    # 2. Cria o pedido "vazio" primeiro
    novo_pedido = Pedido(status='Pendente')
    db.session.add(novo_pedido)
    
    # O flush() envia para o banco provisoriamente só para gerar o ID do pedido, 
    # pois precisamos desse ID para atrelar aos itens na próxima etapa!
    db.session.flush() 

    total_pedido = 0

    # 3. Percorre cada item que veio do Front-end (Angular)
    for item_data in dados['itens']:
        produto = db.session.get(Produto, item_data['produto_id'])
        
        if not produto:
            db.session.rollback() # Cancela tudo se achar alguma fraude/erro
            return jsonify({'erro': f'Produto ID {item_data["produto_id"]} não encontrado'}), 404

        quantidade = item_data.get('quantidade', 1)
        preco_seguro = produto.preco # Pegamos o preço direto do banco!

        # 4. Cria o item e atrela ao pedido recém-criado
        novo_item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=produto.id,
            quantidade=quantidade,
            preco_unitario=preco_seguro
        )
        db.session.add(novo_item)
        
        # Vai somando o valor total para podermos retornar isso ao Angular
        total_pedido += (preco_seguro * quantidade)

    # 5. Salva tudo de forma definitiva
    db.session.commit()

    return jsonify({
        'mensagem': 'Pedido criado com sucesso!',
        'pedido_id': novo_pedido.id,
        'total': round(total_pedido, 2)
    }), 201