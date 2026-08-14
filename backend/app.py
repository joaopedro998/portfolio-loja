import os
from flask import Flask
from flask_cors import CORS
from models import db
from routes import api
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração do Cloudinary usando as variáveis do .env
cloudinary.config(
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

# Verifica a variável de ambiente para decidir qual banco usar (Memória x Arquivo real)
if os.environ.get('TESTING') == 'true':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loja.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Só conecta e cria tabelas no arquivo físico se NÃO estivermos no modo de teste
if os.environ.get('TESTING') != 'true':
    with app.app_context():
        db.create_all()
        print("Tabelas do banco de dados verificadas/criadas com sucesso!")

@app.route('/', methods=['GET'])
def home():
    return {"mensagem": "API da Loja rodando com sucesso!"}

app.register_blueprint(api, url_prefix='/api') 

if __name__ == '__main__':
    app.run(debug=True, port=5000)