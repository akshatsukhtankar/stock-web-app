from . import db
from flask_login import UserMixin


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(10000))
    quantity = db.Column(db.Float)
    purchasePrice = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True))
    current_price = db.Column(db.Float)
    percent_gain = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    stocks = db.relationship('Stock', backref='user')
    cash = db.Column(db.Float)
    cash = 0.0
