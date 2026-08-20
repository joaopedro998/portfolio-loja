from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializa o objeto do banco de dados
db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    
    # Relacionamento: Uma categoria tem vários produtos
    produtos = db.relationship('Produto', backref='categoria', lazy=True)

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tamanhos_disponiveis = db.Column(db.String(50), nullable=False) # Ex: "P, M, G"
    status = db.Column(db.String(20), default='Disponível') # Pode ser "Disponível" ou "Vendido"
    
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    
    # Relacionamento: Um produto tem várias imagens e pode ter uma venda
    imagens = db.relationship('ImagemProduto', backref='produto', lazy=True, cascade="all, delete-orphan")
    venda = db.relationship('VendaFinanceiro', backref='produto', uselist=False, lazy=True)

class ImagemProduto(db.Model):
    __tablename__ = 'imagens_produto'
    
    id = db.Column(db.Integer, primary_key=True)
    url_imagem = db.Column(db.String(255), nullable=False) # Link do Cloudinary
    
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)

class VendaFinanceiro(db.Model):
    __tablename__ = 'vendas_financeiro'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    valor_venda = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False) # "Pix", "Cartão", etc.
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(50), default='Pendente') 
    
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "status": self.status,
            "itens": [item.to_dict() for item in self.itens]
        }

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False) 

    produto = db.relationship('Produto')

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "nome_produto": self.produto.nome if self.produto else None,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "subtotal": round(self.quantidade * self.preco_unitario, 2)
        }