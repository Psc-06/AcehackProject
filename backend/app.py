from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

DB_NAME = "expenses.db"

# Initialize Database
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
    )
    """)
    conn.commit()
    conn.close()

create_db()

# Add Expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.get_json()
    amount = data["amount"]
    category = data["category"]
    description = data["description"]
    date = data.get("date", datetime.datetime.now().strftime("%Y-%m-%d"))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)", 
                   (amount, category, description, date))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Expense added successfully!"}), 201

# Get All Expenses
@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()

    return jsonify(expenses)

# Delete Expense
@app.route("/delete_expense/<int:id>", methods=["DELETE"])
def delete_expense(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Expense deleted!"})

if __name__ == "__main__":
    app.run(debug=True)
