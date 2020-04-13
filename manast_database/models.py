from django.db import models


class Item(models.Model):
    item_id = models.CharField(max_length=16, verbose_name=_("DB ID"), unique=True)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class Sold(models.Model):
    db_id = models.ForeignKey(Item, )
    name = models.CharField(max_length=30)
    price = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")