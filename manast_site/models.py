from django.contrib.postgres.fields import ArrayField
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


class OpeningTime(models.Model):
    weekday = models.IntegerField(choices=WEEKDAYS, unique=True, verbose_name=_("weekday"))
    from_hour = models.TimeField(blank=True)
    rest_hour = models.TimeField(blank=True)
    comeback_hour = models.TimeField(blank=True)
    to_hour = models.TimeField(blank=True)


class Shop(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name_shop"))
    photo = models.ImageField(upload_to='shop', blank=True, default="shop/shop.png", verbose_name=_("photo_shop"),
                              storage=MediaFileSystemStorage())

    direction = models.CharField(max_length=50, blank=True, verbose_name=_("direction_shop"))

    opening_times = models.ManyToManyField(OpeningTime, verbose_name=_("opening_times_shop"),
                                           related_name='opening_times_shop', blank=True)
    zip_code = models.CharField(max_length=5, blank=True, verbose_name=_("zip_code_shop"))

    # holidays = ArrayField(models.DateField(blank=True), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")


# class Holiday(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     holiday = models.DateField(blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=_("user"), related_name='user',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, default="avatars/user.png",
                               verbose_name=_("avatar_user"), storage=MediaFileSystemStorage())

    direction = models.CharField(max_length=50, blank=True, verbose_name=_("direction_user"))
    zip_code = models.CharField(max_length=5, blank=True, verbose_name=_("zip_code_user"))

    shops = models.ManyToManyField(Shop, blank=True, verbose_name=_("shops_user"))

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
