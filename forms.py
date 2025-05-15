from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, FloatField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField('Repetir Senha', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Função', choices=[('admin', 'Administrador'), ('tecnico', 'Técnico'), ('cliente', 'Cliente')])

class EquipamentoForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired(), Length(min=3, max=20)])
    descricao = StringField('Descrição', validators=[DataRequired(), Length(min=5, max=200)])
    tipo = SelectField('Tipo', choices=[
        ('Gerador', 'Gerador'), 
        ('Compressor', 'Compressor'), 
        ('Betoneira', 'Betoneira')
    ])
    valor_compra = FloatField('Valor de Compra', validators=[DataRequired()])
    data_compra = DateField('Data de Compra', validators=[DataRequired()])
    fornecedor = StringField('Fornecedor', validators=[Length(max=100)])
    status = SelectField('Status', choices=[
        ('Disponível', 'Disponível'), 
        ('Alugado', 'Alugado'), 
        ('Manutenção', 'Em Manutenção')
    ])

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3, max=100)])
    contato = StringField('Contato', validators=[DataRequired(), Length(min=5, max=100)])
    endereco = TextAreaField('Endereço', validators=[Length(max=200)])

class ManutencaoForm(FlaskForm):
    equipamento_id = SelectField('Equipamento', coerce=int)
    data = DateField('Data', validators=[DataRequired()])
    problemas = TextAreaField('Problemas Encontrados', validators=[DataRequired()])
    tipo = SelectField('Tipo de Manutenção', choices=[
        ('Preventiva', 'Preventiva'),
        ('Corretiva', 'Corretiva'),
        ('Preditiva', 'Preditiva')
    ])
    tecnico = StringField('Técnico Responsável', validators=[DataRequired()])
    custo = FloatField('Custo')
    proxima_manutencao = DateField('Próxima Manutenção')