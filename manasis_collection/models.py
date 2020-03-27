from datetime import datetime
from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from manasis_database.models import Product


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_("game version"))
    price = models.FloatField(default=0.0, verbose_name=_("price"))

    date_adquired = models.DateField(blank=True, null=True, verbose_name=_("date adquired"))
    time_played = models.FloatField(blank=True, null=True, verbose_name=_("time played"))

    class Meta:
        abstract = True
        unique_together = ('user', 'game_version',)

    def __str__(self):
        return self.game_version.__str__()
