import pytest
import sys
import os

# Força o Python a enxergar a pasta 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# AVISO CRUCIAL: Declara o modo de teste ANTES de importar o app
os.environ['TESTING'] = 'true'

from app import app
from models import db

@pytest.fixture
def client():
    # Cria um "cliente de teste"
    with app.test_client() as client:
        with app.app_context():
            # Cria todas as tabelas no banco de dados temporário
            db.create_all()
            
            # Pausa aqui e entrega o cliente para os testes rodarem
            yield client
            
            # Limpa o banco de dados depois que os testes terminam
            db.session.remove()
            db.drop_all()