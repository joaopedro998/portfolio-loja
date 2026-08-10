from flask import Flask
from flask_cors import CORS
from models import db
from routes import api 

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loja.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Tabelas do banco de dados verificadas/criadas com sucesso!")

@app.route('/', methods=['GET'])
def home():
    return {"mensagem": "API da Loja rodando com sucesso!"}

app.register_blueprint(api, url_prefix='/api') 

if __name__ == '__main__':
    app.run(debug=True, port=5000)