def add_income(self):
    add_income_window = tk.Toplevel(self.root)
    add_income_window.title("Add Income")

    tk.Label(add_income_window, text="Amount:").pack()
    amount_entry = tk.Entry(add_income_window)
    amount_entry.pack()

    tk.Label(add_income_window, text="Category:").pack()
    categories = ["Salary", "Freelance", "Scholarship", "Other"]
    income_category = ttk.Combobox(add_income_window, values=categories)
    income_category.pack()

    def save_income():
        amount = float(amount_entry.get())
        category = income_category.get()

        self.cursor.execute('''
            INSERT INTO income 
            (user_id, amount, category, date) 
            VALUES (?, ?, ?, ?)
        ''', (self.current_user_id, amount, category, datetime.now()))

        self.conn.commit()
        messagebox.showinfo("Success", "Income Added Successfully!")
        add_income_window.destroy()

    tk.Button(add_income_window, text="Save", command=save_income).pack()