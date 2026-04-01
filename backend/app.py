from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------------
# MODEL
# -------------------------------
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)

# -------------------------------
# INIT DB
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# ROUTES
# -------------------------------

# Home route (for testing)
@app.route("/")
def home():
    return "Backend running"

# Get all transactions
@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()
    result = []

    for t in transactions:
        result.append({
            "id": t.id,
            "title": t.title,
            "amount": t.amount,
            "type": t.type
        })

    return jsonify(result)

# Add transaction
@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()

    title = data.get("title")
    amount = data.get("amount")
    type_ = data.get("type")

    # Validation
    if not title or amount is None or not type_:
        return jsonify({"error": "Missing fields"}), 400

    try:
        amount = float(amount)
    except:
        return jsonify({"error": "Invalid amount"}), 400

    new_transaction = Transaction(
        title=title,
        amount=amount,
        type=type_
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added"})

# Insight route
@app.route("/insights", methods=["GET"])
def get_insights():
    transactions = Transaction.query.all()

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")

    if total_expense > total_income:
        insight = "Your expenses are higher than your income. Consider reducing spending."
    elif total_income > total_expense:
        insight = "Good job! You are saving money."
    else:
        insight = "Your income and expenses are balanced."

    return jsonify({"insight": insight})

# Reset data (for demo/testing)
@app.route("/reset", methods=["DELETE"])
def reset_data():
    Transaction.query.delete()
    db.session.commit()
    return jsonify({"message": "All data cleared"})

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run()