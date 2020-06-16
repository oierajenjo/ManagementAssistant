import collections
from datetime import datetime, timedelta

from django.template.defaulttags import register

from manast_database.models import Expense, Sale


def get_day(weekday, week, year):
    weekday_list = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    num = weekday_list.index(weekday) + 1
    # print(num)
    # n = '-%s' % num
    d = str(year) + '-W' + str(week) + '-' + str(num)
    # print(d)
    date = datetime.strptime(d, "%Y-W%W-%u").date().isoformat()
    # print(date)
    return date


# SALES
def get_all_sales(shop):
    sales = Sale.objects.filter(shop=shop)
    return sales


def benefits_category(sales):
    values = {}
    for sale in sales:
        if sale.item.category.name in values.keys():
            c = values.get(sale.item.category.name)
            v = {sale.item.category.name: float(sale.benefits()) + c}
            values.update(v)
        else:
            v = {sale.item.category.name: float(sale.benefits())}
            values.update(v)
    # print(values)

    values_keys = []
    for bk in values.keys():
        values_keys.append(bk)
    # print(values_keys)
    return values


def benefits_item(sales):
    values = {}
    for sale in sales:
        if sale.item.name in values.keys():
            c = values.get(sale.item.name)
            v = {sale.item.name: float(sale.benefits()) + c}
            values.update(v)
        else:
            v = {sale.item.name: float(sale.benefits())}
            values.update(v)
    # print(values)

    values_keys = []
    for bk in values.keys():
        values_keys.append(bk)
    # print(values_keys)
    return values


def benefits_date(sales):
    values = {}

    for sale in sales:
        day = sale.date.strftime("%Y-%W")
        if day[5:7] == '00':
            monday = sale.date - timedelta(days=sale.date.weekday())
            day = monday.strftime("%Y-%W")

        if str(day[0:4]) in values.keys():
            if str(day[5:7]) in values[str(day[0:4])].keys():
                c = values[str(day[0:4])].get(str(day[5:7]))
                v = {str(day[5:7]): float(sale.benefits()) + c}
                values[str(day[0:4])].update(v)
            else:
                v = {str(day[5:7]): float(sale.benefits())}
                values[str(day[0:4])].update(v)
        else:
            v = {str(day[0:4]): {str(day[5:7]): float(sale.benefits())}}
            values.update(v)

    # print(values)
    week = range(1, 53)
    week_list = []
    for wl in week:
        week_list.append("%02d" % wl)
    print(week_list)
    # print(values.keys())
    final = {}

    for key in values.keys():
        v = {key: []}
        final.update(v)
        for wl in week_list:
            if wl in values[key].keys():
                final[key].append(values[key][wl])
            else:
                final[key].append(0)
            if int(wl) >= datetime.today().isocalendar()[1] - 1 and int(key) == datetime.today().year:
                break
        # print(len(final[key]))
    print(final)
    sort_final = collections.OrderedDict(sorted(final.items(), key=lambda x: x[1]))
    print(sort_final)
    return sort_final


# EXPENSES
def get_all_expenses(shop):
    expenses = Expense.objects.filter(shop=shop)
    return expenses


def expenses_category(expenses):
    values = {}
    for expense in expenses:
        if expense.item.category.name in values.keys():
            c = values.get(expense.item.category.name)
            v = {expense.item.category.name: float(expense.cost) + c}
            values.update(v)
        else:
            v = {expense.item.category.name: float(expense.cost)}
            values.update(v)
    # print(values)

    values_keys = []
    for bk in values.keys():
        values_keys.append(bk)
    # print(values_keys)
    return values


def expenses_item(sales):
    values = {}
    for expense in sales:
        if expense.item.name in values.keys():
            c = values.get(expense.item.name)
            v = {expense.item.name: float(expense.cost) + c}
            values.update(v)
        else:
            v = {expense.item.name: float(expense.cost)}
            values.update(v)
    # print(values)

    values_keys = []
    for bk in values.keys():
        values_keys.append(bk)
    # print(values_keys)
    return values


@register.filter
def get_elements(dictionary, key):
    return dictionary.get(key)
