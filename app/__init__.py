from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import dotenv
import os

# Carregar a variável de ambiente(.env)
dotenv.load_dotenv('.env')

# Criação do objecto Flask e configuração do mesmo
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')


# Criação as variáveis de configuração do banco, do formulário
lm= LoginManager(app)
# lm.login_view= 'login'
bcrypt= Bcrypt(app)
db= SQLAlchemy(app)
migrate= Migrate(app, db)

# Importação dos módulos de reenderização, e do banco de dados
from app import views
from app import models