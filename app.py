from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from data import db_session, goods_api
from data.users import User
from data.goods import Goods
from data.cart import Cart
from data.category import Category

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Главная страница
@app.route('/')
def index():
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).all()
    dict = {}
    for el in goods:
        temp = str(db_sess.query(Category).filter(Category.id == el.category).first()).split()
        dict[int(temp[0])] = temp[1]
    return render_template('index.html', goods=goods, categories=dict, title='Каталог')


# Страница товара
@app.route('/catalog/<id>')
def goods_page(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Goods).filter(Goods.id == id).first()
    title = product.title
    return render_template('goods.html', product=product, title=title)


# Страница входа в аккаунт
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Функция выхода из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


# Страница аккаунта
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user, title='Профиль')


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # Если в форме нет ошибок
        if form.password.data != form.password_again.data:  # Если пароли не совпадают
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Пароли на совпадают')
        db_sess = db_session.create_session()
        # Если пользователь с такой почтой существует
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Такой пользователь уже существует')
        # Добавление нового пользователя в базу данных
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            birthdate=form.birthdate.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# Удаление товара из корзины
@app.route('/delete_from_cart/<int:id>')
@login_required
def delete_from_cart(id):
    db_sess = db_session.create_session()
    product = db_sess.query(Cart).filter(Cart.user_id == current_user.id,
                                         Cart.product_id == id).first()
    if product:
        db_sess.delete(product)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/cart')


# Добавление товара в корзину
@app.route('/add_to_cart/<int:id>')
@login_required
def add_to_cart(id):
    db_sess = db_session.create_session()
    cart = Cart(
        user_id=current_user.id,
        product_id=id
    )
    db_sess.add(cart)
    db_sess.commit()
    return redirect(f'/catalog/{id}')


# Страница корзины пользователя
@app.route('/cart')
def cart():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        cart = db_sess.query(Cart).filter(Cart.user_id == current_user.id).all()
        for i in range(len(cart)):
            cart[i] = list(map(int, str(cart[i]).split()))
        for i in range(len(cart)):
            product = db_sess.query(Goods).filter(Goods.id == cart[i][2]).first()
            title = product.title
            price = product.price
            category_id = product.category
            category = db_sess.query(Category).filter(Category.id == category_id).first().name
            # Словарь, который содержит информацию для вывода товара на страницу корзины
            cart[i] = {
                'id': cart[i][0],
                'user_id': cart[i][1],
                'product_id': cart[i][2],
                'title': title,
                'price': price,
                'category': category
            }
        return render_template('cart.html', cart=cart, title='Корзина')
    else:
        return 'Вы не зарегистрированы'


def main():
    db_session.global_init('db/shop.sqlite')  # Соединение с базой данных
    app.register_blueprint(goods_api.blueprint)  # Подключение обработчика для работы с REST-API
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
