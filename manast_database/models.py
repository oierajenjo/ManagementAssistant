import calendar
import datetime
from datetime import date

from django.db import models
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _

from manast_site.models import Profile, Shop

# CURRENCY = settings.CURRENCY

PERIODIC = [
    (1, _("Daily")),
    (2, _("Weekly")),
    (3, _("Monthly")),
    (4, _("Annual")),
]


class Category(models.Model):
    name = models.CharField(max_length=30, primary_key=True, verbose_name=_("name_category"), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Item(models.Model):
    name = models.CharField(max_length=30, primary_key=True, verbose_name=_("name_item"), unique=True)
    category = models.ForeignKey(Category, verbose_name=_("category_item"), on_delete=models.CASCADE, blank=True)
    # in_inventory = models.IntegerField(blank=True, verbose_name=_("in_inventory_item"))
    # price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("price"))
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class Expense(models.Model):
    item = models.ForeignKey(Item, verbose_name=_("item_exp"), on_delete=models.CASCADE)
    quantity = models.DecimalField(default=1.00, decimal_places=2, max_digits=10, verbose_name=_("quantity_expense"))
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("cost_expense"))
    date = models.DateField(default=date.today, verbose_name=_("date_exp"))
    periodicity = models.IntegerField(PERIODIC, default=1)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    repeat = models.BooleanField(default=False, verbose_name=_("repeat_expense"))

    # Get the working days in a week
    def week_workdays(self):
        week_list = self.shop.get_opening_days()

        day = self.date
        mon = day - datetime.timedelta(days=day.weekday())

        holidays = self.shop.holidays
        final_days = week_list
        for i in range(7):
            d = mon + datetime.timedelta(days=i)
            if week_list.check(d.weekday):
                if holidays.check(d):
                    final_days.remove(d.weekday())
        return len(final_days)

    # Get period of expense
    def period_total(self):
        if self.repeat:
            if self.periodicity == 1:  # Daily
                return 1
            elif self.periodicity == 2:  # Weekly
                return self.week_workdays
            elif self.periodicity == 3:  # Monthly
                return calendar.monthrange(self.date.year, self.date.month)[1]
            elif self.periodicity == 4:  # Annual
                return (date(self.date.year, 1, 1) - date(self.date.year, 12, 31)).days
        else:
            return 0

    # Get total cost per day
    def total_cost_per_day(self):
        return (self.quantity * self.cost) / self.period_total()

    # Get total cost
    def total_cost(self):
        return self.quantity * self.cost

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")


class Sale(models.Model):
    item = models.ForeignKey(Item, verbose_name=_("item_sale"), on_delete=models.CASCADE)
    quantity = models.DecimalField(default=1.00, decimal_places=4, max_digits=10, verbose_name=_("quantity_sale"))
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("price_sale"))
    # discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("discount"))
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("cost_sale"))
    date = models.DateField(default=date.today, verbose_name=_("date_sale"))
    # final_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("final_value"))

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def benefits(self):
        return self.price - self.cost * self.quantity

    def benefits_per_product(self):
        return self.price / self.quantity - self.cost

    # def benefits(self):
    #     return self.quantity * (self.item.price - self.discount) - self.quantity * self.cost

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")
