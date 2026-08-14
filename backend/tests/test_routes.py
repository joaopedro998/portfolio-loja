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