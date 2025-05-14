from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')

class EquipamentoForm(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[
        ('Gerador', 'Gerador'),
        ('Compressor', 'Compressor'),
        ('Betoneira', 'Betoneira')
    ])
    valor_compra = FloatField('Valor de Compra', validators=[DataRequired()])
    data_compra = DateField('Data de Compra', validators=[DataRequired()])
    fornecedor = StringField('Fornecedor')
    status = SelectField('Status', choices=[
        ('Disponível', 'Disponível'),
        ('Alugado', 'Alugado'),
        ('Manutenção', 'Em Manutenção')
    ])

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