import sqlite3
from tabulate import tabulate
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Database setup and connection
def create_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        amount REAL,
                        category TEXT,
                        date TEXT
                     )''')
    conn.commit()
    conn.close()

def add_expense(amount, category, date):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                   (amount, category, date))
    conn.commit()
    conn.close()

def view_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    print(tabulate(rows, headers=["ID", "Amount", "Category", "Date"], tablefmt="grid"))

# Main CLI menu
def main():
    create_db()
    while True:
        print("\nExpense Tracker CLI")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Generate Summary")
        print("4. Export Report")
        print("5. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date = input("Enter date (YYYY-MM-DD) or leave empty for today: ")
            date = date if date else datetime.now().strftime("%Y-%m-%d")
            add_expense(amount, category, date)
            print("Expense added!")
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            generate_summary()
        elif choice == '4':
            export_report()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
