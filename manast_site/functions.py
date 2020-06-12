from datetime import datetime

from manast_database.models import Expense, Sale


def get_all_sales(shop):
    sales = Sale.objects.filter(shop=shop)
    return sales


def get_all_expenses(shop):
    expenses = Expense.objects.filter(shop=shop)
    return expenses


def get_day(weekday, week, year):
    weekday_list = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    num = weekday_list.index(weekday)
    # n = '-%s' % num
    d = str(year) + '-W' + str(week) + '-' + str(num)
    date = datetime.strptime(d, "%Y-W%W-%w").date()
    return date
