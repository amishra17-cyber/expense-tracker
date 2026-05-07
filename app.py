
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create database and table
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            amount      REAL NOT NULL,
            type        TEXT NOT NULL,
            date        TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# HOME PAGE — show all transactions
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = c.fetchall()

    # Calculate totals
    income  = sum(t[2] for t in transactions if t[3] == 'income')
    expense = sum(t[2] for t in transactions if t[3] == 'expense')
    balance = income - expense

    conn.close()
    return render_template('index.html',
                           transactions=transactions,
                           income=income,
                           expense=expense,
                           balance=balance)

# ADD a transaction
@app.route('/add', methods=['POST'])
def add():
    title  = request.form['title']
    amount = request.form['amount']
    type   = request.form['type']
    date   = request.form['date']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (title, amount, type, date) VALUES (?, ?, ?, ?)",
              (title, amount, type, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# DELETE a transaction
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)