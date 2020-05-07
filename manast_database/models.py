import calendar
import datetime
from datetime import date

from django.db import models
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _

from ManagementAssistant import settings
from manast_site.models import Profile, Shop

# CURRENCY = settings.CURRENCY


PERIODIC = [
    (1, _("Daily")),
    (2, _("Weekly")),
    (3, _("Monthly ")),
    (4, _("Annual")),
]


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name_category"))
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Item(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name_item"))
    category = models.ForeignKey(Category, verbose_name=_("type_item"), on_delete=models.CASCADE)
    # in_inventory = models.IntegerField(blank=True, verbose_name=_("in_inventory_item"))
    # price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("price"))
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class Expense(models.Model):
    item_exp = models.ManyToManyField(Item, on_delete=models.CASCADE)
    quantity_exp = models.DecimalField(default=0.00, decimal_places=2, max_digits=10,
                                       verbose_name=_("quantity_expense"))
    cost_exp = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("cost_expense"))
    date_exp = models.DateField(default=date.today, input_formats=settings.DATE_INPUT_FORMATS,
                                verbose_name=_("date_expense"))
    periodicity_exp = models.IntegerField(PERIODIC, default=1)
    shop_exp = models.ForeignKey(Shop, on_delete=models.CASCADE)
    repeat_exp = models.BooleanField(default=False, verbose_name=_("repeat_expense"))

    # Get the working days in a week
    def week_workdays(self):
        week_list = self.shop_exp.get_opening_days()

        day = self.date_exp
        mon = day - datetime.timedelta(days=day.weekday())

        holidays = self.shop_exp.holidays
        final_days = week_list
        for i in range(7):
            d = mon + datetime.timedelta(days=i)
            if week_list.check(d.weekday):
                if holidays.check(d):
                    final_days.remove(d.weekday())
        return len(final_days)

    # Get period of expense
    def period_total(self):
        if self.periodicity_exp == 1:  # Daily
            return 1
        elif self.periodicity_exp == 2:  # Weekly
            return self.week_workdays
        elif self.periodicity_exp == 3:  # Monthly
            return calendar.monthrange(self.date_exp.year, self.date_exp.month)[1]
        elif self.periodicity_exp == 4:  # Annual
            return (date(self.date_exp.year, 1, 1) - date(self.date_exp.year, 12, 31)).days

    # Get total cost per day
    def total_cost_per_day(self):
        return (self.quantity_exp * self.cost_exp) / self.period_total()

    # Get total cost
    def total_cost(self):
        return self.quantity_exp * self.cost_exp

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")


class Sale(models.Model):
    item_sale = models.ManyToManyField(Item, on_delete=models.CASCADE)
    quantity_sale = models.DecimalField(default=0.0000, decimal_places=4, max_digits=10,
                                        verbose_name=_("quantity_sale"))
    price_sale = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("price_sale"))
    # discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("discount"))
    cost_sale = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("cost_sale"))
    date_sale = models.DateField(verbose_name=_("date_sale"))
    # final_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name=_("final_value"))

    shop_sale = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def benefits(self):
        return self.price_sale - self.cost_sale

    def benefits_per_product(self):
        return (self.price_sale - self.cost_sale)/self.quantity_sale

    # def benefits(self):
    #     return self.quantity * (self.item.price - self.discount) - self.quantity * self.cost

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")

    # def tag_final_value(self):
    #     return f'{self.final_value} {CURRENCY}'
    #
    # tag_final_value.short_description = 'Value'
