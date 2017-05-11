import os

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import time

from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'test2.db')
db_uri = 'sqlite:///{}'.format(db_path)
#app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    def __init__(self, name, datetime):
        self.name = name
        self.date = datetime

    def __repr__(self):
        return '<Name %r>' % self.name

def picked_up():
    messages = [
        "こんにちは、あなたの名前を入力してください",
        "やあ！お名前は何ですか？",
        "あなたの名前を教えてね"
    ]
    return np.random.choice(messages)

@app.route('/')
def index():
    title = "ようこそ"
    message = picked_up()
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        name = request.form['name']
        user = User(name, datetime.now())
        db.session.add(user)
        db.session.commit()
        return render_template('index.html',
                               name=name, title=title)
    else:
        return redirect(url_for('index'))

@app.route('/look')
def look():
    users = db.session.query(User).all()
    for user in users:
        print(user)
    print("from id", db.session.query(User).get(1))
    return str(users)

if __name__ == '__main__':
    #app.debug = True # デバッグモード有効化
    #port = int(os.environ.get('PORT', 5000))
    #app.run(port=port)
    app.run()
