from app import app
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import user_form, login_form
from app.models import User_model


@app.route('/entrar/', methods= ['GET', 'POST'])
def login_page():

        form= login_form()

        if form.validate_on_submit():
            user= form.login()
            
            login_user(user, remember= True)
            print(current_user.nome)
            return redirect(url_for('home_page'))

        return render_template('login.html', form= form)

###################################################################

@app.route('/sair/', methods= ['GET', 'POST'])
def logout_page():

    logout_user()

    return redirect(url_for('login_page'))
###################################################################

@app.route('/cadastro/', methods= ['GET', 'POST'])
def cadastro_page():
    form= user_form()

    if form.validate_on_submit():
        user= form.save()

        return redirect(url_for('login_page'))

    else:
        flash(message= 'Erro ao cadastrar, tente com outro e-mail')
        print(form.errors)
    
    return render_template('cadastro.html', form= form)
###################################################################

@app.route('/', methods= ['GET', 'POST'])
def home_page():
    context= 0
    if request.method == 'POST':
        produto= request.form.get('produto', '')
        preco= float(request.form.get('preco', ''))

        # horas por mês, considerando que a pessoa trabalha 22 dias no mês e 8 horas por dia
        hora = 22 * 8

        # valor por hora(pagamento por horas de trabalho)
        valor= int(current_user.salario) / hora

        # custo horário do produto
        tempo= preco / round(valor, 2)

        # minutos
        decimal= int(tempo) - round(tempo, 2)
        minuto= abs(round(decimal, 2)) * 60

        # conversão da hora e minuto para dia
        m= minuto / 60
        h= int(tempo) + m

        dia= h / 24

        context= {
            'produto': produto,
            'preco': preco,
            'tempo': int(tempo), 
            'minuto': int(minuto),
            'dia': round(dia, 2)
        }

    if current_user.is_authenticated:
        return render_template('index.html', context= context)
    else:
        return redirect(url_for('comeco_page'))

@app.route('/comeco/')
def comeco_page():
    return render_template('comeco.html')
