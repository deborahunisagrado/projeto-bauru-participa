from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime

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
    
@app.route('/api/enquetes', methods=['GET'])
def get_enquetes():
    enquetes = Enquete.query.all()
    
    for enquete in enquetes:
        enquete_data = {
            'id_enquete': enquete.id_enquete,
            'titulo': enquete.titulo,
            'descricao': enquete.descricao,
            'texto_questao': enquete.texto_questao,
            'data_criacao': enquete.data_criacao,
            'ativo': enquete.ativo
        }
    
    return jsonify(enquete_data), 200

@app.route('/api/enquete', methods=['POST'])
def create_enquete():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    new_enquete = Enquete(titulo=data['titulo'], descricao=data['descricao'], texto_questao=data['texto_questao'], data_criacao=datetime.date.today(), ativo=True)
    db.session.add(new_enquete)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 200

@app.route('/api/enquetes/<int:id_enquete>', methods=['GET'])
def get_enquete(id_enquete):
    enquete = Enquete.query.get(id_enquete)
    opcoes = Opcao.query.filter_by(id_enquete=id_enquete).all()
    opcoes_list = []
    
    if enquete is None:
        return jsonify({"message": "Enquete not found"}), 404
    
    for opcao in opcoes:
        opcao_data = {
            'id_opcao': opcao.id_opcao,
            'texto_opcao': opcao.texto_opcao,
            'ativo': opcao.ativo
        }
        opcoes_list.append(opcao_data)

    enquete_data = {
        'id_enquete': enquete.id_enquete,
        'titulo': enquete.titulo,
        'descricao': enquete.descricao,
        'texto_questao': enquete.texto_questao,
        'data_criacao': enquete.data_criacao.strftime('%Y-%m-%d'),  
        'ativo': enquete.ativo,
        'opcoes': opcoes_list 
    }
    
    return jsonify(enquete_data), 200


@app.route('/api/enquetes/<int:id_enquete>/opcoes', methods=['POST'])
def create_opcao(id_enquete):
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    enquete = Enquete.query.get(id_enquete)
    
    if enquete is None:
        return jsonify({"message": "Enquete not found"}), 404
    
    new_opcao = Opcao(id_enquete=id_enquete, texto_opcao=data['texto_opcao'], ativo=True)
    db.session.add(new_opcao)
    db.session.commit()
    return jsonify({"message": "Opcao created successfully"}), 200

@app.route('/api/enquetes/<int:id_enquete>/opcao', methods=['GET'])
def get_opcao(id_enquete):
    opcoes = Opcao.query.filter_by(id_enquete=id_enquete).all()
    opcoes_list = []
    
    for opcao in opcoes:
        opcao_data = {
            'id_opcao': opcao.id_opcao,
            'texto_opcao': opcao.texto_opcao,
            'ativo': opcao.ativo
        }
        opcoes_list.append(opcao_data)
        
    return jsonify(opcoes_list), 200

@app.route('/api/enquetes/<int:id_enquete>/votar', methods=['POST'])
def create_resposta(id_enquete):
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    enquete = Enquete.query.get(id_enquete)
    opcao = Opcao.query.get(data['id_opcao'])
    
    if enquete is None:
        return jsonify({"message": "Enquete not found"}), 404
    
    if opcao is None:
        return jsonify({"message": "Opcao not found"}), 404
    
    new_resposta = Resposta(id_enquete=id_enquete, id_opcao=data['id_opcao'], data_resposta=datetime.date.today())
    db.session.add(new_resposta)
    db.session.commit()
    return jsonify({"message": "Resposta created successfully"}), 200

@app.route('/api/enquetes/<int:id_enquete>/respostas', methods=['GET'])
def get_respostas(id_enquete):
    # Realiza a contagem das respostas por opção para a enquete específica
    counts = db.session.query(Resposta.id_opcao, func.count()).filter_by(id_enquete=id_enquete).group_by(Resposta.id_opcao).all()
    
    counts_data = []
    for count in counts:
        count_data = {
            'id_opcao': count[0],
            'quantidade_respostas': count[1]
        }
        counts_data.append(count_data)
        
    return jsonify(counts_data), 200

@app.route('/api/enquetes/<int:id_enquete>', methods=['PUT'])
def update_enquete(id_enquete):
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    enquete = Enquete.query.get(id_enquete)
    
    if enquete is None:
        return jsonify({"message": "Enquete not found"}), 404
    
    enquete.ativo = False
    db.session.commit()
    
    return jsonify({"message": "Enquete updated successfully"}), 200

@app.route('/api/enquetes/<int:id_enquete>/opcoes/<int:id_opcao>', methods=['PUT'])
def update_opcao(id_enquete, id_opcao):
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    
    enquete = Enquete.query.get(id_enquete)
    
    if enquete is None:
        return jsonify({"message": "Enquete not found"}), 404
    
    opcao = Opcao.query.get(id_opcao)
    
    if opcao is None:
        return jsonify({"message": "Opcao not found"}), 404
    
    opcao.ativo = False
    db.session.commit()
    
    return jsonify({"message": "Opcao updated successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='localhost', port=5000)