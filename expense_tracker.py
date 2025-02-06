import csv
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# File to store expenses
FILE_NAME = "expenses.csv"

# Ensure file exists
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Amount", "Category", "Description"])

def add_expense(amount, category, description):
    date = datetime.today().strftime('%Y-%m-%d')
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, description])
    messagebox.showinfo("Success", "Expense added successfully!")

def view_expenses():
    win = tk.Toplevel()
    win.title("View Expenses")
    tree = ttk.Treeview(win, columns=("Date", "Amount", "Category", "Description"), show='headings')
    for col in ("Date", "Amount", "Category", "Description"):
        tree.heading(col, text=col)
    tree.pack(expand=True, fill='both')
    
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tree.insert("", "end", values=row)

def analyze_expenses():
    category_totals = {}
    total = 0
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            amount = float(row[1])
            category = row[2]
            total += amount
            category_totals[category] = category_totals.get(category, 0) + amount
    
    result = f"Total Expenses: ${total:.2f}\n"
    for category, amount in category_totals.items():
        result += f"{category}: ${amount:.2f}\n"
    messagebox.showinfo("Expense Analysis", result)

def main():
    initialize_file()
    root = tk.Tk()
    root.title("Expense Tracker")
    
    tk.Label(root, text="Amount").grid(row=0, column=0)
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=0, column=1)
    
    tk.Label(root, text="Category").grid(row=1, column=0)
    category_entry = tk.Entry(root)
    category_entry.grid(row=1, column=1)
    
    tk.Label(root, text="Description").grid(row=2, column=0)
    description_entry = tk.Entry(root)
    description_entry.grid(row=2, column=1)
    
    tk.Button(root, text="Add Expense", command=lambda: add_expense(amount_entry.get(), category_entry.get(), description_entry.get())).grid(row=3, column=0, columnspan=2)
    tk.Button(root, text="View Expenses", command=view_expenses).grid(row=4, column=0, columnspan=2)
    tk.Button(root, text="Analyze Expenses", command=analyze_expenses).grid(row=5, column=0, columnspan=2)
    tk.Button(root, text="Exit", command=root.quit).grid(row=6, column=0, columnspan=2)
    
    root.mainloop()

if __name__ == "__main__":
    main()
