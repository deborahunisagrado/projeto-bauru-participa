from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Enquete(db.Model):
    id_enquete = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(120), nullable=False)
    texto_questao = db.Column(db.String(120), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)
    
class Opcao(db.Model):
    id_opcao = db.Column(db.Integer, primary_key=True)
    id_enquete = db.Column(db.Integer, db.ForeignKey('enquete.id_enquete'), nullable=False)
    texto_opcao = db.Column(db.String(120), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)

class Resposta(db.Model):
    id_resposta = db.Column(db.Integer, primary_key=True)
    id_enquete = db.Column(db.Integer, db.ForeignKey('enquete.id_enquete'), nullable=False)
    id_opcao = db.Column(db.Integer, db.ForeignKey('opcao.id_opcao'), nullable=False)
    data_resposta = db.Column(db.DateTime, nullable=False)
    
