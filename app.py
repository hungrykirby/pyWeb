import os

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import time

from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'test2.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    comment = db.relationship("UserComment", backref='user', lazy='dynamic')


    def __init__(self, name, datetime):
        self.name = name
        self.date = datetime

    def __repr__(self):
        return '<Name %r>' % self.name

    def add_comment(self, comment):
        self.comment = comment

class UserComment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime)

    comment_id = db.Column(db.Integer, db.ForeignKey('entries.id'))

    def __init__(self, comment, date, e_id):
        self.comment = comment
        self.date = date
        self.comment_id = e_id

    def __repr__(self):
        return '<comment %r>' % self.comment

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
        print(user.date)
        db.session.add(user)
        db.session.commit()
        return render_template('post.html',
                               name=name, title=title)
    else:
        return redirect(url_for('index'))

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    title = "Yeah"
    if request.method == 'POST':
        user = db.session.query(User).filter_by(name='aho').first()
        comment = request.form['comment']
        print(user.id)
        uComment = UserComment(comment, datetime.now(), user.id)
        print(uComment.comment_id)
        #user.add_comment(uComment)
        db.session.add(uComment)
        #user.comment = uComment
        #db.session.flush()
        db.session.commit()
        return "+++"
    else:
        return redirect(url_for('index'))

@app.route('/add/<comment>')
def add(comment):
    user = db.session.query(User).filter_by(name='aho').first()
    print(user.id)
    uComment = UserComment(comment, datetime.now(), user.id)
    print(uComment.comment_id)
    db.session.add(uComment)
    db.session.commit()
    return comment


@app.route('/look')
def look():
    users = db.session.query(User).all()
    for user in users:
        print(user.id, user.name, user.date, user.comment.count())
        for comment in user.comment:
            print(comment.id, comment.date, comment.comment)
    user_comments = db.session.query(UserComment).all()
    for user_comment in user_comments:
        print(user_comment.id, user_comment.comment, user_comment.date)
    print("user", users)
    return "look"

@app.route('/<num>')
def l(num):
    return str(num)

@app.route("/d")
def delete_db_all():
    users = db.session.query(User).all()
    user_id_arr = []
    for user in users:
        print(user.name)
        user_id_arr.append(user.name)
        db.session.delete(user)
        db.session.commit()
    user_comments = db.session.query(UserComment).all()
    print("---", len(user_comments), "---")
    for user_comment in user_comments:
        user_id_arr.append(user_comment.comment)
        db.session.delete(user_comment)
        db.session.commit()
    return ",".join(user_id_arr)

if __name__ == '__main__':
    #app.debug = True # デバッグモード有効化
    #port = int(os.environ.get('PORT', 5000))
    #app.run(port=port)
    app.run()
