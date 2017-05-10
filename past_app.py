from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import os
from flask.ext.sqlalchemy import SQLAlchemy
import MySQLdb

conn = MySQLdb.connect(
        user='katsuki',
        passwd='8Lapis6Luna',
        host='localhost',
        db='k_testdb',
        port=3306
    )
c = conn.cursor()
sql = 'create table names (name varchar(32))'
#c.execute(sql)

app = Flask(__name__)

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
        sql = 'insert into names values (%s)'
        c.execute(sql, (name,))
        conn.commit()
        return render_template('index.html',
                               name=name, title=title)
    else:
        return redirect(url_for('index'))

@app.route('/look')
def look():
    sql = 'select * from names'
    c.execute(sql)
    for row in c.fetchall():
        print('Name:', row[0])
    return 'datas'

if __name__ == '__main__':
    #app.debug = True # デバッグモード有効化
    #port = int(os.environ.get('PORT', 5000))
    #app.run(port=port)
    app.run()
