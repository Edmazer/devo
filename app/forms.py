from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, PasswordField, SubmitField
from wtforms.validators import EqualTo, Email, DataRequired, ValidationError, Length
from app import app, db, bcrypt
from app.models import User_model



class login_form(FlaskForm):
    email= EmailField('E-mail', validators= [DataRequired(), Email(message= 'Insira um email válido com @')])
    senha= PasswordField('Senha', validators= [DataRequired(), Length(min= 6, message= 'Insira no mínino 8 caracteres')])
    btn_submit= SubmitField('Entrar')

    def login(self):
        user= User_model.query.filter_by(email= self.email.data).first() 
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user
            else:
                raise Exception('Senha incorreta')

        else:
            raise Exception('Usuário não encontrado')

class user_form(FlaskForm):
    nome= StringField('Nome', validators= [DataRequired()])
    email= EmailField('E-mail', validators= [DataRequired(), Email(message= 'Insira um email válido')] )
    trabalho= StringField('Trabalho', validators= [DataRequired(message= 'Insira o seu trabalho')] )
    salario= IntegerField('Salario', validators= [DataRequired(message= 'Insira o seu salário')] )
    senha= PasswordField('Senha', validators=[DataRequired(), Length(min= 6, message= 'Insira no mínino 6 caracteres')])
    senha_confirm= PasswordField('Confirmar senha', validators=[DataRequired(), Length(min= 6, message= 'Insira no mínino 6 caracteres'), EqualTo('senha', message= 'Senhas não compatíveis')])
    btn_submit= SubmitField('Criar conta')

    def validate_email(self, email):
        if User_model.query.filter_by(email= email.data).first():
            return ValidationError(message= 'E-mail inválido, tente com outro')

    def save(self):
        senha= bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        user= User_model(
            nome= self.nome.data,
            email= self.email.data,
            trabalho= self.trabalho.data,
            salario= self.salario.data,
            senha= senha
        )

        db.session.add(user)
        db.session.commit()

        return user