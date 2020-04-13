from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext_lazy as _


class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise (Exception("The file is bigger than supported"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            return name
        return super(MediaFileSystemStorage, self)._save(name, content)


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=_("user"), related_name='user',
                                on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars', blank=True, default="avatars/user.png",
                               verbose_name=_("avatar"), storage=MediaFileSystemStorage())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


class Shop(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=_("shop"), related_name='shop',
                            on_delete=models.CASCADE)
    direction = models.CharField(max_length=50)
    PD = models.IntegerField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")
