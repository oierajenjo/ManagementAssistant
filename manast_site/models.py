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
    from_hour = models.TimeField(verbose_name=_("from_hour"), related_name='from_hour')
    rest_hour = models.TimeField(blank=True, verbose_name=_("rest_hour"), related_name='rest_hour')
    comeback_hour = models.TimeField(blank=True, verbose_name=_("comeback_hour"), related_name='comeback_hour')
    to_hour = models.TimeField(verbose_name=_("to_hour"), related_name='to_hour')


class Holiday(models.Model):
    holiday = models.DateField(verbose_name=_("holiday"), related_name='holiday')


class Shop(models.Model):
    ID = models.CharField(max_length=20, unique=True, verbose_name=_("shop_id"), related_name='shop_id',
                          on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name=_("name"), related_name='name', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='shop', blank=True, default="shop/shop.png", verbose_name=_("shop_photo"),
                              related_name='shop_photo', storage=MediaFileSystemStorage())

    direction = models.CharField(max_length=50, blank=True, verbose_name=_("direction"), related_name='direction')
    postal_code = models.IntegerField(max_length=5, blank=True, verbose_name=_("postal_code"))
    opening_times = models.ManyToManyField(OpeningTime, verbose_name=_("opening_times"), related_name='opening_times')
    holidays = models.ManyToManyField(Holiday, verbose_name=_("holidays"), related_name='holidays')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=_("user"), related_name='user',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, default="avatars/user.png",
                               verbose_name=_("avatar"), related_name='avatar', storage=MediaFileSystemStorage())

    direction = models.CharField(max_length=50, blank=True, verbose_name=_("direction"), related_name='direction')
    postal_code = models.IntegerField(max_length=5, blank=True, verbose_name=_("postal_code"))

    shops = models.ManyToManyField(Shop, verbose_name=_("shops"), related_name='shops', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
