# -*- coding: utf-8 -*-
from . import *
from flask.ext.login import UserMixin, session
from .. import login_manager


class Student(Document, UserMixin):
    class_name = StringField()
    gender = StringField()
    name = StringField()
    student_id = StringField(primary_key=True)
    password = StringField()
    pic_exist = BooleanField(default=False)

    def get_id(self):
        return self.student_id


class Teacher(Document, UserMixin):
    class_name = StringField()
    gender = StringField()
    name = StringField()
    teacher_id = StringField(primary_key=True)
    password = StringField()
    pic_exist = BooleanField(default=False)

    def get_id(self):
        return self.teacher_id


@login_manager.user_loader
def load_user(user_id):
    try:
        a = Student.objects.get(pk=user_id)
        # session['user'] = a
        return a
    except DoesNotExist:
        try:
            return Teacher.objects.get(pk=user_id)
        except DoesNotExist:

            return None


class MyList(Document):
    present = ListField(StringField())
    absent = ListField(StringField())


# class Lesson(Document):
#     lesson_id = StringField(primary_key=True)
#     lesson_name = StringField()
#     teacher_id = StringField()
#     student_list = ListField(StringField())
