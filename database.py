import sqlite3

class BudgetDatabase:
    def __init__(self, db_name="budget_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                source TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                goal REAL NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL NOT NULL,
                target_date TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_income(self, amount, source, date):
        self.cursor.execute('INSERT INTO income (amount, source, date) VALUES (?, ?, ?)', (amount, source, date))
        self.conn.commit()

    def add_expense(self, amount, category, date):
        self.cursor.execute('INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)', (amount, category, date))
        self.conn.commit()

    def set_budget_goal(self, category, goal):
        self.cursor.execute('REPLACE INTO budget_goals (category, goal) VALUES (?, ?)', (category, goal))
        self.conn.commit()

    def get_total_income(self):
        self.cursor.execute('SELECT SUM(amount) FROM income')
        return self.cursor.fetchone()[0] or 0

    def get_total_expenses(self):
        self.cursor.execute('SELECT SUM(amount) FROM expenses')
        return self.cursor.fetchone()[0] or 0

    def get_expenses_by_category(self):
        self.cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        return self.cursor.fetchall()

    def add_savings_goal(self, goal_name, target_amount, current_amount, target_date):
        self.cursor.execute('''
            INSERT INTO savings_goals (goal_name, target_amount, current_amount, target_date) 
            VALUES (?, ?, ?, ?)
        ''', (goal_name, target_amount, current_amount, target_date))
        self.conn.commit()

    def update_savings_amount(self, goal_name, new_amount):
        self.cursor.execute('UPDATE savings_goals SET current_amount = ? WHERE goal_name = ?', (new_amount, goal_name))
        self.conn.commit()

    def get_savings_goals(self):
        self.cursor.execute('SELECT * FROM savings_goals')
        return self.cursor.fetchall()

    def reset_database(self):
        tables = ['income', 'expenses', 'budget_goals', 'savings_goals']
        for table in tables:
            self.cursor.execute(f'DELETE FROM {table}')
        self.conn.commit()

    def close(self):
        self.conn.close()
