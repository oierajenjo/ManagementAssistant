from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *
from django import forms
from betterforms.multiform import MultiModelForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)


class ShopForm(UserCreationForm):
    class Meta:
        model = Shop
        fields = ('name_shop', 'direction_shop', 'zip_code_shop', 'phone_shop', 'opening_hours_shop', 'holidays_shop',)


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


class UserAvatarForm(MultiModelForm):
    form_classes = {
        'user': UserForm,
        'avatar': AvatarForm,
    }


class ShopPhotoForm(MultiModelForm):
    form_classes = {
        'shop': ShopForm,
        'photo': PhotoForm,
    }


class HolidayForm(forms.ModelForm):
    model = Holiday
    fields = ('name', 'date',)
