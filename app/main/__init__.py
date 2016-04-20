# -*- coding: utf-8 -*-
from flask import Blueprint

from mongoengine import BooleanField, IntField, StringField, ListField, Document, DoesNotExist

IMAGE_FOLDER = 'D:\\'
main = Blueprint('main', __name__)
import errors, views
