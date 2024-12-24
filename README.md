<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1>My App</h1>
    </header>
    <main class="main-content">
        <section class="section">
            <h2>Welcome to My App</h2>
            <p>This is a sample application with a design inspired by Square Cash App.</p>
        </section>
    </main>
    <footer class="footer">
        <p>&copy; 2024 My App</p>
    </footer>
</body>
</html>


style.css/
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f0f0;
}

.header {
    background-color: #00d632;
    color: white;
    text-align: center;
    padding: 1rem;
}

.main-content {
    padding: 2rem;
}

.section {
    background-color: white;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 1rem;
    position: fixed;
    bottom: 0;
    width: 100%;
}
Flask==2.1.1
Flask-SQLAlchemy==2.5.1
Flask-Migrate==3.1.0
Flask-Bcrypt==0.7.1
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

@app.route('/credits/store/<int:store_id>', methods=['GET'])
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
            if transaction.remaining_change >= amount_to_redeem:
                transaction.remaining_change -= amount_to_redeem
                db.session.commit()
                return jsonify({'message': 'Credits redeemed successfully'})
            else:
                amount_to_redeem -= transaction.remaining_change
                transaction.remaining_change = 0
                db.session.commit()
        return jsonify({'message': 'Credits redeemed successfully'})
    else:
        return jsonify({'message': 'Insufficient credits'}), 400

if __name__ == '__main__':
    app.run(debug=True)
{
  "name": "change-management-app",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/jest-dom": "^5.11.4",
    "@testing-library/react": "^11.1.0",
    "@testing-library/user-event": "^12.1.10",
    "axios": "^0.21.1",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-router-dom": "^5.2.0",
    "react-scripts": "4.0.3",
    "web-vitals": "^1.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}

import React, { useState } from 'react';
import { getUserCredits, getStoreCredits } from '../services/api';

const Credits = () => {
  const [userId, setUserId] = useState('');
  const [storeId, setStoreId] = useState('');
  const [credits, setCredits] = useState(null);

  const handleGetUserCredits = async () => {
    try {
      const response = await getUserCredits(userId);
      setCredits(response.data.total_credits);
    } catch (error) {
      alert('Failed to fetch user credits');
    }
  };

  const handleGetStoreCredits = async () => {
    try {
      const response = await getStoreCredits(storeId);
      setCredits(response.data.total_credits);
    } catch (error) {
      alert('Failed to fetch store credits');
    }
  };

  return (
    <div>
      <h2>View Credits</h2>
      <input type="text" placeholder="User ID" value={userId} onChange={(e) => setUserId(e.target.value)} />
      <button onClick={handleGetUserCredits}>Get User Credits</button>
      <input type="text" placeholder="Store ID" value={storeId} onChange={(e) => setStoreId(e.target.value)} />
      <button onClick={handleGetStoreCredits}>Get Store Credits</button>
      {credits !== null && (
        <div>
          <h3>Total Credits: {credits}</h3>
        </div>
      )}
    </div>
  );
};

export default Credits;