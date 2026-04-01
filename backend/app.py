from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Transaction

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Backend running 🚀"

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json

    if not data.get('title') or not data.get('amount') or not data.get('type'):
        return jsonify({"error": "Missing fields"}), 400

    txn = Transaction(
        title=data['title'],
        amount=float(data['amount']),
        type=data['type']
    )

    db.session.add(txn)
    db.session.commit()

    return jsonify({"message": "Added successfully"})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    txns = Transaction.query.all()
    return jsonify([t.to_dict() for t in txns])

@app.route('/insights', methods=['GET'])
def insights():
    txns = Transaction.query.all()
    total_expense = sum(t.amount for t in txns if t.type == 'expense')

    if total_expense > 5000:
        msg = "bestie… maybe slow down on spending 😭"
    else:
        msg = "you're doing great financially 💅"

    return jsonify({"insight": msg})

if __name__ == "__main__":
    app.run()