from betterforms.multiform import MultiModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')
        except AttributeError:
            pass
        return avatar


class UserAvatarForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'avatar': AvatarForm,
    }


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'direction', 'zip_code', 'phone', 'opening_times', 'holidays',)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('photo',)

    def clean_avatar(self):
        avatar = self.cleaned_data['photo']
        try:
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')
        except AttributeError:
            pass
        return avatar


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ('name', 'date',)


class ShopEditForm(MultiModelForm):
    form_classes = {
        'shop': ShopForm,
        'photo': PhotoForm,
        # 'holiday': HolidayForm,
    }
