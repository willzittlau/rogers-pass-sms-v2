from app import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    status = db.Column(db.String())
    signup_date = db.Column(db.Date())
    def __init__(self, number, status, signup_date):
        self.number = number
        self.status = status
        self.signup_date = signup_date
    def __repr__(self):
        return '<id {}>'.format(self.id)

class Info(db.Model):
    __tablename__ = 'Info'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text())
    status_date = db.Column(db.Date())
    def __init__(self, status, status_date):
        self.status = status
        self.status_date = status_date
    def __repr__(self):
        return '<id {}>'.format(self.id)