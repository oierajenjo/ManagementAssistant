import collections
from datetime import datetime, timedelta, date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import rrule
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
from sklearn.metrics import mean_squared_error

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

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
    sales = Sale.objects.filter(shop=shop).order_by('date')
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


def benefits_week(sales):
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
    # print(week_list)
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
    # print(final)
    context = {
        "final": final,
        "week_list": week_list
    }
    return context


def benefits_per_day(sales):
    values = {}
    dates = {}

    for sale in sales:
        day = sale.date.strftime("%d-%m-%Y")
        y = str(day[-4:])
        d = str(day[:-5])

        if y in values.keys():  # Year
            if d in values[y].keys():  # Day in Year
                c = values[y].get(d)
                v = {d: float(sale.benefits()) + c}
                values[y].update(v)
            else:
                v = {d: float(sale.benefits())}
                values[y].update(v)
                dates[y].append(d)
        else:
            v = {y: {d: float(sale.benefits())}}
            values.update(v)
            dt = {y: [d]}
            dates.update(dt)

    # print(values)
    # print(dates)

    sdate = date(2020, 1, 1)  # start date
    edate = date(2020, 12, 31)  # end date

    delta = edate - sdate  # as timedelta
    days = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        days.append(day.strftime("%d-%m"))
    final = {}
    # print(days)

    for key in values.keys():
        v = {key: []}
        final.update(v)
        for d in days:
            if d in dates[key]:
                final[key].append(values[key][d])
            elif datetime.strptime(d + "-2020", "%d-%m-%Y") < datetime.strptime(str(dates[key][0]) + "-2020", "%d-%m-%Y"):
                final[key].append(0)

        # print(len(final[key]))

    # print(final)
    # print(dates)

    context = {
        "final": final,
        "days": days
    }
    return context


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

# def get_stationarity(timeseries):
#     # rolling statistics
#     rolling_mean = timeseries.rolling(window=12).mean()
#     rolling_std = timeseries.rolling(window=12).std()
#
#     # rolling statistics plot
#     original = plt.plot(timeseries, color='blue', label='Original')
#     mean = plt.plot(rolling_mean, color='red', label='Rolling Mean')
#     std = plt.plot(rolling_std, color='black', label='Rolling Std')
#     plt.legend(loc='best')
#     plt.title('Rolling Mean & Standard Deviation')
#     plt.show(block=False)
#
#     # Dickey–Fuller test:
#     result = adfuller(timeseries['Sales'])
#     print('ADF Statistic: {}'.format(result[0]))
#     print('p-value: {}'.format(result[1]))
#     print('Critical Values:')
#     for key, value in result[4].items():
#         print('\t{}: {}'.format(key, value))


# PREDICTIONS
# def arima_prediction(sales):
#
#     ben = []
#     dates = []
#     for sale in sales:
#         day = str(sale.date.strftime("%Y-%m-%d"))
#         if day not in dates:
#             ben.append(float(sale.benefits()))
#             dates.append(day)
#         else:
#             v = ben[dates.index(day)]
#             ben[dates.index(day)] = v + float(sale.benefits())
#
#     plt.xlabel('Date')
#     plt.ylabel('Number of air passengers')
#     plt.plot([dates, ben])
#     plt.show()
#
#     # # print(h)
#     # # print(len(h))
#     # # print(len(dates))
#     # # print(dates)
#     # size = int(len(h) * 0.66)
#     # print(size)
#     # # size = int(len(h))
#     # train, test = h[0:size], h[size:len(h)]
#     # print(train)
#     # print(test)
#     # history = [x for x in train]
#     # print(history)
#     # predictions = list()
#     # for t in range(len(test)):
#     #     model = ARIMAResults
#     #     model = ARIMA(history, order=(5, 1, 0))
#     #     model_fit = model.fit(disp=0)
#     #     output = model_fit.forecast(steps=1, exog=None, alpha=0.05)
#     #     yhat = output[0]
#     #     predictions.append(yhat)
#     #     obs = test[t]
#     #     history.append(obs)
#     #     print('predicted=%f, expected=%f' % (yhat, obs))
#     # error = mean_squared_error(test, predictions)
#     # print('Test MSE: %.3f' % error)
#     # # plot
#     # print(len(test))
#     # print(len(predictions))
#     # print(len(dates))
#     # ax = plt.gca()
#     # formatter = mdates.DateFormatter("%Y-%m-%d")
#     # ax.xaxis.set_major_formatter(formatter)
#     # locator = mdates.DayLocator()
#     # ax.xaxis.set_major_locator(locator)
#     # plt.plot(dates, test, label="Results")
#     # plt.plot(dates, predictions, label="Predictions")
#     #
#     # plt.legend()
#     # plt.show()
#     #
#     # # pyplot.plot(test)
#     # # pyplot.plot(predictions, color='red')
#     # # pyplot.xticks([test, predictions], dates)
#     # # pyplot.show()
#     # # pyplot.savefig("plot.png")
#     context = {
#         # "predictions": predictions,
#         # "error": error,
#         # "history": history,
#         "dates": dates
#     }
#     return context
