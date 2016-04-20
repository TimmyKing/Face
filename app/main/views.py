# -*- coding: utf-8 -*-
from .models import *
from . import *
from flask import Flask, render_template, session, flash, redirect, url_for, request
from .forms import *
from errors import error
from flask.ext.login import login_user, login_required, current_user
import errors
from datetime import datetime
from facepp import API, File, APIError
import os

api = API(key='8a7d5a6eb05b56b065a837a82d340bb3', secret='SGpACR-nr6L86cV-Wnq50Hskf8tlJUlC')
student_chek_in = ["41355061", "41355062", "41355063", "41355064", "41355065", "41355066"]


@main.route('/', methods=['GET', 'POST'])  # 主页
def index():
    name = None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.user_id.data
        # form.user_id.data = ''
        return render_template('login.html', form=form, name='')
    else:
        flash('tbjinkj')
        return render_template('login.html', form=form, name='')


@main.route('/login', methods=['GET', 'POST'])  # 登陆
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Student.objects.get(pk=form.user_id.data)
            login_user(user, remember=True)
            next = request.args.get('next')
            # next_is_valid should check if the user has valid
            # permission to access the `next` url
            # if not next_is_valid(next):
            # return abort(400)

            # return redirect(next or url_for('index'))
            if not user.pic_exist:
                return redirect(url_for('main.test'))
            else:
                return redirect(url_for('main.check_in'))
        except:
            return error('The user does not exsit!')
    return render_template('login.html', form=form)


@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@main.route('/register', methods=['GET', 'POST'])  # 注册
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        role = form.role.data
        if role == 'student':
            try:
                Student.objects.get(pk=form.user_id.data)
            except:
                student = Student(student_id=form.user_id.data, name=form.name.data, gender=form.gender.data,
                                  class_name=form.class_name.data, password=form.password.data)
            try:
                student.save()
            except:
                return error('Save Error. User exsit.')
        else:
            try:
                Teacher.objects.get(pk=form.user_id.data)
            except:
                teacher = Teacher(teacher_id=form.user_id.data, name=form.name.data, gender=form.gender.data,
                                  class_name=form.class_name.data, password=form.password.data)
            try:
                teacher.save()
            except:
                return error('Save Error')
        # person = session['user'].student_id

        return redirect(url_for('main.test'))

    else:
        return render_template('register.html', form=form)


@main.route('/test')
@login_required
def test():
    return render_template('Do.html')


@main.route('/photo', methods=['POST', 'GET'])
def get_pic():
    image_string = request.form['data']
    timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    image_file = open(IMAGE_FOLDER + 'temp' + str(timestamp) + '.png', 'wb')
    image_file.write(image_string.decode('base64'))
    image_file.close()
    try:
        a = api.detection.detect(img=File('D:\\temp' + str(timestamp) + '.png'))

        if len(a['face']) >= 0:
            # print a['face'][0]['face_id']
            try:
                api.person.create(person_name=current_user.student_id, face_id=a['face'][0]['face_id'])
                # print a['face'][0]['face_id']
                os.remove('D:\\temp' + str(timestamp) + '.png')
                current_user.update(pic_exist=True)
                api.train.verify(person_name=current_user.student_id)
            except APIError, e:
                print e.body
                return "Error.Face++ is so Low."
            return url_for('main.check_in')
    except APIError, e:
        try:
            api.person.delete(person_name=current_user.studetn_id)

        except:
            pass
        print e.body

    return render_template('login.html', form=LoginForm())


@main.route('/check_in')
@login_required
def check_in():
    return render_template("checkIn.html")


@main.route('/check_in_photo', methods=['POST'])
@login_required
def check_in_photo():
    image_string = request.form['data']
    timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
    image_file = open(IMAGE_FOLDER + 'temp' + str(timestamp) + '.png', 'wb')
    image_file.write(image_string.decode('base64'))
    image_file.close()
    try:
        a = api.detection.detect(img=File('D:\\temp' + str(timestamp) + '.png'))

        if len(a['face']) >= 0:
            # print a['face'][0]['face_id']
            try:
                # api.person.create(person_name=current_user.student_id, face_id=a['face'][0]['face_id'])
                # print a['face'][0]['face_id']
                os.remove('D:\\temp' + str(timestamp) + '.png')
                result = api.recognition.verify(person_name=current_user.student_id, face_id=a['face'][0]['face_id'])
                print result
                if result['is_same_person']:
                    try:
                        student_list = MyList.objects[0]
                    except:
                        student_list = MyList(absent=student_chek_in)
                        student_list.save()
                    student_num = current_user.student_id
                    student_list.update(pull__absent=student_num, add_to_set__present=student_num)

                    return '签到成功'
                else:
                    return '签到失败'
            except APIError, e:
                print e.body
                return "Error.Face++ is so Low."
            return url_for('main.check_in')
    except APIError, e:
        try:
            api.person.delete(person_name=current_user.studetn_id)

        except:
            pass
        print e.body

    return render_template('login.html', form=LoginForm())


@main.route('/teacher')
def teacher():
    students = Student.objects
    try:
        student_list = MyList.objects[0]
        student_present = student_list.present
        student_absent = student_list.absent
        for stu in students:
            if stu.student_id in student_present:
                stu.present = "是"
            else:
                stu.present = "否"

    except:
        student_list = MyList(absent=student_chek_in)
        student_list.save()
        for stu in students:
            stu.present = "否"
    return render_template('teacherUse.html', student_list=students)
