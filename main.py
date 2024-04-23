import os.path

from flask import Flask, render_template, url_for, redirect, request
from data import db_session
from data.dishes import Dishes
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

login_manager = LoginManager()
login_manager.init_app(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            return redirect("/")
        return render_template('login2.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login2.html', title='Авторизация', form=form)


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/breakfast')
def breakfast():
    dishes = Dishes.query.all().filter(Dishes.date == 'Утреннее меню')
    return render_template("breakfast.html", dishes=dishes)


@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name_of_dish = request.form['name_of_dish']
        time = request.form['menu_type']
        dish_price = request.form['dish_price']
        if 'file' not in request.files:
            return redirect('/add_dish')
        file = request.files['file']
        if file.filename == '':
            return redirect('/add_dish')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return redirect('/add_dish')
        dish = Dishes(name=name_of_dish, time=time, price=dish_price, photo=os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
