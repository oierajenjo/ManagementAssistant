from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext_lazy as _

WEEKDAYS = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


class MediaFileSystemStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise (Exception("The file is bigger than supported"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            return name
        return super(MediaFileSystemStorage, self)._save(name, content)


class OpeningHours(models.Model):
    op_weekday = models.IntegerField(choices=WEEKDAYS, unique=True, verbose_name=_("weekday"))

    from_hour = models.TimeField(blank=True)
    rest_hour = models.TimeField(blank=True)
    comeback_hour = models.TimeField(blank=True)
    to_hour = models.TimeField(blank=True)

    class Meta:
        ordering = ('op_weekday', 'from_hour')
        unique_together = ('op_weekday', 'from_hour', 'rest_hour', 'comeback_hour', 'to_hour')

    def __unicode__(self):
        if self.rest_hour is None and self.comeback_hour is None and self.from_hour is not None \
                and self.to_hour is not None:
            return u'%s: %s - %s' % (self.get_op_weekday_display(), self.from_hour, self.to_hour)
        elif self.from_hour is None and self.to_hour is None:
            return u'closed'
        else:
            return u'%s: %s - %s; %s - %s' % (self.get_op_weekday_display(), self.from_hour, self.rest_hour,
                                              self.comeback_hour, self.to_hour)


class Holiday(models.Model):
    name = models.CharField(blank=True, max_length=30, unique=True, verbose_name=_("holiday_name"))
    date = models.DateField(blank=True, unique=True, verbose_name=_("holiday_date"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Holiday")
        verbose_name_plural = _("Holidays")


class Shop(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name_shop"))
    photo = models.ImageField(upload_to='shops', blank=True, default="shops/shop.png", verbose_name=_("photo"),
                              storage=MediaFileSystemStorage())

    direction = models.CharField(max_length=50, blank=True, verbose_name=_("direction_shop"))
    zip_code = models.CharField(max_length=5, blank=True, verbose_name=_("zip_code_shop"))
    phone = models.CharField(max_length=9, blank=True, verbose_name=_("phone_shop"))

    opening_times = models.ManyToManyField(OpeningHours, verbose_name=_("opening_hours_shop"),
                                           related_name='opening_hours_shop', blank=True)
    holidays = models.ManyToManyField(Holiday, verbose_name=_("holidays_shop"), related_name='holidays_shop', blank=True)

    def __str__(self):
        return self.name

    def get_opening_days(self):
        list_days = list(range(0, 7))
        for op in self.opening_times.all:
            if op.from_hour is None and op.to_hour is None:
                list_days.remove(op.op_weekday)

        return list_days

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=_("user"), related_name='user',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, default="avatars/user.png", verbose_name=_("avatar"),
                               storage=MediaFileSystemStorage())

    shops = models.ManyToManyField(Shop, blank=True, verbose_name=_("shops_user"))

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
