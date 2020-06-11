from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

file_path = os.path.abspath(os.getcwd()) + "\mydb.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)


# The product fields are Id, Name, Price, Category, CreatedDate, UpdatedDate
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    createdDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updatedDate = db.Column(db.DateTime)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


@app.route('/user', methods=['GET'])
def get_users():
    return ''


@app.route('/user', methods=['POST'])
def add_user():
    return ''


@app.route('/user/<id>', methods=['DELETE'])
def delete_user():
    return ''


@app.route('/user', methods=['GET'])
def get_users():
    return ''


@app.route('/user/<id>', methods=['GET'])
def get_one_user():
    return ''


if __name__ == '__main__':
    app.run(debug=True)