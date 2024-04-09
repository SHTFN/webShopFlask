from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # TODO: разобраться с эти ключом


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/user')
def user():
    return 'user page'


def main():
    app.run()


if __name__ == '__main__':
    main()
