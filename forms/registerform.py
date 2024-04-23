from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, DateField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    phone_number = StringField('Телефон', validators=[DataRequired()])
    birthdate = DateField('Дата рождения (ДД.ММ.ГГГГ)', format='%d.%m.%Y')
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
