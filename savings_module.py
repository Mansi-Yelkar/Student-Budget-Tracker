def generate_expense_report(self):
    self.cursor.execute('''
        SELECT category, SUM(amount) as total_expense 
        FROM expenses 
        WHERE user_id = ? 
        GROUP BY category
    ''', (self.current_user_id,))

    expense_data = self.cursor.fetchall()

    categories = [row[0] for row in expense_data]
    amounts = [row[1] for row in expense_data]

    plt.figure(figsize=(10, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')
    plt.title("Expense Distribution")
    plt.show()