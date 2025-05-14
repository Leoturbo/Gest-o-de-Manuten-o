from flask_mail import Message
from app import mail
from threading import Thread
from flask import current_app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def notificar_aluguel_proximo_vencimento():
    from models import Aluguel
    from datetime import datetime, timedelta
    
    alugueis = Aluguel.query.filter(
        Aluguel.status == 'Em Andamento',
        Aluguel.data_termino <= datetime.now() + timedelta(days=3)
    ).all()
    
    for aluguel in alugueis:
        subject = f"Aluguel próximo do vencimento - Equipamento {aluguel.equipamento.codigo}"
        recipients = ['admin@empresa.com', aluguel.cliente.contato]
        text_body = f"""
        O aluguel do equipamento {aluguel.equipamento.codigo} vence em {(aluguel.data_termino - datetime.now()).days} dias.
        Cliente: {aluguel.cliente.nome}
        Valor: R${aluguel.valor}
        """
        
        send_email(subject, recipients, text_body, text_body)