from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
    remaining_change = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/register/user', methods=['POST'])
def register_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password, email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/register/store', methods=['POST'])
def register_store():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_store = Store(store_name=data['store_name'], password=hashed_password, email=data['email'])
    db.session.add(new_store)
    db.session.commit()
    return jsonify({'message': 'Store registered successfully'})

@app.route('/login/user', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'User logged in successfully'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/login/store', methods=['POST'])
def login_store():
    data = request.get_json()
    store = Store.query.filter_by(store_name=data['store_name']).first()
    if store and bcrypt.check_password_hash(store.password, data['password']):
        return jsonify({'message': 'Store logged in successfully'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/transaction', methods=['POST'])
def record_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        user_id=data['user_id'],
        store_id=data['store_id'],
        amount_due=data['amount_due'],
        remaining_change=data['remaining_change']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction recorded successfully'})

@app.route('/credits/user/<int:user_id>', methods=['GET'])
def get_user_credits(user_id):
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    total_credits = sum([transaction.remaining_change for transaction in transactions])
    return jsonify({'total_credits': total_credits})

@app.route('/credits/store/<int:store_id>', methods['GET'])
def get_store_credits(store_id):
    transactions = Transaction.query.filter_by(store_id=store_id).all()
    total_credits = sum([transaction.remaining_change for transaction in transactions])
    return jsonify({'total_credits': total_credits})

@app.route('/notify/user/<int:user_id>', methods=['GET'])
def notify_user(user_id):
    user = User.query.get(user_id)
    if user:
        print(f"Notification for user {user.username}: You have credits available!")
        return jsonify({'message': 'User notified successfully'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/redeem', methods=['POST'])
def redeem_credits():
    data = request.get_json()
    user_id = data['user_id']
    store_id = data['store_id']
    amount_to_redeem = data['amount_to_redeem']
    
    transactions = Transaction.query.filter_by(user_id=user_id, store_id=store_id).all()
    total_credits = sum([transaction.remaining_change for transaction in transactions])
    
    if total_credits >= amount_to_redeem:
        for transaction in transactions:
            if transaction.remaining_change >= amount_to_reem:
                transaction.remaining_change -= amount_to_reem
                db.session.commit()
                return jsonify({'message': 'Credits redeemed successfully'})
            else:
                amount_to_reem -= transaction.remaining_change
                transaction.remaining_change = 0
                db.session.commit()
        return jsonify({'message': 'Credits redeemed successfully'})
    else:
        return jsonify({'message': 'Insufficient credits'}), 400

if __name__ == '__main__':
    app.run(debug=True)