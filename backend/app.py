from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------------------
# DATABASE CONFIG
# -------------------------------
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
# INIT DATABASE
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# ROUTES
# -------------------------------

# Health check
@app.route("/")
def home():
    return "Backend running"

# -------------------------------
# GET ALL TRANSACTIONS
# -------------------------------
@app.route("/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "amount": t.amount,
            "type": t.type
        } for t in transactions
    ])

# -------------------------------
# ADD TRANSACTION
# -------------------------------
@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()

    title = data.get("title")
    amount = data.get("amount")
    type_ = data.get("type")

    # Validation
    if not title or amount is None or not type_:
        return jsonify({"error": "Missing fields"}), 400

    if type_ not in ["income", "expense"]:
        return jsonify({"error": "Invalid type"}), 400

    try:
        amount = float(amount)
    except:
        return jsonify({"error": "Amount must be a number"}), 400

    new_transaction = Transaction(
        title=title,
        amount=amount,
        type=type_
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added"}), 201

# -------------------------------
# DELETE SINGLE TRANSACTION
# -------------------------------
@app.route("/transactions/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    transaction = Transaction.query.get(id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted"})

# -------------------------------
# RESET ALL DATA
# -------------------------------
@app.route("/reset", methods=["DELETE"])
def reset_data():
    Transaction.query.delete()
    db.session.commit()

    return jsonify({"message": "All data cleared"})

# -------------------------------
# INSIGHTS
# -------------------------------
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

    return jsonify({
        "income": total_income,
        "expense": total_expense,
        "insight": insight
    })

# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run()