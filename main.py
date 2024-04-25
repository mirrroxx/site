from flask import Flask, render_template, url_for, redirect, request, session
from data import db_session
from data.dishes import Dishes
from data.users import User
from data.application import Application
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import os
import sys

import pygame
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

import datetime

date = datetime.datetime.now()

days = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу', 'Субботу', 'Воскресенье']

day = days[date.weekday()]


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        elif db_sess.query(Application).filter(Application.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = Application(
            name=form.name.data,
            email=form.email.data,
            grade=form.grade.data,
            role=form.role.data,
            balance=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/inform')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login2.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login2.html', title='Авторизация', form=form)


@app.route('/inform')
def inform():
    return render_template('inform.html')


@app.route("/add_new_user")
def add():
    if current_user.role == 'student' or current_user.role == 'cook':
        return redirect('/')
    else:
        db_sess = db_session.create_session()
        application = db_sess.query(Application)
        return render_template("application.html", application=application)

@app.route('/order')
def order():
    if current_user.role == 'student':
        return redirect('/')
    else:
        teacher_grade = current_user.grade
        db_sess = db_session.create_session()
        data = db_sess.query(User).filter(User.grade==teacher_grade, User.role == 'student').all()
        return render_template("order.html", data=data)


@app.route('/add/<int:id>')
def add_user(id):

    db_sess = db_session.create_session()
    data = db_sess.query(Application).filter(Application.id == id).first()
    user = User()
    user.name = data.name
    user.email = data.email
    user.grade = data.grade
    user.role = data.role
    user.hashed_password = data.hashed_password
    user.balance = data.balance
    db_sess.add(user)
    db_sess.commit()

    user = db_sess.query(Application).filter(Application.id == id).first()
    db_sess.delete(user)
    db_sess.commit()
    return redirect('/add_new_user')

@app.route('/reject/<int:id>')
def reject(id):
    db_sess = db_session.create_session()
    user = db_sess.query(Application).filter(Application.id == id).first()
    db_sess.delete(user)
    db_sess.commit()
    return redirect('/add_new_user')


@app.route('/api')
def api():

    map_request = "http://static-maps.yandex.ru/1.x/?ll=37.587093,55.7339748&spn=0.002,0.002&l=map"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption('Яндекс офис(улица Льва Толстого, 16, Москва, 119021)')
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    # Удаляем за собой файл с изображением.
    os.remove(map_file)
    return redirect('/')


@app.route('/profile')
@login_required
def profile():
    name = current_user.name
    name = "_".join(name.split())
    grade = current_user.grade
    balance = current_user.balance
    return render_template('profile.html', name=name, balance=balance, grade=grade)


@app.route('/')
def index():
    return render_template("main.html")


@app.errorhandler(401)
def go_login(code):
    return redirect('/login')


@app.route('/breakfast')
@login_required
def breakfast():
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dishes).filter(Dishes.time == 'утреннее меню').all()
    return render_template("menu.html", dishes=dishes, day=day)


@app.route('/dinner1')
@login_required
def dinner1():
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dishes).filter(Dishes.time == 'обеденное меню').all()
    return render_template("menu.html", dishes=dishes, day=day)


@app.route('/dinner2')
@login_required
def dinner2():
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dishes).filter(Dishes.time == 'вечернее меню').all()
    return render_template("menu.html", dishes=dishes, day=day)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name_of_dish = request.form['name']
        time = request.form['menu_type']
        dish_price = request.form['price']
        image = request.files['image']

        dish = Dishes(name=name_of_dish, time=time, price=dish_price)
        if image:
            image.save('static/img/' + image.filename)
            dish.photo = 'img/' + image.filename
        try:
            db_sess = db_session.create_session()
            db_sess.add(dish)
            db_sess.commit()
            return redirect('/')
        except:
            return "При добавлении произошла ошибка"

    return render_template("new_dish.html")

    
if __name__ == '__main__':
    db_session.global_init("db/main.db")
    app.run(debug=True)