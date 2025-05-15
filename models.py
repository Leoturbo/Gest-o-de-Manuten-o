from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='tecnico')  # admin, tecnico, cliente
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    manutencoes = db.relationship('Manutencao', backref='tecnico_rel', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, index=True, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    valor_compra = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.Date, nullable=False)
    fornecedor = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Disponível')  # Disponível, Alugado, Manutenção
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    manutencoes = db.relationship('Manutencao', backref='equipamento', lazy='dynamic')
    alugueis = db.relationship('Aluguel', backref='equipamento', lazy='dynamic')
    
    def __repr__(self):
        return f'<Equipamento {self.codigo}>'

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    contato = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    alugueis = db.relationship('Aluguel', backref='cliente', lazy='dynamic')
    
    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Aluguel(db.Model):
    __tablename__ = 'alugueis'
    
    id = db.Column(db.Integer, primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_termino = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Em Andamento')  # Em Andamento, Finalizado
    pago = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Aluguel {self.id}>'

class Manutencao(db.Model):
    __tablename__ = 'manutencoes'
    
    id = db.Column(db.Integer, primary_key=True)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)
    tecnico_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    data = db.Column(db.Date, nullable=False)
    problemas = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # Preventiva, Corretiva, Preditiva
    custo = db.Column(db.Float)
    proxima_manutencao = db.Column(db.Date)
    foto_path = db.Column(db.String(200))
    localizacao = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Manutencao {self.id}>'