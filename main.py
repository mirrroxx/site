from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("main.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/breakfast')
def breakfast():
    return render_template("breakfast.html")


if __name__ == '__main__':
    app.run(debug=True)
