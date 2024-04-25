
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired



class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Фамилия, имя', validators=[DataRequired()])
    grade = StringField('Номер класса и буква (пример: "8A")', validators=[DataRequired()])
    role = SelectField('Тип пользователя:', choices=[('teacher', 'Учитель'), ('student', 'Ученик'), ('cook', 'Повар')], validators=[DataRequired()])
    submit = SubmitField('Отправить заявку')

class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

    submit = SubmitField('Войти')

