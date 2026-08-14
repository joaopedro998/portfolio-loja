def test_criar_categoria_com_sucesso(client):
    # PREPARAÇÃO & AÇÃO: Simulamos o envio de um JSON para a nossa rota
    resposta = client.post('/api/categorias', json={
        "nome": "Feminino"
    })
    
    # VERIFICAÇÃO (Asserts): O que esperamos que aconteça?
    
    # 1. Esperamos que o código de status HTTP seja 201 (Created)
    assert resposta.status_code == 201
    
    # 2. Esperamos que a mensagem de sucesso venha no JSON
    dados = resposta.get_json()
    assert dados["mensagem"] == "Categoria criada!"
    
    # 3. Esperamos que o banco de dados tenha gerado o ID 1
    assert dados["id"] == 1

def test_criar_produto_com_sucesso(client):
    # PREPARAÇÃO: Primeiro criamos uma categoria para o produto pertencer
    resposta_categoria = client.post('/api/categorias', json={
        "nome": "Vestidos"
    })
    
    # Pegamos o ID da categoria que acabou de ser criada na memória
    categoria_id = resposta_categoria.get_json()["id"]
    
    # AÇÃO: Agora criamos o produto vinculando a ele o ID da categoria
    resposta_produto = client.post('/api/produtos', json={
        "nome": "Vestido de Festa",
        "preco": 299.90,
        "tamanhos_disponiveis": "P, M",
        "categoria_id": categoria_id
    })
    
    # VERIFICAÇÃO (Asserts)
    
    # 1. Verifica se deu sucesso na criação (Status 201)
    assert resposta_produto.status_code == 201
    
    # 2. Verifica se a mensagem de retorno está correta
    dados = resposta_produto.get_json()
    assert dados["mensagem"] == "Produto cadastrado com sucesso!"
    
    # 3. Verifica se o banco de dados gerou o ID 1 para este primeiro produto
    assert dados["id"] == 1