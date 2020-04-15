from django.db import models
from django.utils.translation import ugettext_lazy as _

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
    item_id = models.CharField(max_length=16, verbose_name=_("item ID"), related_name='item ID', unique=True,
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name=_("name"), related_name='name')
    type = models.IntegerField(choices=TYPE, verbose_name=_("type"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class Expense(models.Model):
    item = models.ForeignKey(Item, verbose_name=_("item"), related_name='item', on_delete=models.CASCADE)
    cost = models.FloatField(verbose_name=_("cost"))

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")


class Sale(models.Model):
    item = models.ForeignKey(Item, verbose_name=_("item"), related_name='item', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name=_("quantity"))
    price = models.FloatField(verbose_name=_("price"))
    cost = models.FloatField(verbose_name=_("cost"))
    date = models.DateField(verbose_name=_("date"), related_name='date')

    class Meta:
        verbose_name = _("Sale")
        verbose_name_plural = _("Sales")
