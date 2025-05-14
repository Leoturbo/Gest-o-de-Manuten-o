from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))  # admin, tecnico, cliente
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Equipamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, index=True)
    descricao = db.Column(db.String(200))
    tipo = db.Column(db.String(50))
    valor_compra = db.Column(db.Float)
    data_compra = db.Column(db.Date)
    fornecedor = db.Column(db.String(100))
    status = db.Column(db.String(20))  # Disponível, Alugado, Manutenção
    manutencoes = db.relationship('Manutencao', backref='equipamento', lazy='dynamic')
    alugueis = db.relationship('Aluguel', backref='equipamento', lazy='dynamic')

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    contato = db.Column(db.String(100))
    endereco = db.Column(db.String(200))
    alugueis = db.relationship('Aluguel', backref='cliente', lazy='dynamic')

class Aluguel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamento.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    data_inicio = db.Column(db.Date)
    data_termino = db.Column(db.Date)
    valor = db.Column(db.Float)
    forma_pagamento = db.Column(db.String(50))
    status = db.Column(db.String(20))  # Em Andamento, Finalizado
    pago = db.Column(db.Boolean, default=False)

class Manutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamento.id'))
    data = db.Column(db.Date)
    problemas = db.Column(db.Text)
    tipo = db.Column(db.String(20))  # Preventiva, Corretiva, Preditiva
    tecnico = db.Column(db.String(100))
    custo = db.Column(db.Float)
    proxima_manutencao = db.Column(db.Date)
    foto_path = db.Column(db.String(200))
    localizacao = db.Column(db.String(100))