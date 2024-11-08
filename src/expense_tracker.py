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


def generate_summary():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    # Summarize by category
    cursor.execute('''SELECT category, SUM(amount) FROM expenses GROUP BY category''')
    category_summary = cursor.fetchall()
    
    # Summarize by month
    cursor.execute('''SELECT strftime('%Y-%m', date) as month, SUM(amount) 
                      FROM expenses GROUP BY month''')
    monthly_summary = cursor.fetchall()
    
    conn.close()

    print("\nSummary by Category:")
    print(tabulate(category_summary, headers=["Category", "Total Amount"], tablefmt="grid"))

    print("\nSummary by Month:")
    print(tabulate(monthly_summary, headers=["Month", "Total Amount"], tablefmt="grid"))

def export_report():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    # Export to CSV
    with open('expenses_report.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["ID", "Amount", "Category", "Date"])
        csvwriter.writerows(rows)
    print("Report exported as CSV: expenses_report.csv")

    # Export to PDF
    pdf_file = 'expenses_report.pdf'
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.drawString(100, 750, "Expense Report")
    
    # Table in PDF
    y = 700
    c.drawString(50, y, "ID    Amount    Category    Date")
    for row in rows:
        y -= 20
        c.drawString(50, y, f"{row[0]}    {row[1]}    {row[2]}    {row[3]}")
        if y < 50:
            c.showPage()  # Add a new page if data goes beyond one page
            y = 750
    
    c.save()
    print("Report exported as PDF: expenses_report.pdf")


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
