from manast_database.models import Expense, Sale


def get_all_sales(shop):
    sales = Sale.objects.get(shop=shop)
    return sales


def get_all_expenses(shop):
    expenses = Expense.objects.get(shop=shop)
    return expenses
