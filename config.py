# -*- coding: utf-8 -*-


class Config:
    @staticmethod
    def init_app(app):
        app.config['SECRET_KEY'] = 'Timmy'
        app.config['DATABASE_NAME'] = 'MY_FACE'
