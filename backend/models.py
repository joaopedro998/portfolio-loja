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