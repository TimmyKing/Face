# -*- coding: utf-8 -*-
from flask import render_template
from . import main


@main.errorhandler(404)  # 自定义404错误页面
def page_not_found(e):
    return render_template('error.html')


def error(info):
    return render_template('error.html', info=info)
