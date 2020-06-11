from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

file_path = os.path.abspath(os.getcwd()) + "\mydb.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'biggestsecretever'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)


# The product fields are Id, Name, Price, Category, CreatedDate, UpdatedDate
class Product(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    createdDate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updatedDate = db.Column(db.DateTime)


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/catalog', methods=['GET'])
@token_required
def get_all_products():
    products = Product.query.all()
    products_data = []
    #Id, Name, Price, Category, CreatedDate, UpdatedDate
    for product in products:
        pr_data = {'id': product.id, 'name': product.name, 'price': product.price, 'category': product.category,
                   'createdDate': product.createdDate, 'updatedDate': product.updatedDate}
        products_data.append(pr_data)

    return jsonify({'All products': products_data})


@app.route('/catalog/<product_id>', methods=['GET'])
@token_required
def get_one_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'No product found!'})

    pr_data = {'id': product.id, 'name': product.name, 'price': product.price, 'category': product.category,
               'createdDate': product.createdDate, 'updatedDate': product.updatedDate}

    return jsonify(pr_data)


@app.route('/catalog/<product_id>', methods=['DELETE'])
@token_required
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message': 'No product found!'})

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted!'})


@app.route('/catalog', methods=['POST'])
@token_required
def add_product(current_user):
    data = request.get_json()

    new_product = Product(name=data['name'], price=data['price'], category=data['category'], updatedDate=datetime.datetime.utcnow)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added!'})


@app.route('/user', methods=['GET'])
@token_required
def get_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()
    users_data = []

    for user in users:
        user_data = {'id': user.id, 'name': user.name, 'password': user.password, 'admin': user.admin}
        users_data.append(user_data)

    return jsonify({'All users': users_data})


@app.route('/user/<user_id>', methods=['GET'])
@token_required
def get_one_user(current_user, user_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'})

    user_data = {'id': user.id, 'name': user.name, 'password': user.password, 'admin': user.admin}

    return jsonify({'user': user_data})


@app.route('/user', methods=['POST'])
@token_required
def add_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'], method='sha256')
    username = data['name']
    new_user = User(name=username, password=hashed_pw, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': username + ' joined!'})


@app.route('/user/<user_id>', methods=['PUT'])
@token_required
def make_admin(current_user, user_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': user.name + ' is now an admin!'})


@app.route('/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'})
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': user.name + ' has been deleted!'})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return jsonify({'message': 'User not found!'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


if __name__ == '__main__':
    app.run(debug=True)
