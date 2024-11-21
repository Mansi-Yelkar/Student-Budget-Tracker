def add_expense(self):
    add_expense_window = tk.Toplevel(self.root)
    add_expense_window.title("Add Expense")

    expense_categories = [
        "Groceries", "Transportation", "Education",
        "Rent", "Entertainment", "Utilities", "Other"
    ]

    tk.Label(add_expense_window, text="Amount:").pack()
    amount_entry = tk.Entry(add_expense_window)
    amount_entry.pack()

    tk.Label(add_expense_window, text="Category:").pack()
    expense_category = ttk.Combobox(add_expense_window, values=expense_categories)
    expense_category.pack()

    tk.Label(add_expense_window, text="Description:").pack()
    description_entry = tk.Entry(add_expense_window)
    description_entry.pack()

    def save_expense():
        amount = float(amount_entry.get())
        category = expense_category.get()
        description = description_entry.get()

        self.cursor.execute('''
            INSERT INTO expenses 
            (user_id, amount, category, description, date) 
            VALUES (?, ?, ?, ?, ?)
        ''', (self.current_user_id, amount, category, description, datetime.now()))

        self.conn.commit()
        messagebox.showinfo("Success", "Expense Added Successfully!")
        add_expense_window.destroy()

    tk.Button(add_expense_window, text="Save", command=save_expense).pack()