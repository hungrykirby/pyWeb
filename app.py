import os

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import time

from flask import Flask, render_template, request, redirect, url_for
#import tables

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'test2.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    comment = db.relationship("Message", backref='user', lazy='dynamic')


    def __init__(self, name, datetime):
        self.name = name
        self.date = datetime

    def __repr__(self):
        return '<Name %r>' % self.name

class Message(db.Model):
    __tablename__='message'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime)

    comment_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, comment, date, e_id):
        self.comment = comment
        self.date = date
        self.comment_id = e_id

    def __repr__(self):
        return '<comment %r>' % self.comment


@app.route('/')
def index():
    title = "ようこそ"
    message = "データベースに追加するidとmessageを教えてね"
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "名前を追加します"
    if request.method == 'POST':
        name = request.form['name']
        user = User(name, datetime.now())
        db.session.add(user)
        db.session.commit()
        return render_template('post.html',
                               name=name, title=title)
    else:
        return redirect(url_for('index'))

@app.route('/message', methods=['GET', 'POST'])
def comment():
    title = "メッセージを投稿するページです"
    if request.method == 'POST':
        message_content = request.form['message']
        my_id = request.form['id']
        user = db.session.query(User).filter_by(id=my_id).first()
        if user != None and user != []:
            message = Message(message_content, datetime.now(), user.id)
            db.session.add(message)
            print("finish adding")
            #return "finish adding"
        else:
            print("No add")
            #return "No add"
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/look')
def look():
    users = db.session.query(User).all()
    for user in users:
        print(user.id, user.name, user.date)
        #print(user.__dict__["name"])
        #for m in user.comment:
        #    print(m.id, m.date, m.comment)
    ms = db.session.query(Message).all()
    print("ms", ms)
    for m in ms:
        print(m.id, m.comment, m.date)
    return "ユーザとメッセージを確認できます"

@app.route("/delete")
def delete_db_all():
    users = db.session.query(User).all()
    user_id_arr = []
    for user in users:
        print(user.name)
        user_id_arr.append(user.name)
        db.session.delete(user)
        db.session.commit()
    message = db.session.query(Message).all()
    print("---", len(message), "---")
    for m in message:
        db.session.delete(m)
        db.session.commit()
    return ",".join(user_id_arr)

if __name__ == '__main__':
    #app.debug = True # デバッグモード有効化
    #port = int(os.environ.get('PORT', 5000))
    #app.run(port=port)
    app.run()
