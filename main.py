import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import BudgetDatabase

class FunkyBudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Budget Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg='#ffe4b5')
        self.root.minsize(800, 500)

        # Initialize database
        self.db = BudgetDatabase()

        # Create main container with a funky style
        self.create_main_container()

    def create_main_container(self):
        self.main_frame = tk.Frame(self.root, bg='#ffe4b5')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.nav_frame = tk.Frame(self.main_frame, bg='#ffdab9')
        self.nav_frame.pack(side='left', fill='y', padx=10, pady=10)

        self.content_frame = tk.Frame(self.main_frame, bg='#fff5ee')
        self.content_frame.pack(side='right', expand=True, fill='both', padx=10, pady=10)

        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("💰 Add Income", self.show_income_section),
            ("🛒 Add Expense", self.show_expense_section),
            ("🎯 Budget Goals", self.show_budget_goals),
            ("📊 Reports", self.show_reports),
            ("💼 Savings Tracker", self.show_savings_tracker)
        ]

        for text, command in nav_buttons:
            btn = tk.Button(self.nav_frame, text=text, width=18, command=command,
                            font=('Comic Sans MS', 10, 'bold'), bg='#ff69b4', fg='white')
            btn.pack(pady=5, padx=5)

        # Show initial dashboard
        self.show_dashboard()

    def show_dashboard(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        dashboard_frame = tk.Frame(self.content_frame, bg='#fff5ee')
        dashboard_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Add reset database button
        reset_btn = tk.Button(dashboard_frame, text="Reset Database", bg='#ff4500', fg='white',
                              font=('Comic Sans MS', 10, 'bold'), command=self.reset_database)
        reset_btn.pack(anchor='ne', pady=5, padx=5)

        total_income = self.db.get_total_income()
        total_expenses = self.db.get_total_expenses()
        remaining_balance = total_income - total_expenses

        summary_sections = [
            ("💰 Total Income", f"${total_income:.2f}"),
            ("🛒 Total Expenses", f"${total_expenses:.2f}"),
            ("💼 Remaining Balance", f"${remaining_balance:.2f}")
        ]

        for label, value in summary_sections:
            section_frame = tk.Frame(dashboard_frame, bg='#fff5ee', relief='groove', borderwidth=2)
            section_frame.pack(fill='x', pady=5, padx=10)

            tk.Label(section_frame, text=label, font=('Comic Sans MS', 12, 'bold'), bg='#fff5ee').pack(side='left', padx=10)
            tk.Label(section_frame, text=value, font=('Comic Sans MS', 12), fg='green', bg='#fff5ee').pack(side='right', padx=10)

    def show_income_section(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        income_frame = tk.Frame(self.content_frame, bg='#fff5ee')
        income_frame.pack(expand=True, fill='both', padx=10, pady=10)

        tk.Label(income_frame, text="💰 Add Income", font=('Comic Sans MS', 16, 'bold'), bg='#fff5ee').pack(pady=10)

        amount_entry = self.create_entry(income_frame, "Amount")
        source_entry = self.create_combobox(income_frame, "Source", ['Part-time Job', 'Scholarship', 'Stipend', 'Other'])

        add_income_btn = tk.Button(income_frame, text="Add Income", bg='#ff1493', fg='white', font=('Comic Sans MS', 10, 'bold'),
                                   command=lambda: self.add_income(amount_entry, source_entry))
        add_income_btn.pack(pady=10)

    def show_expense_section(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        expense_frame = tk.Frame(self.content_frame, bg='#fff5ee')
        expense_frame.pack(expand=True, fill='both', padx=10, pady=10)

        tk.Label(expense_frame, text="🛒 Add Expense", font=('Comic Sans MS', 16, 'bold'), bg='#fff5ee').pack(pady=10)

        amount_entry = self.create_entry(expense_frame, "Amount")
        category_entry = self.create_combobox(expense_frame, "Category", ['Food', 'Transport', 'Books', 'Supplies', 'Entertainment', 'Other'])

        add_expense_btn = tk.Button(expense_frame, text="Add Expense", bg='#ff1493', fg='white', font=('Comic Sans MS', 10, 'bold'),
                                    command=lambda: self.add_expense(amount_entry, category_entry))
        add_expense_btn.pack(pady=10)

    def show_budget_goals(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        budget_frame = tk.Frame(self.content_frame, bg='#fff5ee')
        budget_frame.pack(expand=True, fill='both', padx=10, pady=10)

        tk.Label(budget_frame, text="🎯 Set Budget Goals", font=('Comic Sans MS', 16, 'bold'), bg='#fff5ee').pack(pady=10)

        budget_categories = ['Food', 'Transport', 'Books', 'Entertainment']
        entries = {}

        for category in budget_categories:
            entries[category] = self.create_entry(budget_frame, f"{category} Budget")

        set_budget_btn = tk.Button(budget_frame, text="Set Budget Goals", bg='#ff1493', fg='white', font=('Comic Sans MS', 10, 'bold'),
                                   command=lambda: self.set_budget_goals(entries))
        set_budget_btn.pack(pady=10)

    def show_reports(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        reports_frame = tk.Frame(self.content_frame, bg='#fff5ee')
        reports_frame.pack(expand=True, fill='both', padx=10, pady=10)

        tk.Label(reports_frame, text="📊 Financial Reports", font=('Comic Sans MS', 16, 'bold'), bg='#fff5ee').pack(pady=10)

        # Example report: Expenses by Category
        expenses_by_category = self.db.get_expenses_by_category()
        for category, total in expenses_by_category:
            tk.Label(reports_frame, text=f"{category}: ${total:.2f}", font=('Comic Sans MS', 12), bg='#fff5ee').pack(pady=2)

    def show_savings_tracker(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        savings_frame = tk.Frame(self.content_frame, bg='#fff5ee')
        savings_frame.pack(expand=True, fill='both', padx=10, pady=10)

        tk.Label(savings_frame, text="💼 Savings Tracker", font=('Comic Sans MS', 16, 'bold'), bg='#fff5ee').pack(pady=10)

        # Add new savings goal section
        goal_frame = tk.Frame(savings_frame, bg='#fff5ee')
        goal_frame.pack(fill='x', pady=10)

        goal_name = self.create_entry(goal_frame, "Goal Name")
        target_amount = self.create_entry(goal_frame, "Target Amount ($)")
        current_amount = self.create_entry(goal_frame, "Current Amount ($)")
        target_date = self.create_entry(goal_frame, "Target Date (YYYY-MM-DD)")

        def add_goal():
            try:
                name = goal_name.get()
                target = float(target_amount.get())
                current = float(current_amount.get())
                date = target_date.get()
                self.db.add_savings_goal(name, target, current, date)
                messagebox.showinfo("Success", "Savings goal added!")
                self.show_savings_tracker()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for amounts")

        add_btn = tk.Button(goal_frame, text="Add Savings Goal", bg='#ff1493', fg='white',
                            font=('Comic Sans MS', 10, 'bold'), command=add_goal)
        add_btn.pack(pady=10)

        # Display existing savings goals
        goals_list_frame = tk.Frame(savings_frame, bg='#fff5ee')
        goals_list_frame.pack(fill='both', expand=True, pady=10)

        tk.Label(goals_list_frame, text="Current Savings Goals",
                 font=('Comic Sans MS', 14, 'bold'), bg='#fff5ee').pack(pady=5)

        for goal in self.db.get_savings_goals():
            goal_item = tk.Frame(goals_list_frame, bg='#ffd700', relief='raised', bd=2)
            goal_item.pack(fill='x', pady=5, padx=10)

            tk.Label(goal_item, text=f"Goal: {goal[1]}", bg='#ffd700').pack(side='left', padx=5)
            tk.Label(goal_item, text=f"Progress: ${goal[3]}/{goal[2]}", bg='#ffd700').pack(side='right', padx=5)

    def create_entry(self, parent, label_text):
        frame = tk.Frame(parent, bg='#fff5ee')
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text=label_text, font=('Comic Sans MS', 10), bg='#fff5ee').pack(side='left', padx=10)
        entry = tk.Entry(frame, width=30)
        entry.pack(side='right', padx=10)
        return entry

    def create_combobox(self, parent, label_text, values):
        frame = tk.Frame(parent, bg='#fff5ee')
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text=label_text, font=('Comic Sans MS', 10), bg='#fff5ee').pack(side='left', padx=10)
        combobox = ttk.Combobox(frame, values=values, width=28)
        combobox.pack(side='right', padx=10)
        return combobox

    def add_income(self, amount_entry, source_entry):
        try:
            amount = float(amount_entry.get())
            source = source_entry.get()
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.add_income(amount, source, date)
            messagebox.showinfo("Success", "Income added successfully!")
            self.show_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered. Please enter a number.")

    def add_expense(self, amount_entry, category_entry):
        try:
            amount = float(amount_entry.get())
            category = category_entry.get()
            date = datetime.now().strftime("%Y-%m-%d")
            self.db.add_expense(amount, category, date)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.show_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered. Please enter a number.")

    def set_budget_goals(self, entries):
        for category, entry in entries.items():
            try:
                goal = float(entry.get())
                self.db.set_budget_goal(category, goal)
                messagebox.showinfo("Success", f"Budget goal set for {category}!")
            except ValueError:
                messagebox.showerror("Error", f"Invalid goal for {category}. Please enter a number.")

    def reset_database(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the database? This will delete all data."):
            self.db.reset_database()
            messagebox.showinfo("Success", "Database has been reset!")
            self.show_dashboard()

# Main Application
def main():
    root = tk.Tk()
    app = FunkyBudgetTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
