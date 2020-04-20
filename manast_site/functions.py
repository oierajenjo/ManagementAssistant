from manast_database.models import Expense, Sale


def get_all_sales(shop):
    sales = Sale.objects.filter(shop=shop)
    return sales


def get_all_expenses(shop):
    expenses = Expense.objects.filter(shop=shop)
    return expenses
