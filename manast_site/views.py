import io
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.utils.translation import gettext_lazy

from manast_database.models import Item, Category
from manast_site.forms import *
from manast_site.models import *
from .functions import *


def index(request):
    if not request.user.is_authenticated:
        return render(request, "registration/login_register.html")

    return redirect(profile_view)


def login_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.last()
            user.save()
            return HttpResponseRedirect('login')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # faster than len()
                    if Profile.objects.filter(user=user).count() == 0:
                        profile = Profile(user=user)
                        profile.save()
                    login(request, user)
                    return HttpResponseRedirect('/')
    else:
        form = UserForm()

    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'registration/login_register.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("login")


@login_required(login_url='login')
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        "profile": profile,
    }
    return render(request, "account/profile_view.html", context)


@login_required(login_url='login')
def shop_view(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)
    list_hours = Shop.get_opening_days(shop)
    context = {
        "profile": profile,
        "shop": shop,
        "hours": list_hours
    }
    return render(request, "shop/shop_view.html", context)


@login_required(login_url='login')
def edit_user(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserAvatarForm(request.POST, request.FILES, instance={
            'user': request.user,
            'avatar': Profile.objects.get(user=request.user),
        })
        if form.is_valid():
            form.save()
            return redirect(profile_view)
    else:
        form = UserAvatarForm

    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'account/edit_user.html',
                  {'user': request.user, 'profile': profile})


@login_required(login_url='login')
def holiday(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    if request.method == 'POST':
        form = HolidayForm(request.POST, request.FILES, instance={
            'holidays': shop.holidays,
        })
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/shop/' + str(shop.pk))
    else:
        form = HolidayForm

    token = {}
    token.update(csrf(request))
    token['form'] = form

    context = {
        "profile": profile,
        "holidays": shop.holidays,
    }

    return render(request, 'shop/holidays.html', context)


@login_required(login_url='login')
def edit_shop(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    if request.method == 'POST':
        form = ShopEditForm(request.POST, request.FILES, instance={
            'shop': shop,
            'photo': shop,
            'holiday': shop.holidays,
        })
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/shop/' + str(shop.pk))
    else:
        form = ShopEditForm

    token = {}
    token.update(csrf(request))
    token['form'] = form

    context = {
        "profile": profile,
        "shop": shop,
        "photo": shop
    }

    return render(request, 'shop/edit_shop.html', context)


@login_required(login_url='login')
def new_shop(request):
    profile = Profile.objects.get(user=request.user)
    shop = profile.shops.create(name="new")

    return redirect(edit_shop, pk=shop.pk)


@login_required(login_url='login')
def delete_shop(request, pk):
    shop = Shop.objects.get(pk=pk)
    shop.delete()
    return redirect(profile_view)


@login_required(login_url='login')
def data_upload(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)
    text = gettext_lazy('Title of the file "01Ventas(semana05-2020).csv" Order of the CSV should be Day, Item, Price, '
                        'Quantity, Cost, Category')
    context = {
        "profile": profile,
        "shop": shop,
        'order': text,
    }

    if request.method == 'GET':
        return render(request, "shop/upload.html", context)

    else:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')
        else:
            file_name = request.FILES['file'].name
            week = file_name[-12:-10]
            year = file_name[-9:-5]
            # "01Ventas(semana05-2020)"
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=';', quotechar="|"):
                _, created = Category.objects.update_or_create(
                    name=column[5]
                )
                _, created2 = Item.objects.update_or_create(
                    name=column[1],
                    category=Category.objects.get(name=column[5]),
                    shop=Shop.objects.get(pk=pk)
                )
                _, created3 = Sale.objects.update_or_create(
                    date=get_day(column[0], week, year),
                    item=Item.objects.get(name=column[1]),
                    price=float(column[2].replace(',', '.')),
                    quantity=float(column[3].replace(',', '.')),
                    cost=float(column[4].replace(',', '.')),
                    shop=Shop.objects.get(pk=pk)
                )

    return render(request, "shop/upload.html", context)



@login_required(login_url='login')
def sales_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    sales = get_all_sales(shop)

    ben_c = benefits_category(sales)
    ben_c_keys = []
    for bk in ben_c.keys():
        ben_c_keys.append(bk)

    ben_i = benefits_item(sales)
    ben_i_keys = []
    for bk in ben_i.keys():
        ben_i_keys.append(bk)

    context = {
        "profile": profile,
        "shop": shop,
        "sales": sales,
        "benefitsCategory": ben_c,
        "benefitsCategory_keys": ben_c_keys,
        "benefitsItems": ben_i,
        "benefitsItems_keys": ben_i_keys,
    }
    return render(request, "shop/tables/sales_table.html", context)


@login_required(login_url='login')
def expenses_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    expenses = get_all_expenses(shop)

    exp_c = expenses_category(expenses)
    exp_c_keys = []
    for bk in exp_c.keys():
        exp_c_keys.append(bk)

    exp_i = expenses_item(expenses)
    exp_i_keys = []
    for bk in exp_i.keys():
        exp_i_keys.append(bk)

    context = {
        "profile": profile,
        "shop": shop,
        "expenses": expenses,
        "expensesCategory": exp_c,
        "expensesCategory_keys": exp_c_keys,
        "expensesItems": exp_i,
        "expensesItems_keys": exp_i_keys,
    }
    return render(request, "shop/tables/expenses_table.html", context)


@login_required(login_url='login')
def stats_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    # expenses = get_all_expenses(shop)
    sales = get_all_sales(shop)

    ben_per_week = benefits_week(sales)
    ben_per_week_keys = []
    for bk in ben_per_week["final"].keys():
        ben_per_week_keys.append(int(bk))

    ben_per_day = benefits_per_day(sales)
    ben_per_day_keys = []
    for bk in ben_per_day["final"].keys():
        ben_per_day_keys.append(int(bk))

    # week = range(1, 53)
    # week_list = []
    # for wl in week:
    #     week_list.append(wl)

    context = {
        "profile": profile,
        "shop": shop,
        "sales": sales,
        # "expenses": expenses,
        "benefits_per_week": ben_per_week["final"],
        "benefits_per_week_keys": ben_per_week_keys,
        "week_list": ben_per_week["week_list"],
        "benefits_per_day": ben_per_day["final"],
        "benefits_per_day_keys": ben_per_day_keys,
        "days_list": ben_per_day["days"]
    }

    return render(request, "shop/tables/stats_table.html", context)


@login_required(login_url='login')
def predictions_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    expenses = get_all_expenses(shop)
    sales = get_all_sales(shop)

    # arima = arima_prediction(sales)
    # ax, pred_mean_dates, values_mean, pred_mean = pred_by_mean(sales)
    pred_mean_dates, values_mean, pred_mean = pred_by_mean(sales)
    # response = HttpResponse(content_type='image/png')
    # ax.show()
    direction, prediction = pred_forecast(sales)

    context = {
        "profile": profile,
        "shop": shop,
        "sales": sales,
        "expenses": expenses,
        "pred_mean_dates": pred_mean_dates,
        "values_mean": values_mean,
        "pred_mean": pred_mean,
        "direction": direction,
        "prediction": prediction
        # "history": arima["history"],
    }

    return render(request, "shop/tables/predictions_table.html", context)

