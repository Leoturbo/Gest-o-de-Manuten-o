from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import Config
import click
from flask.cli import with_appcontext
from datetime import datetime

# Inicialização do app e extensões
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# Importação de modelos
from models import User, Equipamento, Cliente, Aluguel, Manutencao

# Configuração do user_loader
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Importação de formulários
from forms import LoginForm, RegistrationForm, EquipamentoForm, ManutencaoForm, ClienteForm

# Injeta a variável 'now' em todos os templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Comando CLI para criar admin
@click.command('create-admin')
@with_appcontext
def create_admin_command():
    """Cria um usuário admin inicial"""
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully!")
    else:
        print("ℹ️ Admin user already exists!")

app.cli.add_command(create_admin_command)

# Rotas principais
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha inválidos', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login realizado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('auth/login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index'))

# Rotas de equipamentos
@app.route('/equipamentos')
@login_required
def listar_equipamentos():
    equipamentos = Equipamento.query.all()
    return render_template('equipamentos/listar.html', equipamentos=equipamentos)

@app.route('/equipamentos/adicionar', methods=['GET', 'POST'])
@login_required
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

# Rotas de clientes
@app.route('/clientes')
@login_required
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)

@app.route('/clientes/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            contato=form.contato.data,
            endereco=form.endereco.data
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente adicionado com sucesso!', 'success')
        return redirect(url_for('listar_clientes'))
    return render_template('clientes/form.html', form=form)

# Rotas de manutenção
@app.route('/manutencoes')
@login_required
def listar_manutencoes():
    manutencoes = Manutencao.query.all()
    return render_template('manutencoes/listar.html', manutencoes=manutencoes)

@app.route('/manutencoes/registrar', methods=['GET', 'POST'])
@login_required
def registrar_manutencao():
    form = ManutencaoForm()
    form.equipamento_id.choices = [(e.id, e.codigo) for e in Equipamento.query.all()]
    
    if form.validate_on_submit():
        manutencao = Manutencao(
            equipamento_id=form.equipamento_id.data,
            data=form.data.data,
            problemas=form.problemas.data,
            tipo=form.tipo.data,
            tecnico=current_user.username,
            custo=form.custo.data,
            proxima_manutencao=form.proxima_manutencao.data
        )
        
        equipamento = Equipamento.query.get(form.equipamento_id.data)
        equipamento.status = 'Manutenção'
        
        db.session.add(manutencao)
        db.session.commit()
        
        flash('Manutenção registrada com sucesso!', 'success')
        return redirect(url_for('listar_manutencoes'))
    
    return render_template('manutencoes/form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)