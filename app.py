from datetime import date

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from models import db, Expense

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {
        "status": "ok",
        "message": "Budget API running"
    }


@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return jsonify([e.to_dict() for e in expenses])


@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()

    expense = Expense(
        date=date.fromisoformat(data["date"]),
        category=data["category"],
        amount=float(data["amount"]),
        note=data.get("note", "")
    )

    db.session.add(expense)
    db.session.commit()

    return jsonify(expense.to_dict()), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
