class ExpenseMarkup:
    def __init__(self, cost_price, total_expenses, implementation_period):
        self.cost_price = cost_price
        self.total_expenses = total_expenses
        self.implementation_period = implementation_period

    def get_cost(self):
        return self.cost_price

    def get_expenses(self):
        return self.total_expenses

    def get_implementation_period(self):
        return self.implementation_period

    def get_expense_markup(self):
        rec_markup = self.total_expenses / (self.implementation_period * self.cost_price) * 100
        return rec_markup


m1 = ExpenseMarkup(30, 200, 2)

print(m1.get_expense_markup())
