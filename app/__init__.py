from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging 

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='LOG: %(asctime)s: %(message)s')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, db)

from app import views, models