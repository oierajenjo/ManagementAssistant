import csv
from datetime import datetime, timedelta, date
import numpy
from django.template.defaulttags import register
from django.utils.translation import gettext_lazy as _
from matplotlib import pyplot
from pandas import read_csv
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.ar_model import AutoReg, AutoRegResults
from statsmodels.tsa.arima_model import ARMA
from math import sqrt
from sklearn.metrics import mean_squared_error

from manast_database.models import Expense, Sale

register_matplotlib_converters()


def get_day(weekday, week, year):
    weekday_list = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
    num = weekday_list.index(weekday) + 1
    # print(num)
    # n = '-%s' % num
    d = str(year) + '-W' + str(week) + '-' + str(num)
    # print(d)
    day = datetime.strptime(d, "%Y-W%W-%u").date().isoformat()
    # print(date)
    return day


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
            elif datetime.strptime(d + "-2020", "%d-%m-%Y") < datetime.strptime(str(dates[key][0]) + "-2020",
                                                                                "%d-%m-%Y"):
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


def tuple_to_list(sales):
    values = []
    dates = []
    tmp = {}
    for sale in sales:
        day = str(sale.date.strftime("%Y-%m-%d"))
        if day not in tmp.keys():
            v = {day: float(sale.benefits())}
            tmp.update(v)
        else:
            c = tmp.get(day)
            v = {day: float(sale.benefits()) + c}
            tmp.update(v)

    for k in tmp.keys():
        values.append(float(tmp.get(k)))
        dates.append(k)

    return values, dates, tmp


def average_of_list(num):
    sum = 0
    for t in num:
        sum = sum + t

    avg = sum / len(num)
    return float(avg)


def pred_by_mean(sales):
    values, dates, tmp = tuple_to_list(sales)
    # print(value)
    # print(tmp)
    # print(dates)
    # pred = value[:len(value) - 8]
    pred = []
    pred_dates = []
    for i in range(len(values)):
        if i != 0:
            pred.append(average_of_list(values[:i]))
            pred_dates.append(dates[i])
        else:
            pred.append(float(values[i]))
            pred_dates.append(dates[i])

    v = average_of_list(values)
    for i in range(7):
        pred.append(v)
        day = datetime.strptime(pred_dates[len(pred_dates) - 1], "%Y-%m-%d") + timedelta(days=1)
        pred_dates.append(str(day.strftime("%Y-%m-%d")))

    # print(len(dates))
    # print(dates[len(dates) - 1])
    # print(len(values))
    # print(pred_dates[len(pred_dates) - 1])
    # print(len(pred))

    # plt.plot(dates, values, label=_("Sales"))
    # plt.plot(pred_dates, pred, label=_("Prediction"))
    # plt.title('Benefits prediction by mean')
    # plt.legend()
    # plt.show()

    # return plt, pred_dates, values, pred
    return pred_dates, values, pred


def sales_to_csv(sales):
    values, dates, tmp = tuple_to_list(sales)

    values = []
    for tk in tmp.keys():
        pmp = {'Date': str(tk), 'Benefits': tmp[tk]}
        values.append(pmp)

    # print(values)
    csv_columns = ['Date', 'Benefits']

    # csv_file = '{}predictions/predictions.csv'.format(settings.STATIC_URL)
    csv_file = "manast_site/static/predictions/sales.csv"

    return csv_file, csv_columns, values


# create a difference transform of the dataset
def difference(dataset):
    diff = list()
    for i in range(1, len(dataset)):
        value = dataset[i] - dataset[i - 1]
        diff.append(value)
    return numpy.array(diff)


# Make a prediction give regression coefficients and lag obs
def predict(coef, history):
    yhat = coef[0]
    for i in range(1, len(coef)):
        yhat += coef[i] * history[-i]
    return yhat


def pred_forecast(sales):
    # values, dates, tmp = tuple_to_list(sales)
    csv_file, csv_columns, values = sales_to_csv(sales)

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in values:
                writer.writerow(data)
    except IOError:
        print("I/O error")

    series = read_csv(csv_file, header=0, index_col=0)
    # print(series.head())
    # series.plot()
    # pyplot.show()

    x = difference(series.values)
    size = int(len(x) * 0.66)
    train, test = x[0:size], x[size:]
    # train autoregression

    # AR
    window = 7
    model_ar = AutoReg(train, lags=window)
    model_fit_ar = model_ar.fit()

    # save model to file
    model_fit_ar.save("manast_site/static/predictions/ar_model.pkl")
    # save the differenced dataset
    numpy.save("manast_site/static/predictions/ar_data.npy", x)
    # save the last ob
    numpy.save("manast_site/static/predictions/ar_obs.npy", [series.values[-1]])

    # save coefficients
    coef = model_fit_ar.params
    numpy.save("manast_site/static/predictions/ar_man_model.npy", coef)
    # save lag
    lag = x[-window:]
    numpy.save("manast_site/static/predictions/ar_man_data.npy", lag)
    # save the last ob
    numpy.save("manast_site/static/predictions/ar_man_obs.npy", [series.values[-1]])

    # load model
    model = AutoRegResults.load("manast_site/static/predictions/ar_model.pkl")
    data = numpy.load("manast_site/static/predictions/ar_data.npy")
    last_ob = numpy.load("manast_site/static/predictions/ar_obs.npy")
    # make prediction
    predictions = model.predict(start=len(data), end=len(data))
    # transform prediction
    yhat_ar = predictions[0] + last_ob[0]
    rmse_ar = sqrt(mean_squared_error(test, predictions[:len(predictions) - 1]))

    direction = "manast_site/static/predictions/predictionAR.png"
    direction_ar = "predictions/predictionAR.png"
    pyplot.close()
    pyplot.plot(test, color='blue', label=_("Results"))
    pyplot.plot(predictions, color='red', label=_("Predictions"))
    pyplot.legend()
    pyplot.savefig(direction)

    # MA

    model_ma = ARMA(train, order=(0, 0))
    model_fit_ma = model_ma.fit(disp=False)

    # save model to file
    model_fit_ma.save("manast_site/static/predictions/ma_model.pkl")
    # save the differenced dataset
    numpy.save("manast_site/static/predictions/ma_data.npy", x)
    # save the last ob
    numpy.save("manast_site/static/predictions/ma_obs.npy", [series.values[-1]])

    # save coefficients
    coef = model_fit_ma.params
    numpy.save("manast_site/static/predictions/ma_man_model.npy", coef)
    # save lag
    lag = x[-window:]
    numpy.save("manast_site/static/predictions/ma_man_data.npy", lag)
    # save the last ob
    numpy.save("manast_site/static/predictions/ma_man_obs.npy", [series.values[-1]])

    # load model
    model = AutoRegResults.load("manast_site/static/predictions/ma_model.pkl")
    data = numpy.load("manast_site/static/predictions/ma_data.npy")
    last_ob = numpy.load("manast_site/static/predictions/ma_obs.npy")
    # make prediction
    predictions = model.predict(start=len(data), end=len(data))
    # transform prediction
    yhat_ma = predictions[0] + last_ob[0]
    rmse_ma = sqrt(mean_squared_error(test, predictions[:len(predictions) - 1]))

    # ARMA

    model_arma = ARMA(train, order=(window, 0))
    model_fit_arma = model_arma.fit(disp=False)

    # save model to file
    model_fit_arma.save("manast_site/static/predictions/arma_model.pkl")
    # save the differenced dataset
    numpy.save("manast_site/static/predictions/arma_data.npy", x)
    # save the last ob
    numpy.save("manast_site/static/predictions/arma_obs.npy", [series.values[-1]])

    # save coefficients
    coef = model_fit_arma.params
    numpy.save("manast_site/static/predictions/arma_man_model.npy", coef)
    # save lag
    lag = x[-window:]
    numpy.save("manast_site/static/predictions/arma_man_data.npy", lag)
    # save the last ob
    numpy.save("manast_site/static/predictions/arma_man_obs.npy", [series.values[-1]])

    # load model
    model = AutoRegResults.load("manast_site/static/predictions/arma_model.pkl")
    data = numpy.load("manast_site/static/predictions/arma_data.npy")
    last_ob = numpy.load("manast_site/static/predictions/arma_obs.npy")
    # make prediction
    predictions = model.predict(start=len(data), end=len(data))
    # transform prediction
    yhat_arma = predictions[0] + last_ob[0]
    rmse_arma = sqrt(mean_squared_error(test, predictions[:len(predictions) - 1]))

    prev_week = []
    error_prev_week = 0
    actual_week = []

    for v in range(6, len(series.values)):
        prev_week.append(float(series.values[v-7]))
        actual_week.append(float(series.values[v]))
        error = float(series.values[v]) - float(series.values[v-7])
        error_prev_week += abs(error)

    epd_week = error_prev_week/(len(series.values)-7)
    # print(epd_week)

    return direction_ar, yhat_ar, rmse_ar, yhat_ma, rmse_ma, yhat_arma, rmse_arma, prev_week, actual_week, error_prev_week, epd_week
