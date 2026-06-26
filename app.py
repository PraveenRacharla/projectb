from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
DB = "expenses.db"
CORS(app)

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# INIT DB
def init_db():
    conn = connect()
    with open("schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

init_db()

# HOME ROUTE (MUST BE HERE)
@app.route("/")
def home():
    return {
        "status": "ok",
        "message": "Budget API is running",
        "endpoints": ["/expenses"]
    }

# GET ALL EXPENSES
@app.route("/expenses", methods=["GET"])
def get_expenses():
    conn = connect()
    rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])

# ADD EXPENSE
@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.json

    conn = connect()
    conn.execute(
        "INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
        (data["date"], data["category"], data["amount"], data.get("note", ""))
    )
    conn.commit()
    conn.close()

    return {"status": "success"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
