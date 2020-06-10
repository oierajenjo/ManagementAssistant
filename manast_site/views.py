import csv
import io
import os

from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf

from manast_database.models import Item, Category
from manast_site.forms import *
from manast_site.models import *
from .functions import *


def index(request):
    if not request.user.is_authenticated:
        return render(request, "registration/login_register.html")

    return profile_view(request)


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
    context = {
        "profile": profile,
        "shop": shop
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
            return HttpResponseRedirect('/')
    else:
        form = UserAvatarForm

    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render(request, 'account/edit_user.html',
                  {'user': request.user, 'profile': profile})


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
            return HttpResponseRedirect('/')
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
def sales_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    sales = get_all_sales(shop)

    context = {
        "profile": profile,
        "shop": shop,
        "sales": sales,
    }

    return render(request, "shop/tables/sales_table.html", context)


# Create your views here.
def data_upload(request, pk):
    template = "upload.html"
    prompt = {
        'order': 'Order of the CSV should be Día, Item, Price, Quantity, Cost, Categoria'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'Please upload a .csv file.')

    file_name = os.path.splitext(os.path.basename('file'))[0]
    week = file_name[-8:-6]
    year = file_name[-5:-1]
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
            category=column[5],
            shop=Shop.objects.get(pk=pk)
        )
        _, created3 = Sale.objects.update_or_create(
            date=get_day(column[0], week, year),
            item=column[1],
            price=column[2],
            quantity=column[3],
            # cost=column[4],
            shop=Shop.objects.get(pk=pk)
        )

    context = {
        # 'tables': Table.objects.all()
    }
    return render(request, template, context)


@login_required(login_url='login')
def expenses_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    expenses = get_all_expenses(shop)

    context = {
        "profile": profile,
        "shop": shop,
        "expenses": expenses,
    }

    return render(request, "shop/tables/expenses_table.html", context)


@login_required(login_url='login')
def stats_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    expenses = get_all_expenses(shop)
    sales = get_all_sales(shop)

    context = {
        "profile": profile,
        "shop": shop,
        "sales": sales,
        "expenses": expenses,
    }

    return render(request, "shop/tables/stats_table.html", context)


@login_required(login_url='login')
def predictions_table(request, pk):
    profile = Profile.objects.get(user=request.user)
    shop = Shop.objects.get(pk=pk)

    expenses = get_all_expenses(shop)
    sales = get_all_sales(shop)

    predictions = None

    context = {
        "profile": profile,
        "shop": shop,
        "sales": sales,
        "expenses": expenses,
        "predictions": predictions
    }

    return render(request, "shop/tables/predictions_table.html", context)

# @login_required(login_url='login')
# def download_csv(request):
#     if request.method == 'POST':
#         response = HttpResponse(content_type='text/csv')
#         data = request.POST.getlist("data")
#
#         response['Content-Disposition'] = 'attachment; filename="%s.csv"' % request.POST.get("filename")
#
#         writer = csv.writer(response)
#
#         headers = json.loads(data[0].replace("'", '"'))
#         writer.writerow(headers.keys())
#
#         for row in data:
#             title = json.loads(row.replace("'", '"'))
#
#             if 'original_title' in title:
#                 title["game"] = title["original_title"]
#                 title.pop("original_title")
#
#             writer.writerow(list(title.values()))
#
#         return response
#
# def calendar(request):
#     return render(request, 'calendar_pic.html')
