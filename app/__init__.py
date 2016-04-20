# -*- coding: utf-8 -*-'
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from config import Config
import mongoengine
from flask.ext.login import LoginManager

bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    Config.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    mongoengine.connect(app.config['DATABASE_NAME'])
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
