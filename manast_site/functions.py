from datetime import datetime, timedelta

from manast_database.models import Expense, Sale
from django.shortcuts import redirect
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError


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
