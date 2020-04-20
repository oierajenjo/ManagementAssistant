from django.db import models
from django.utils.translation import ugettext_lazy as _

from manast_site.models import Profile, Shop

TYPE = [
    (1, _("Employee")),
    (2, _("Clothes")),
    (3, _("Lottery")),
    (4, _("Goods")),
    (5, _("Paper")),
    (6, _("Electronic")),
    (7, _("Leisure")),
]


class Item(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name_item"))
    type = models.IntegerField(choices=TYPE, verbose_name=_("type_item"))
    in_inventory = models.IntegerField(blank=True, verbose_name=_("in_inventory_item"))

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class Expense(models.Model):
    item = models.ManyToManyField(Item)
    quantity = models.IntegerField(verbose_name=_("quantity_expense"))
    cost = models.FloatField(verbose_name=_("cost_expense"))
    date = models.DateField(verbose_name=_("date_expense"))

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")


class Sale(models.Model):
    item = models.ManyToManyField(Item)
    quantity = models.IntegerField(verbose_name=_("quantity_sale"))
    price = models.FloatField(blank=True, verbose_name=_("price_sale"))
    cost = models.FloatField(verbose_name=_("cost_sale"))
    date = models.DateField(verbose_name=_("date_sale"))

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")
