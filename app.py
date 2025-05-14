from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from models import User, Equipamento, Cliente, Aluguel, Manutencao
from forms import LoginForm, RegistrationForm, EquipamentoForm, ManutencaoForm

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/equipamentos')
def listar_equipamentos():
    equipamentos = Equipamento.query.all()
    return render_template('equipamentos/listar.html', equipamentos=equipamentos)

@app.route('/equipamentos/adicionar', methods=['GET', 'POST'])
def adicionar_equipamento():
    form = EquipamentoForm()
    if form.validate_on_submit():
        equipamento = Equipamento(
            codigo=form.codigo.data,
            descricao=form.descricao.data,
            tipo=form.tipo.data,
            valor_compra=form.valor_compra.data,
            data_compra=form.data_compra.data,
            fornecedor=form.fornecedor.data,
            status=form.status.data
        )
        db.session.add(equipamento)
        db.session.commit()
        flash('Equipamento adicionado com sucesso!', 'success')
        return redirect(url_for('listar_equipamentos'))
    return render_template('equipamentos/form.html', form=form)

@app.route('/manutencoes/registrar', methods=['GET', 'POST'])
def registrar_manutencao():
    form = ManutencaoForm()
    form.equipamento_id.choices = [(e.id, e.codigo) for e in Equipamento.query.all()]
    
    if form.validate_on_submit():
        manutencao = Manutencao(
            equipamento_id=form.equipamento_id.data,
            data=form.data.data,
            problemas=form.problemas.data,
            tipo=form.tipo.data,
            tecnico=form.tecnico.data,
            custo=form.custo.data,
            proxima_manutencao=form.proxima_manutencao.data
        )
        
        # Atualiza status do equipamento
        equipamento = Equipamento.query.get(form.equipamento_id.data)
        equipamento.status = 'Manutenção'
        
        db.session.add(manutencao)
        db.session.commit()
        
        flash('Manutenção registrada com sucesso!', 'success')
        return redirect(url_for('listar_manutencoes'))
    
    return render_template('manutencoes/form.html', form=form)

# ... (outras rotas para clientes, aluguéis, relatórios)