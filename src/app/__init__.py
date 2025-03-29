# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Cria e configura a aplicação
    app = Flask(__name__)
    
    # Configuração do banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waste_calculation.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa o db com a aplicação
    db.init_app(app)
    
    # Importa e registra as rotas
    from app.routes import api
    app.register_blueprint(api)
    
    # Certifica que a pasta da base de dados existe
    os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')), exist_ok=True)
    
    # Cria as tabelas no banco de dados
    with app.app_context():
        db.create_all()
    
    return app