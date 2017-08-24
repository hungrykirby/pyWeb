from app import db

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

'''
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
'''
