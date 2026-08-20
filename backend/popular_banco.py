# Importa o seu aplicativo e as ferramentas do banco de dados
from app import app
from models import db, Categoria, Produto

# Entra no contexto do Flask para poder mexer no banco
with app.app_context():
    print("Iniciando a inserção de produtos...")

    # 1. Cria uma Categoria primeiro (porque o produto precisa de uma)
    categoria_verao = Categoria(nome="Coleção de Verão")
    db.session.add(categoria_verao)
    
    # Salva no banco para o Flask gerar o ID dessa categoria
    db.session.commit() 

    # 2. Cria as nossas 3 roupas famosas
    produto1 = Produto(
        nome="Camiseta Básica Preta",
        preco=49.90,
        tamanhos_disponiveis="P,M,G,GG",
        categoria_id=categoria_verao.id
    )

    produto2 = Produto(
        nome="Vestido Florido",
        preco=129.90,
        tamanhos_disponiveis="P,M,G",
        categoria_id=categoria_verao.id
    )

    produto3 = Produto(
        nome="Conjunto Moletom",
        preco=199.90,
        tamanhos_disponiveis="M,G,GG",
        categoria_id=categoria_verao.id
    )

    # 3. Adiciona todas as roupas no banco e salva!
    db.session.add_all([produto1, produto2, produto3])
    db.session.commit()

    print("✅ Banco de dados populado com sucesso! Já pode olhar a sua vitrine.")